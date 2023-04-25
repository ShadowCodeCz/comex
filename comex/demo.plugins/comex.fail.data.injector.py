import logging
import yapsy.IPlugin


class FailDataInjector(yapsy.IPlugin.IPlugin):
    cmd_type = "fail.data.injector"

    def execute(self, cmd_cfg, data):
        logger = logging.getLogger("comex.logger")
        data_key = cmd_cfg["data.key"]
        data_value = cmd_cfg["data.value"]
        data[data_key] += data_value
        logger.debug(f"[{self.cmd_type}] Injecting '{data_key}'='{data_value}'")

