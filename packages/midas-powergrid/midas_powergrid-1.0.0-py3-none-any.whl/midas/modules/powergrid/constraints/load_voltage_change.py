from .voltage_change import ConstraintVoltageChange


class ConstraintLoadVoltageChange(ConstraintVoltageChange):
    """Voltage change of a load is not allowed to rise over 2%."""

    def __init__(self, element, expected_value):
        super().__init__(element)

        self._expected_value = expected_value

    def handle_violation(self):
        # Overvoltages should be handles by generators
        if self._time_voltages[-1].value < 1.0:
            self._element.in_service = False

        self._element.current_bus_voltage = self._time_voltages[-1].value
