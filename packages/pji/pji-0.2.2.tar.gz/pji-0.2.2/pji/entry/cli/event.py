import io
import os
from typing import Callable, Mapping, Any

import click
from hbutils.scale import size_to_bytes_str

from ..event import _load_dispatch_getter as _load_abstract_dispatch_getter
from ..runner import DispatchRunner
from ...control import RunResult
from ...service import Dispatch, Command, FileInput, CopyFileInput, TagFileInput, LinkFileInput, \
    Section, SectionInfoMapping, FileOutput, CopyFileOutput, TagFileOutput


class DispatchEventRunner(DispatchRunner):
    def _section_start(self, section: Section):
        click.echo(click.style('Section {section} start ...'.format(
            section=repr(section.name)
        ), fg='blue'))

    def _section_complete(self, section: Section, result):
        _success, _results, _info = result
        _color = 'green' if _success else 'red'
        _result_str = 'completed' if _success else 'failed'

        click.echo(click.style('Section {section} execute {result}!'.format(
            section=repr(section.name),
            result=_result_str,
        ), fg=_color))
        click.echo('')

    def _input_start(self, input_: FileInput):
        if isinstance(input_, CopyFileInput):
            type_ = 'directory' if os.path.isdir(input_.file) else 'file'
            _sentence = "Coping {type} from {from_} to {to} ... ".format(type=type_, from_=repr(input_.file),
                                                                         to=repr(input_.local))

        elif isinstance(input_, TagFileInput):
            _sentence = "Loading tag {tag} to {to} ... ".format(tag=repr(input_.tag), to=repr(input_.local))
        elif isinstance(input_, LinkFileInput):
            type_ = 'directory' if os.path.isdir(input_.file) else 'file'
            _sentence = "Linking {type} from {from_} to {to} ... ".format(type=type_, from_=repr(input_.file),
                                                                          to=repr(input_.local))
        else:
            raise TypeError('Invalid file input object - {repr}.'.format(repr=repr(input_)))

        click.echo(click.style(_sentence, bold=False), nl=False)

    def _input_complete(self, input_: FileInput):
        click.echo(click.style('COMPLETE', fg='green'))

    def _input_skip(self, input_: FileInput):
        click.echo(click.style('SKIPPED', fg='yellow'))

    def _command_start(self, command: Command):
        click.echo(click.style(f"Running {repr(command.args)} ... ", bold=True), nl=False)

    def _command_complete(self, command: Command, result: RunResult):
        _color = 'green' if result.ok else 'red'
        with io.StringIO() as sio:
            print(result.status.name, file=sio, end='')
            ret = result.result
            if ret.exitcode or ret.signal:
                print(f'({ret.signal or ret.exitcode})', file=sio, end='')

            print(f', time: {ret.cpu_time:.3f}s / {ret.real_time:.3f}s', file=sio, end='')
            print(f', memory: {size_to_bytes_str(ret.max_memory)}', file=sio, end='')
            _title = sio.getvalue()

        click.echo(click.style(_title, fg=_color, bold=True), nl=True)

    def _output_start(self, output: FileOutput):
        if isinstance(output, CopyFileOutput):
            type_ = 'directory' if os.path.isdir(output.local) else 'file'
            _sentence = "Coping {type} from {from_} to {to} ... ".format(type=type_, from_=repr(output.local),
                                                                         to=repr(output.file))
        elif isinstance(output, TagFileOutput):
            type_ = 'directory' if os.path.isdir(output.local) else 'file'
            _sentence = "Saving {type} from {from_} to tag {tag} ... ".format(type=type_, tag=repr(output.tag),
                                                                              from_=repr(output.local))
        else:
            raise TypeError('Invalid file output object - {repr}.'.format(repr=repr(output)))

        click.echo(click.style(_sentence, bold=False), nl=False)

    def _output_complete(self, output: FileOutput):
        click.echo(click.style('COMPLETE', fg='green'))

    def _output_skip(self, output: FileOutput):
        click.echo(click.style('SKIPPED', fg='yellow'))

    def _info_mapping_start(self, mapping: SectionInfoMapping):
        click.echo(click.style('Collecting result information ... ', bold=False), nl=False)

    def _info_mapping_complete(self, mapping: SectionInfoMapping, result):
        click.echo(click.style('COMPLETE', fg='green'), nl=True)

    def _info_dump_start(self, section: Section, info: Mapping[str, Any]):
        click.echo(click.style('Dumping result information to {dump} ... '.format(
            dump=repr(section.info_dump)), bold=False), nl=False)

    def _info_dump_complete(self, section: Section, info: Mapping[str, Any]):
        click.echo(click.style('COMPLETE', fg='green'), nl=True)


def _load_dispatch_getter(filename: str = None) -> Callable[..., Dispatch]:
    return _load_abstract_dispatch_getter(DispatchEventRunner, filename)
