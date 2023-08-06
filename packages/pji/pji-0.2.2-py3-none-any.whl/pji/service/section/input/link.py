import os
from abc import ABCMeta
from typing import Optional, Mapping, Callable

from hbutils.model import get_repr_info
from hbutils.string import env_template

from .base import FileInput, FileInputTemplate, InputCondition, _DEFAULT_INPUT_CONDITION
from ...base import _check_workdir_file, _check_os_path, _process_environ
from ....utils import makedirs, wrap_empty


class _ILinkFileInput(metaclass=ABCMeta):
    def __init__(self, file: str, local: str, condition: InputCondition):
        """
        :param file: file path
        :param local: local path
        """
        self.__file = file
        self.__local = local
        self.__condition = condition

    def __repr__(self):
        """
        :return: representation string
        """
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('file', lambda: repr(self.__file)),
                ('local', lambda: repr(self.__local)),
                ('condition', lambda: self.__condition.name.lower()),
            ]
        )


class LinkFileInputTemplate(FileInputTemplate, _ILinkFileInput):
    def __init__(self, file: str, local: str, condition=None):
        """
        :param file: file path
        :param local: local path
        """
        self.__file = file
        self.__local = local
        self.__condition = InputCondition.loads(condition or _DEFAULT_INPUT_CONDITION)

        _ILinkFileInput.__init__(self, self.__file, self.__local, self.__condition)

    @property
    def file(self) -> str:
        return self.__file

    @property
    def local(self) -> str:
        return self.__local

    # noinspection DuplicatedCode
    def __call__(self, scriptdir: str, workdir: str,
                 environ: Optional[Mapping[str, str]] = None, **kwargs) -> 'LinkFileInput':
        """
        generate link file input object from extension information
        :param scriptdir: script directory
        :param workdir: work directory
        :param environ: environment variable
        :return: link file input object
        """
        environ = _process_environ(environ)
        _file = os.path.normpath(
            os.path.abspath(os.path.join(scriptdir, _check_os_path(env_template(self.__file, environ)))))
        _local = os.path.normpath(
            os.path.abspath(os.path.join(workdir, _check_workdir_file(env_template(self.__local, environ)))))

        return LinkFileInput(
            file=_file, local=_local, condition=self.__condition,
        )


class LinkFileInput(FileInput, _ILinkFileInput):
    def __init__(self, file: str, local: str, condition: InputCondition):
        """
        :param file: file path
        :param local: local path
        """
        self.__file = file
        self.__local = local
        self.__condition = condition

        _ILinkFileInput.__init__(self, self.__file, self.__local, self.__condition)

    @property
    def file(self) -> str:
        return self.__file

    @property
    def local(self) -> str:
        return self.__local

    def __call__(self, input_start: Optional[Callable[['LinkFileInput'], None]] = None,
                 input_complete: Optional[Callable[['LinkFileInput'], None]] = None,
                 input_skip: Optional[Callable[['LinkFileInput'], None]] = None, **kwargs):
        """
        execute this link event
        """
        wrap_empty(input_start)(self)
        if self.__condition == InputCondition.OPTIONAL and not os.path.exists(self.__file):
            wrap_empty(input_skip)(self)
        else:
            if not os.path.exists(self.__file):
                raise FileNotFoundError(self.__file)
            _parent_path, _ = os.path.split(self.__local)
            makedirs(_parent_path)
            os.symlink(self.__file, self.__local, target_is_directory=os.path.isdir(self.__file))
            wrap_empty(input_complete)(self)
