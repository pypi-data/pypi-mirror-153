from threading import Thread, Event

import canopen
from olaf import Resource, OreSatFileCache, logger


class MockApp(Thread):
    def __init__(self):
        super().__init__()
        logger.disable('olaf')
        self.node = canopen.LocalNode(0x10, 'olaf/data/oresat_app.eds')
        self.fread_cache = OreSatFileCache('/tmp/fread')
        self.fread_cache.clear()
        self.fwrite_cache = OreSatFileCache('/tmp/fwrite')
        self.fwrite_cache.clear()

        # python canopen does not set the value to default for some reason
        self.od = self.node.object_dictionary
        for i in self.od:
            if not isinstance(self.od[i], canopen.objectdictionary.Variable):
                for j in self.od[i]:
                    self.od[i][j].value = self.od[i][j].default

    def send_tpdo(self, tpdo: int):
        return  # don't do anything

    def add_resource(self, resource: Resource):
        self.resource = resource(
            self.node,
            self.fread_cache,
            self.fwrite_cache,
            True,
            self.send_tpdo
        )

    def run(self):
        self.event = Event()
        self.resource.on_start()
        while not self.event.is_set():
            self.resource.on_loop()
            self.event.wait(self.resource.delay)
        self.resource.on_end()

    def stop(self):
        self.event.set()
        self.join()
