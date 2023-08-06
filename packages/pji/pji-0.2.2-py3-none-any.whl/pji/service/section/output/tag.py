import os
from abc import ABCMeta
from typing import Optional, Mapping, Callable, Union

from hbutils.model import get_repr_info
from hbutils.string import env_template

from .base import FileOutputTemplate, FileOutput, ResultCondition, OutputCondition, _DEFAULT_OUTPUT_CONDITION, \
    _DEFAULT_RESULT_CONDITION
from ...base import _check_workdir_file, _check_pool_tag, _process_environ
from ....utils import FilePool, wrap_empty


class _ITagFileOutput(metaclass=ABCMeta):
    def __init__(self, local: str, tag: str, condition: OutputCondition, on_: ResultCondition):
        """
        :param local: local path
        :param tag: pool tag
        """
        self.__local = local
        self.__tag = tag
        self.__condition = condition
        self.__on = on_

    def __repr__(self):
        """
        :return: representation string
        """
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('local', lambda: repr(self.__local)),
                ('tag', lambda: repr(self.__tag)),
                ('condition', lambda: self.__condition.name.lower()),
                ('on', lambda: self.__on.name.lower()),
            ]
        )


class TagFileOutputTemplate(FileOutputTemplate, _ITagFileOutput):
    def __init__(self, local: str, tag: str,
                 condition: Union[OutputCondition, str, None] = None,
                 on_: Union[ResultCondition, str, None] = None):
        """
        :param local: local path
        :param tag: pool tag
        """
        self.__local = local
        self.__tag = tag
        self.__condition = OutputCondition.loads(condition or _DEFAULT_OUTPUT_CONDITION)
        self.__on = ResultCondition.loads(on_ or _DEFAULT_RESULT_CONDITION)

        _ITagFileOutput.__init__(self, self.__local, self.__tag, self.__condition, self.__on)

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def local(self) -> str:
        return self.__local

    def __call__(self, workdir: str, pool: FilePool,
                 environ: Optional[Mapping[str, str]] = None, **kwargs) -> 'TagFileOutput':
        """
        get tag file input object
        :param workdir: local work directory
        :param pool: file pool object
        :param environ: environment variables
        :return: tag file input object
        """
        environ = _process_environ(environ)
        _tag = _check_pool_tag(env_template(self.__tag, environ))
        _local = os.path.normpath(
            os.path.abspath(os.path.join(workdir, _check_workdir_file(env_template(self.__local, environ)))))

        return TagFileOutput(pool, _local, _tag, self.__condition, self.__on)


class TagFileOutput(FileOutput, _ITagFileOutput):
    def __init__(self, pool: FilePool, local: str, tag: str, condition: OutputCondition, on_: ResultCondition):
        """
        :param pool: file pool
        :param local: local path
        :param tag: pool tag
        """
        self.__pool = pool
        self.__local = local
        self.__tag = tag
        self.__condition = condition
        self.__on = on_

        _ITagFileOutput.__init__(self, self.__local, self.__tag, self.__condition, self.__on)

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def local(self) -> str:
        return self.__local

    def __call__(self, *,
                 run_success: bool,
                 output_start: Optional[Callable[['TagFileOutput'], None]] = None,
                 output_complete: Optional[Callable[['TagFileOutput'], None]] = None,
                 output_skip: Optional[Callable[['TagFileOutput'], None]] = None, **kwargs):
        """
        execute this file output
        """
        if self.__on.need_run(run_success):
            wrap_empty(output_start)(self)
            if self.__condition == OutputCondition.OPTIONAL and \
                    (not os.path.exists(self.__local) or not os.access(self.__local, os.R_OK)):
                wrap_empty(output_skip)(self)
            else:
                self.__pool[self.__tag] = self.__local
                wrap_empty(output_complete)(self)
