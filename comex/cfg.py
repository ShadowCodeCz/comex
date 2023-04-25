import logging
import os

from . import log


class DefaultPath:
    example_cfg = "./comex.example_1.cfg.json"
    empty_batch = "./comex.default.batch.json"


class Attribute:
    logger_cfg = "logger.configuration"
    plugins_directories = "plugins.directories"
    plugins_regular_expression = "plugin.regular.expression"
    commands = "commands"
    configurations = "configurations"
    cmd_type = "cmd.type"
    configuration = "configuration"
    over_take_data = "overtake.data.from.previous.step"


def default_logger_configuration(level="DEBUG"):
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'loggers': {
            log.comEx_logger_name: {
                'level': level,
                'propagate': False,
                'handlers': ['console_handler'],
            },
        },

        'handlers': {
            'console_handler': {
                'level': level,
                'formatter': 'generic',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
        },

        'formatters': {
            'generic': {
                'format': '%(asctime)s %(levelname)s %(message)s'
            }
        },
    }


def example_configuration_1():
    return {
        Attribute.plugins_directories: [os.path.join(
            os.path.dirname(__file__),
            "demo.plugins/"
        )],
        Attribute.plugins_regular_expression: "comex.+.py$",
        Attribute.logger_cfg: default_logger_configuration(),
        Attribute.commands: [
            {
                "cmd.type": "cmd.cfg.printer",
                "variable.label": "variable.value"
            },
            {
                "cmd.type": "data.injector",
                "data.key": "key",
                "data.value": "value",
            },
            {
                "cmd.type": "fail.data.injector",
                "data.key": "key2",
                "data.value": "value2",
            },
            {
                "cmd.type": "data.printer"
            },
            {
                "cmd.type": "press.enter"
            },
        ]
    }


def example_configuration_2():
    return {
        Attribute.plugins_directories: [os.path.join(
            os.path.dirname(__file__),
            "demo.plugins/"
        )],
        Attribute.plugins_regular_expression: "comex.+.py$",
        Attribute.logger_cfg: default_logger_configuration(),
        Attribute.commands: [
            {
                "cmd.type": "data.printer"
            },
        ]
    }


def empty_batch():
    return {
        Attribute.configurations: [
            {
                "configuration": DefaultPath.example_cfg,
                "overtake.data.from.previous.step": "True"
            },
            {
                "configuration": DefaultPath.example_cfg.replace("1", "2"),
                "overtake.data.from.previous.step": "True"
            },
            {
                "configuration": DefaultPath.example_cfg.replace("1", "2"),
                "overtake.data.from.previous.step": "False"
            }
        ]
    }


def read_from_cfg(cfg, attribute, default_value):
    try:
        return cfg[attribute]
    except Exception as e:
        logger = logging.getLogger(log.comEx_logger_name)
        logger.warning(f"[ComEx] Reading attribute '{attribute}' failed. "
                       f"Default value '{default_value}' was used.\n{e}")
        return default_value
