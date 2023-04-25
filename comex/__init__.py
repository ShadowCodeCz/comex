import argparse
import logging
import logging.config

from . import cli
from . import log
from . import cfg
from . import plugin


def main():
    parser = argparse.ArgumentParser(
        description="ComEx - Command Executor",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("-l", "--logger_level", default="DEBUG")
    subparsers = parser.add_subparsers()

    run_parser = subparsers.add_parser('run')
    run_parser.set_defaults(func=cli.run)
    run_parser.add_argument("-c", "--configuration", required=True)

    gen_cfg_parser = subparsers.add_parser('gen-cfg')
    gen_cfg_parser.add_argument("-e", "--example", default="1")
    gen_cfg_parser.set_defaults(func=cli.generate_example_cfg_file)

    gen_batch_parser = subparsers.add_parser('gen-batch')
    gen_batch_parser.set_defaults(func=cli.generate_empty_batch_file)

    batch_parser = subparsers.add_parser('batch')
    batch_parser.add_argument("-b", "--batch_file", required=True)
    batch_parser.set_defaults(func=cli.batch)

    list_parser = subparsers.add_parser('list')
    list_parser.set_defaults(func=cli.list_plugins)
    list_parser.add_argument("-c", "--configuration", required=True)

    arguments = parser.parse_args()
    logging.config.dictConfig(cfg.default_logger_configuration(arguments.logger_level))
    arguments.func(arguments)

