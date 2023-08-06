import io
import os
import signal
import time
from abc import ABCMeta
from multiprocessing import Event, Value, Lock
from multiprocessing.synchronize import Event as _EventType
from queue import Empty, Queue
from threading import Thread
from typing import Tuple, Callable, Optional, BinaryIO

from ..model import ProcessResult, ResourceLimit, RunResult, RunResultStatus
from ...utils import ValueProxy


class GeneralProcess(metaclass=ABCMeta):
    def __init__(self, start_time: float, resources: ResourceLimit,
                 process_result_func: Callable[[], Optional[ProcessResult]],
                 lifetime_event: _EventType, lock: Optional[Lock] = None):
        self.__start_time = start_time
        self.__resources = resources
        self.__process_result = None
        self.__process_result_func = process_result_func
        self.__result = None
        self.__lifetime_event = lifetime_event
        self.__lock = lock or Lock()

    def __get_process_result(self) -> ProcessResult:
        if self.__process_result is None:
            self.__process_result = self.__process_result_func()
        return self.__process_result

    def __get_result(self) -> RunResult:
        if self.__result is None or self.__result.result is None:
            self.__result = RunResult(self.__resources, self.__get_process_result())
        return self.__result

    def _wait_for_end(self):
        self.__lifetime_event.wait()

    @property
    def start_time(self) -> float:
        with self.__lock:
            return self.__start_time

    @property
    def resources(self) -> ResourceLimit:
        with self.__lock:
            return self.__resources

    @property
    def result(self) -> RunResult:
        with self.__lock:
            return self.__get_result()

    @property
    def ok(self) -> bool:
        with self.__lock:
            return self.__get_result().ok

    @property
    def completed(self) -> bool:
        with self.__lock:
            return self.__get_result().completed

    @property
    def status(self) -> RunResultStatus:
        with self.__lock:
            return self.__get_result().status

    def join(self):
        with self.__lock:
            self._wait_for_end()


BYTES_LINESEQ = bytes(os.linesep, 'utf8')


def read_from_stream(stream: BinaryIO, process_complete: _EventType) -> bytes:
    with io.BytesIO() as bio:
        for line in stream:
            bio.write(line)

        return bio.getvalue()


def load_lines_from_stream(stream: BinaryIO, stream_ready: _EventType, process_complete: _EventType,
                           queue: Queue, trans=None):
    _processing_queue = Queue()
    _load_complete = Event()
    trans = trans or (lambda x: x)

    def _output_load_func():
        stream_ready.set()
        for line in stream:
            _processing_queue.put((time.time(), line))

        _load_complete.set()

    def _item_process_func():
        while not _processing_queue.empty() or not _load_complete.is_set():
            try:
                item = _processing_queue.get(timeout=0.2)
            except Empty:
                continue
            else:
                queue.put(trans(item))

    _output_load_thread = Thread(target=_output_load_func)
    _item_process_func = Thread(target=_item_process_func)

    _output_load_thread.start()
    _item_process_func.start()

    _output_load_thread.join()
    _item_process_func.join()


def measure_thread(start_time_ok: Event, start_time: Value, child_pid: int) \
        -> Tuple[Thread, _EventType, _EventType, _EventType, ValueProxy]:
    _process_result = ValueProxy()
    _process_complete = Event()
    _measure_initialized = Event()
    _measure_complete = Event()

    def _thread_func():
        _measure_initialized.set()
        _, status, resource_usage = os.wait4(child_pid, os.WSTOPPED)
        _process_complete.set()
        start_time_ok.wait()
        _process_result.value = ProcessResult(status, start_time.value, time.time(), resource_usage)
        _measure_complete.set()

    return Thread(target=_thread_func), _measure_initialized, _process_complete, _measure_complete, _process_result


def killer_thread(start_time_ok: Event, start_time: Value, child_pid: int,
                  real_time_limit: float, process_complete: Event) -> Tuple[Thread, _EventType]:
    _killer_initialized = Event()

    def _thread_func():
        _killer_initialized.set()
        if real_time_limit is not None:
            start_time_ok.wait()
            target_time = start_time.value + real_time_limit
            while time.time() < target_time and not process_complete.is_set():
                time.sleep(min(max(target_time - time.time(), 0.0), 0.2))
            if not process_complete.is_set():
                os.killpg(os.getpgid(child_pid), signal.SIGKILL)
                process_complete.wait()

    return Thread(target=_thread_func), _killer_initialized
