import json
from inspec_ai.utils.utils import _StrEnum


class Metric(_StrEnum):
    MAE = "mae"
    MASE = "mase"
    MAPE = "mape"
    AUC = "auc"
    F1 = "f1"
    PRECISION = "precision"
    RECALL = "recall"
    ACCURACY = "accuracy"


class Condition(_StrEnum):
    LOWER = "lt"
    GREATER = "gt"
    LOWER_EQUALS = "lte"
    GREATER_EQUALS = "gte"
    EQUALS = "eq"

    def convert_to_plain_english(self):
        condition_to_plain_english_dict = {
            Condition.LOWER.value: "lower than",
            Condition.GREATER.value: "greater than",
            Condition.LOWER_EQUALS.value: "lower or equal to",
            Condition.GREATER_EQUALS.value: "greater or equal to",
            Condition.EQUALS.value: "equal to",
        }
        return condition_to_plain_english_dict[self.value]


class Status(_StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"


class EvaluationMode(_StrEnum):
    GLOBAL = "global"
    FOR_SINGLE_DIM_VALUE = "for single dim value"
    FOR_EACH_UNIQUE_DIM_VALUE = "for each unique dim value"
    FOR_EACH_DIM_VALUE_IN_LIST = "for each dim value in list"


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, _StrEnum):
            return str(obj)
        else:
            return super(JsonEncoder, self).default(obj)
