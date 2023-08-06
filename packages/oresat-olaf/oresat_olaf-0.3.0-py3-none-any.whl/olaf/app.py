import sys
import errno
import struct
import signal
import subprocess
from os import geteuid
from pathlib import Path
from threading import Thread, Event

import canopen
import psutil
from loguru import logger

from .common.resource import Resource
from .common.oresat_file_cache import OreSatFileCache
from .resources.os_command import OSCommandResource
from .resources.system_info import SystemInfoResource
from .resources.file_caches import FileCachesResource
from .resources.fread import FreadResource
from .resources.fwrite import FwriteResource
from .resources.ecss import ECSSResource
from .resources.updater import UpdaterResource
from .resources.logs import LogsResource


class App:
    '''The application class that manages the CAN bus, resources, and threads.'''

    def __init__(self, eds: str, bus: str, node_id=0, mock_hw=False):
        '''
        Parameters
        ----------
        eds: str
            File path to EDS or DCF file.
        bus: str
            Which CAN bus to use.
        node_id: int, str
            The node ID. If set to 0 and DCF was used for the eds arg, the value will be pulled
            from the DCF, otherwise, it will be set to 0x7C.
        mock_hw: bool
            Flag to mock hardware. This will be pass to any resources added.

        Raises
        ------
        ValueError
            Invalid parameter(s)
        '''

        self.bus = bus
        self.event = Event()
        self.resources = []
        self.network = None
        self.mock_hw = mock_hw

        if isinstance(node_id, str):
            if node_id.startswith('0x'):
                node_id = int(node_id, 16)
            else:
                node_id = int(node_id)
        elif not isinstance(node_id, int):
            raise ValueError('node_id is not a int/hex str or a int')

        if geteuid() == 0:  # running as root
            self.work_base_dir = '/var/lib/oresat'
            self.cache_base_dir = '/var/cache/oresat'
        else:
            self.work_base_dir = str(Path.home()) + '/.oresat'
            self.cache_base_dir = str(Path.home()) + '/.cache/oresat'

        fread_path = self.cache_base_dir + '/fread'
        fwrite_path = self.cache_base_dir + '/fwrite'
        logger.debug(f'fread cache path {fread_path}')
        logger.debug(f'fwrite cache path {fwrite_path}')

        self.fread_cache = OreSatFileCache(fread_path)
        self.fwrite_cache = OreSatFileCache(fwrite_path)

        # setup event
        for sig in ['SIGTERM', 'SIGHUP', 'SIGINT']:
            signal.signal(getattr(signal, sig), self._quit)

        dcf_node_id = canopen.import_od(eds).node_id
        if node_id != 0:
            self.node_id = node_id
        elif dcf_node_id:
            self.node_id = dcf_node_id
        else:
            self.node_id = 0x7C
        self.node = canopen.LocalNode(self.node_id, eds)
        self.node.object_dictionary.node_id = self.node_id

        self.name = self.node.object_dictionary.device_information.product_name

        # python canopen does not set the value to default for some reason
        for i in self.od:
            if not isinstance(self.od[i], canopen.objectdictionary.Variable):
                for j in self.od[i]:
                    self.od[i][j].value = self.od[i][j].default

        default_rpdos = [
            0x200 + self.node_id,
            0x300 + self.node_id,
            0x400 + self.node_id,
            0x500 + self.node_id
        ]
        default_tpdos = [
            0x180 + self.node_id,
            0x280 + self.node_id,
            0x380 + self.node_id,
            0x480 + self.node_id
        ]

        # fix COB-IDs for invaild PDOs
        #
        # all oresat node RPDO COB-ID follow values of 0x[2345]00 + $NODEID
        # all oresat node TPDO COB-ID follow values of 0x[1234]80 + $NODEID
        # this fixes the values for all 16 RPDOs/TPDOs
        for i in range(len(self.node.rpdo)):
            cob_id = self.od[0x1400 + i][1].default & 0xFFF
            if cob_id in default_rpdos:
                cob_id = 0x200 + 0x100 * (i % 4) + self.node_id + i // 4
            else:
                cob_id = self.od[0x1400 + i][1].default
            self.od[0x1400 + i][1].value = cob_id
        for i in range(len(self.node.tpdo)):
            cob_id = self.od[0x1800 + i][1].default & 0xFFF
            if cob_id in default_tpdos:
                cob_id = 0x180 + 0x100 * (i % 4) + self.node_id + i // 4
            else:
                cob_id = self.od[0x1800 + i][1].default
            self.od[0x1800 + i][1].value = cob_id

        # default resources
        self.add_resource(OSCommandResource)
        self.add_resource(ECSSResource)
        self.add_resource(SystemInfoResource)
        self.add_resource(FileCachesResource)
        self.add_resource(FreadResource)
        self.add_resource(FwriteResource)
        self.add_resource(UpdaterResource)
        self.add_resource(LogsResource)

    def __del__(self):

        self.stop()

        try:
            self.network.disconnect()
        except Exception as exc:
            logger.error(exc)

    def _quit(self, signo, _frame):
        '''Called when signals are caught'''

        logger.debug(f'signal {signal.Signals(signo).name} was caught')
        self.stop()

    def send_tpdo(self, tpdo: int):
        '''Send a TPDO. Will not be sent if not node is not in operational state.

        Parameters
        ----------
        tpdo: int
            TPDO number to send
        '''

        # PDOs can't be sent if CAN bus is down and PDOs should not be sent if CAN bus not in
        # 'OPERATIONAL' state
        can_bus = psutil.net_if_stats().get(self.bus)
        if not can_bus or (can_bus.isup and self.node.nmt.state != 'OPERATIONAL'):
            return

        cob_id = self.od[0x1800 + tpdo][1].value
        maps = self.od[0x1A00 + tpdo][0].value

        data = b''
        for i in range(maps):
            pdo_map = self.od[0x1A00 + tpdo][i + 1].value

            if pdo_map == 0:
                break  # nothing todo

            pdo_map_bytes = pdo_map.to_bytes(4, 'big')
            index, subindex, length = struct.unpack('>HBB', pdo_map_bytes)

            # call sdo callback(s) and convert data to bytes
            if isinstance(self.od[index], canopen.objectdictionary.Variable):
                value = self.node.sdo[index].phys
                value_bytes = self.od[index].encode_raw(value)
            else:  # record or array
                value = self.node.sdo[index][subindex].phys
                value_bytes = self.od[index][subindex].encode_raw(value)

            # pack pdo with bytes
            data += value_bytes

        try:
            self.network.send_message(cob_id, data)
        except Exception:
            pass

    def _send_tpdo_loop(self, tpdo: int):

        while not self.event.is_set():
            self.send_tpdo(tpdo)

            # get event time
            value = self.od[0x1800 + tpdo][5].value

            # milliseconds as int to seconds as a float
            delay = float(value) / 1000

            self.event.wait(delay)

    def add_resource(self, resource: Resource):
        '''Add a resource for the app'''

        res = resource(
            self.node,
            self.fread_cache,
            self.fwrite_cache,
            self.mock_hw,
            self.send_tpdo
        )
        logger.debug(f'adding {res.__class__.__name__} resources')
        self.resources.append(res)

    def _run_resource(self, resource):
        '''Run the resource'''

        while not self.event.is_set():
            try:
                resource.on_loop()
            except Exception as exc:  # nothing fancy just end return if the resource loop fails
                name = resource.__class__.__name__
                msg = f'{name} resource\'s on_loop raised an uncaught exception: {exc}'
                logger.critical(msg)
                break

            if resource.delay > 0:
                self.event.wait(resource.delay)

    def run(self) -> int:
        '''Go into operational mode, start all the resources, start all the threads, and monitor
        everything in a loop.

        Returns
        -------
        int
            Errno value or 0 for on no error.
        '''
        tpdo_threads = []
        resource_threads = {}

        logger.info(f'{self.name} app is starting')
        if geteuid() != 0:  # running as root
            logger.warning('not running as root, cannot restart CAN bus if it goes down')

        if not psutil.net_if_stats().get(self.bus):
            logger.critical(f'{self.bus} does not exist, nothing OLAF can do, exiting')
            return errno.ENETUNREACH

        for resource in self.resources:
            try:
                resource.on_start()
            except Exception as exc:
                name = resource.__class__.__name__
                msg = f'{resource} resource\'s on_start raised an uncaught exception: {exc}'
                logger.critical(msg)
                continue

            if resource.delay >= 0:
                name = resource.__class__.__name__
                t = Thread(name=name, target=self._run_resource, args=(resource,))
                logger.debug(f'starting {t.name} resource thread')
                t.start()
                resource_threads[t] = resource

        for i in range(len(self.node.tpdo)):
            transmission_type = self.od[0x1800 + i][2].default
            event_time = self.od[0x1800 + i][5].default

            if transmission_type in [0xFE, 0xFF] and event_time and event_time > 0:
                t = Thread(name='TPDO' + str(i + 1), target=self._send_tpdo_loop, args=(i,))
                logger.debug(f'starting {t.name} thread')
                t.start()
                tpdo_threads.append(t)

        logger.info(f'{self.name} app is running')
        while not self.event.is_set():
            if not psutil.net_if_stats().get(self.bus):
                logger.critical(f'{self.bus} no longer exists, nothing OLAF can do, exiting')
                self.event.set()
                break
            elif not psutil.net_if_stats().get(self.bus).isup:
                logger.error(f'{self.bus} is down')
                if self.network:
                    self.network = None
                if geteuid() == 0:  # running as root
                    logger.info(f'trying to restart CAN bus {self.bus}')
                    out = subprocess.run(f'ip link set {self.bus} up', shell=True)
                    if out.returncode != 0:
                        logger.error(out)
            else:
                if not self.network:
                    logger.debug('(re)starting can network')
                    self.network = canopen.Network()
                    self.network.connect(bustype='socketcan', channel=self.bus)
                    self.network.add_node(self.node)
                    try:
                        self.node.nmt.state = 'PRE-OPERATIONAL'
                        self.node.nmt.start_heartbeat(self.od[0x1017].default)
                        self.node.nmt.state = 'OPERATIONAL'
                    except Exception as exc:
                        logger.error(exc)

                # monitor threads
                for t in tpdo_threads:
                    if not t.is_alive:
                        logger.error(f'tpdo thread {t.name} has ended')
                        t.join()
                        tpdo_threads.remove(t)
                for t in resource_threads:
                    if not t.is_alive:
                        logger.error(f'resource thread {t.name} has ended')
                        t.join()
                        try:
                            resource_threads[t].on_end()
                        except Exception as exc:
                            logger.critical(f'{resource_threads[t].name} resource\'s on_end raised'
                                            f' an uncaught exception: {exc}')
                        del resource_threads[t]

            self.event.wait(1)

        for resource in self.resources:
            try:
                resource.on_end()
            except Exception as exc:
                msg = f'{resource.name} resource\'s on_end raised an uncaught exception: {exc}'
                logger.critical(msg)

        for t in tpdo_threads:
            logger.debug(f'joining {t.name} thread')
            t.join()

        for t in resource_threads:
            logger.debug(f'joining {t.name} resource thread')
            t.join()

        logger.info(f'{self.name} app has ended')
        return 0

    def stop(self):
        '''End the run loop'''

        logger.info(f'{self.name} app is stopping')
        self.event.set()

    @property
    def od(self):
        '''For convenience. Access to the object dictionary.'''

        return self.node.object_dictionary
