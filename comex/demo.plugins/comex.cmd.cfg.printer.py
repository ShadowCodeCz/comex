import logging
import yapsy.IPlugin


class CmdCfgPrinter(yapsy.IPlugin.IPlugin):
    cmd_type = "cmd.cfg.printer"

    def execute(self, cmd_cfg, data):
        logger = logging.getLogger("comex.logger")
        logger.debug(f"[{self.cmd_type}] {cmd_cfg}")

