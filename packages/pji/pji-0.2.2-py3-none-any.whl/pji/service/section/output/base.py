from abc import ABCMeta, abstractmethod
from enum import unique, IntEnum

from hbutils.model import int_enum_loads


class FileOutputTemplate(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, *args, **kwargs) -> 'FileOutput':
        raise NotImplementedError  # pragma: no cover


class FileOutput(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, **kwargs):
        raise NotImplementedError  # pragma: no cover


@int_enum_loads(name_preprocess=str.upper)
@unique
class OutputCondition(IntEnum):
    OPTIONAL = 1
    REQUIRED = 2


_DEFAULT_OUTPUT_CONDITION = OutputCondition.REQUIRED


@int_enum_loads(name_preprocess=str.upper)
@unique
class ResultCondition(IntEnum):
    SUCCESS = 1
    FAIL = 2
    ALL = 3

    def need_run(self, success: bool):
        if self == self.SUCCESS:
            return success
        elif self == self.FAIL:
            return not success
        elif self == self.ALL:
            return True
        else:
            raise ValueError(f'Unknown result condition - {self}.')  # pragma: no cover


_DEFAULT_RESULT_CONDITION = ResultCondition.SUCCESS
