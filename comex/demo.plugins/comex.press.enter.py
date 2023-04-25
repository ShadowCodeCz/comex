import logging
import comex
import yapsy.IPlugin


class Press(comex.plugin.ComExCommand):
    cmd_type = "press.enter"
    description = ""
    examples = """
            {
                "cmd.type": "press.enter"
            },
    """

    def execute(self, cmd_cfg, data):
        self.logger.debug(f"[{self.cmd_type}] Waiting ...")
        input("Press Enter to continue...")

