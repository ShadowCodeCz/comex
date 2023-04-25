import logging
import yapsy
import yapsy.IPlugin

from . import log


class ComExCommand(yapsy.IPlugin.IPlugin):
    cmd_type = ""
    description = ""
    examples = ""

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(log.comEx_logger_name)

    def execute(self, cmd_cfg, data):
        pass