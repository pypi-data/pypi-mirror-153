from abc import ABC, abstractmethod


class Constraint(ABC):
    def __init__(self, element):
        self._element = element
        self._expected_value = None
        self._violated_value = None

        self._satisfied = True

    def set_violation_values(self, expected_value, violated_value):
        self._violated_value = violated_value
        self._expected_value = expected_value

    @abstractmethod
    def check(self, time) -> bool:
        pass

    @abstractmethod
    def handle_violation(self):
        pass
