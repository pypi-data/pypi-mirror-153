import uvicorn
from missingrepo.repository.MissingRepository import MissingRepository

from apiautomata.holder.ItemHolder import ItemHolder


class AutomataAPIServer:

    def __init__(self, options):
        self.options = options
        self.port = options['API_SERVER_PORT']
        self.init_dependencies()

    def init_dependencies(self):
        item_holder = ItemHolder()
        item_holder.add(self.options['VERSION'], 'version')
        item_holder.add_entity(MissingRepository(self.options))

    def run(self):
        uvicorn.run('apiautomata.API:app', port=self.port, access_log=False)
