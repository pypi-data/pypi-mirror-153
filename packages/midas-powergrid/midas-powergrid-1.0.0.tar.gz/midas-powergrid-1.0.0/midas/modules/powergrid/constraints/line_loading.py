from .base import Constraint


class ConstraintLineLoading(Constraint):
    def __init__(self, element):
        super().__init__(element)

    def check(self, time) -> bool:
        self._statisfied = True

        loading = self._element.grid.res_line.loading_percent.loc[
            self._element.index
        ]
        if loading > self._element.max_percentage:
            self._statisfied = False

        return self._statisfied

    def handle_violation(self):
        self._element.in_service = False
