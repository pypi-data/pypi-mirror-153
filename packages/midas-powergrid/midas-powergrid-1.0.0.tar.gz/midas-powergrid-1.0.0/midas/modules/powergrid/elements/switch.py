from .base import GridElement
import logging


LOG = logging.getLogger(__name__)


class PPSwitch(GridElement):
    @staticmethod
    def pp_key() -> str:
        return "switch"

    @staticmethod
    def res_pp_key() -> str:
        return "res_switch"

    def __init__(self, index, grid, value):
        super().__init__(index, grid, LOG)
        self.closed = True

    def step(self, time):
        old_state = self.closed
        self.closed = True
        self._check(time)

        self.set_value("closed", self.closed)

        return old_state != self.closed
