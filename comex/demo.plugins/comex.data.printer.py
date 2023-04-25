import logging
import yapsy.IPlugin
import json

class DataPrinter(yapsy.IPlugin.IPlugin):
    cmd_type = "data.printer"

    def execute(self, cmd_cfg, data):
        logger = logging.getLogger("comex.logger")
        logger.debug(f"[{self.cmd_type}] {data}")
