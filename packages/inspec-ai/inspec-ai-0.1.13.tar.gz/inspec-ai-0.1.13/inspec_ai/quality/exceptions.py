class ConfigError(Exception):
    """Error raised when any of the provided configs for evaluation is wrong"""

    pass


class ConditionEvaluationError(Exception):
    """Error raised when an issue is encountered while evaluating a quality standard."""

    pass


class InternalEvaluationError(Exception):
    """Error raised when errors are met within a group evaluation."""

    def __init__(self, evaluation_result, *args):
        self.evaluation_result = evaluation_result
        self.error_message = args[0]

    def __str__(self):
        return self.error_message
