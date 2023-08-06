from core.arguments.command_line_arguments import option_arg_parser
from logger.ConfigureLogger import ConfigureLogger
from metainfo.MetaInfo import MetaInfo

from apiautomata.server.AutomataAPIServer import AutomataAPIServer


def start():
    ConfigureLogger()

    meta_info = MetaInfo('persuader-technology-automata-api')

    command_line_arg_parser = option_arg_parser(meta_info)
    args = command_line_arg_parser.parse_args()

    server = AutomataAPIServer(args.options)
    server.run()


if __name__ == '__main__':
    start()
