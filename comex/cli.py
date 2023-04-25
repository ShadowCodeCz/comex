import json
import logging
import os
import traceback

from prettytable import PrettyTable

from . import core
from . import cfg
from . import log


def run_single_configuration(configuration_path, data):
    logger = logging.getLogger(log.comEx_logger_name)
    logger.debug(f"[ComEx] "
                 f"====================="
                 f" C O M E X   R U N   {configuration_path} "
                 f"=====================")
    executor = core.ComEx()

    with open(configuration_path) as json_file:
        cfg = json.load(json_file)
        executor.run(cfg, data)

    return executor.data


def run(arguments):
    try:
        run_single_configuration(arguments.configuration, {})
    except Exception as e:
        logger = logging.getLogger(log.comEx_logger_name)
        logger.error(f"[ComEx] Error during processing '{arguments.configuration}'. Exception({e})")
        logger.error(f"[ComEx] Traceback\n{traceback.format_exc()}")


def generate_example_cfg_file(arguments):
    logger = logging.getLogger(log.comEx_logger_name)
    path = cfg.DefaultPath.example_cfg.replace("1", str(arguments.example))
    if not os.path.exists(path):
        with open(path, "w+") as cfg_file:
            logger.info(f"[ComEx] Empty configuration was generated in path '{path}'. "
                        f"Note that attribute '{cfg.Attribute.logger_cfg}' can be completely remove. "
                        f"Default logger will be used instead.")
            content = cfg.example_configuration_1() if int(arguments.example) == 1 else cfg.example_configuration_2()
            json.dump(content, cfg_file, indent="    ")
    else:
        logger.warning(f"[ComEx] Target file '{path}' already exists.")


def batch(arguments):
    logger = logging.getLogger(log.comEx_logger_name)
    data = {}
    try:
        with open(arguments.batch_file) as batch_file:
            batch = json.load(batch_file)

        for specification in batch[cfg.Attribute.configurations]:
            over_take_data = cfg.read_from_cfg(specification, cfg.Attribute.over_take_data, "false")
            if str(over_take_data).lower() == "true":
                data = run_single_configuration(specification[cfg.Attribute.configuration], data)
            else:
                data = run_single_configuration(specification[cfg.Attribute.configuration], {})

    except Exception as e:
        logger.error(f"[ComEx] Error during processing '{arguments.batch_file}'. Exception({e})")
        logger.error(f"[ComEx] Traceback\n{traceback.format_exc()}")


def list_plugins(arguments):
    with open(arguments.configuration) as json_file:
        cfg = json.load(json_file)
        executor = core.ComEx()
        executor.cfg = cfg
        executor.load_plugins()

        for cmd_plugin in executor.command_plugins:
            cmd_table = PrettyTable()
            cmd_table.field_names = [get_cmd_type(cmd_plugin)]
            cmd_table.add_row([get_description(cmd_plugin)])
            cmd_table.add_row([get_examples(cmd_plugin)])
            cmd_table.align = "l"
            print(cmd_table)
            print(" ")


def get_cmd_type(cmd_plugin):
    try:
        return cmd_plugin.cmd_type
    except Exception as e:
        return "undefined"


def get_description(cmd_plugin):
    try:
        return cmd_plugin.description
    except Exception as e:
        return "undefined"


def get_examples(cmd_plugin):
    try:
        return cmd_plugin.examples
    except Exception as e:
        return "undefined"


def generate_empty_batch_file(arguments):
    logger = logging.getLogger(log.comEx_logger_name)

    path = cfg.DefaultPath.empty_batch
    if not os.path.exists(path):
        with open(path, "w+") as batch_file:
            logger.info(f"[ComEx] Empty batch configuration was generated in path '{path}'. "
                        f"Note that attribute '{cfg.Attribute.logger_cfg}' can be completely remove. "
                        f"Default logger will be used instead. ")
            json.dump(cfg.empty_batch(), batch_file, indent="    ")
    else:
        logger.warning(f"[ComEx] Target file '{path}' already exists.")

