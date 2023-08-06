import logging

import uvicorn
from missingrepo.repository.MissingRepository import MissingRepository

from apiautomata.holder.ItemHolder import ItemHolder


class AutomataAPIServer:

    def __init__(self, options):
        self.log = logging.getLogger(__name__)
        self.options = options
        self.host = options['API_SERVER_HOST']
        self.port = options['API_SERVER_PORT']
        self.init_dependencies()

    def init_dependencies(self):
        self.log.info('Initializing dependencies')
        item_holder = ItemHolder()
        item_holder.add(self.options['VERSION'], 'version')
        item_holder.add_entity(MissingRepository(self.options))

    def run(self):
        self.log.info('Running')
        uvicorn.run('apiautomata.API:app', host=self.host, port=self.port, access_log=False)
