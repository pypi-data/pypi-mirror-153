from .base import GridElement
import logging
from midas.modules.powergrid.constraints.tap_changes import (
    ConstraintTapChanges,
)

LOG = logging.getLogger(__name__)
MAX_PERCENT = 150.0


class PPTransformer(GridElement):
    @staticmethod
    def pp_key() -> str:
        return "trafo"

    @staticmethod
    def res_pp_key() -> str:
        return "res_trafo"

    def __init__(self, index, grid, value):
        super().__init__(index, grid, LOG)
        self.max_percent = MAX_PERCENT
        self.tap_pos = 0
        self.add_constraint(ConstraintTapChanges(self, value))

    def step(self, time):
        old_state = self.tap_pos
        self._check(time)

        self.set_value("tap_pos", self.tap_pos)
        return old_state != self.tap_pos
