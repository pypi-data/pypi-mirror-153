from enum import Enum


class _StrEnum(str, Enum):
    def __str__(self):
        return str(self.value)
