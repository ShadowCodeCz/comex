import logging
import logging.config
import traceback

import generic_design_patterns as gdp

from . import log
from . import cfg


class EmptyCommand:
    def execute(self, cmd_config, data):
        pass


class ComEx:
    def __init__(self):
        self.cfg = None
        self.data = {}
        self.plugin_command_collector = None
        self.command_plugins = []
        self.command_index = {}

        self.logger = logging.getLogger(log.comEx_logger_name)

    def run(self, cfg, data=None, command_plugins=None):
        self.cfg = cfg
        self.init_logger()
        self.load_data_from_outside(data)
        self.load_plugins_from_outside(command_plugins)

        self.load_plugins()
        self.log_loaded_plugins()
        self.build_command_index()
        self.execute_commands()

    def load_data_from_outside(self, data):
        if data:
            self.data = data
            self.logger.debug(f"[ComEx] Loaded data from outside.")
        else:
            self.data = {}
            self.logger.debug(f"[ComEx] Loaded default data.")

    def load_plugins_from_outside(self, command_plugins):
        if command_plugins:
            self.command_plugins = command_plugins
            self.logger.debug(f"[ComEx] Loaded command plugins from outside.")
        else:
            self.command_plugins = []
            self.logger.debug(f"[ComEx] Loaded default command plugins.")

    def init_logger(self):
        try:
            logger_cfg = cfg.read_from_cfg(
                self.cfg,
                cfg.Attribute.logger_cfg,
                cfg.default_logger_configuration()
            )
            logging.config.dictConfig(logger_cfg)
            self.logger = logging.getLogger(log.comEx_logger_name)
        except Exception as e:
            self.logger.error(f"[ComEx] Configuration of logger failed. Exception({e})")
            self.logger.error(f"[ComEx] Traceback\n{traceback.format_exc()}")

    def build_command_index(self):
        for command in self.command_plugins:
            self.command_index[command.cmd_type] = command

    def load_plugins(self):
        # TODO: Plugin replace warning
        plugins_directories = cfg.read_from_cfg(self.cfg, cfg.Attribute.plugins_directories, [])
        plugins_regular_expression = cfg.read_from_cfg(self.cfg, cfg.Attribute.plugins_regular_expression, "")

        self.logger.debug(f"[ComEx] {cfg.Attribute.plugins_directories}={plugins_directories}")
        self.logger.debug(f"[ComEx] {cfg.Attribute.plugins_regular_expression}={plugins_regular_expression}")

        self.plugin_command_collector = gdp.plugin.YapsyRegExPluginCollector(
            plugins_directories,
            plugins_regular_expression
        )
        self.command_plugins = self.plugin_command_collector.collect()

    def log_loaded_plugins(self):
        try:
            cmds_type = "\n\t".join([plugin.cmd_type for plugin in self.command_plugins])
            self.logger.debug(f"[ComEx] {len(self.command_plugins)} plugins were loaded:\n\t{cmds_type}")
        except Exception as e:
            self.logger.error(f"[ComEx] Logging of loaded plugins failed. Exception({e})")
            self.logger.error(f"[ComEx] Traceback\n{traceback.format_exc()}")

    def find_command(self, cmd_cfg):
        try:
            return self.command_index[cmd_cfg[cfg.Attribute.cmd_type]]
        except Exception as e:
            self.logger.error(f"[ComEx] Finding command for configuration '{cmd_cfg}' by attribute '{cfg.Attribute.cmd_type}' failed. "
                              f"Command was replaced by EmptyCommand. Exception({e})")
            return EmptyCommand()

    def execute_commands(self):
        for cmd_cfg in cfg.read_from_cfg(self.cfg, cfg.Attribute.commands, []):
            cmd_type = cfg.read_from_cfg(cmd_cfg, cfg.Attribute.cmd_type, 'undefined.cmd.type')
            self.logger.debug(f"[ComEx] Command execution {cmd_type}")
            self.execute_command(cmd_cfg, cmd_type)

    def execute_command(self, cmd_cfg, cmd_type):
        try:
            cmd = self.find_command(cmd_cfg)
            cmd.execute(cmd_cfg, self.data)
        except Exception as e:
            self.logger.error(f"[ComEx] Execution of command '{cmd_type}' failed. Exception({e})")
            self.logger.error(f"[ComEx] Traceback\n{traceback.format_exc()}")
