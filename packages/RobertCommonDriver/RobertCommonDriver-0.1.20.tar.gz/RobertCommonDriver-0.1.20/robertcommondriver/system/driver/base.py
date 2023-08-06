from typing import Dict, Any, Callable
from abc import abstractmethod
from datetime import datetime
from threading import Timer, Thread


class BaseCommon():

    class RepeatingTimer(Timer):

        def run(self):
            self.finished.wait(self.interval)
            while not self.finished.is_set():
                self.function(*self.args, **self.kwargs)
                self.finished.wait(self.interval)

    class SimpleTimer():

        def __init__(self):
            self.timer = None

        def is_running(self):
            return self.timer and self.timer.is_alive()

        def run(self, interval: int, function: Callable, args=None, kwargs=None):
            if self.is_running():
                if kwargs.get('force', False) is False:
                    raise Exception(f"timer is running, please cancel")
                else:
                    self.cancel()
            self._run_timer(interval, function, args, kwargs)

        def _run_timer(self, interval: int, function: Callable, args=None, kwargs=None):
            self.timer = Timer(interval, function, args, kwargs)
            self.timer.start()

        def cancel(self):
            if self.is_running():
                self.timer.cancel()
            self.timer = None

    @staticmethod
    def function_thread(fn: Callable, daemon: bool, *args, **kwargs):
        return Thread(target=fn, args=args, kwargs=kwargs, daemon=daemon)


# Point base class
class BasePoint(object):

    def __init__(self, point_source: str, point_writable: bool, point_name: str, point_description: str = '', point_sample_value: Any = None):
        self.point_writable = point_writable
        self.point_source = point_source
        self.point_name = point_name
        self.point_description = point_description
        self.point_sample_value = point_sample_value
        self.point_value = None

    # get point_source
    @property
    def get_point_source(self):
        return self.point_source

    # get point_description
    @property
    def get_point_description(self):
        return self.point_description

    # get point_name
    @property
    def get_point_name(self):
        return self.point_name

    # get point_writable
    @property
    def get_point_writable(self):
        return self.point_writable


PointTableDict = Dict[str, Dict[str, Any]]


class BaseDriver(object):

    def __init__(self, dict_config: dict, dict_point: PointTableDict):
        self.dict_config = dict_config
        self.dict_point = dict_point
        self.callbacks = {}

    def __del__(self):
        self.exit()

    def exit(self):
        pass

    @abstractmethod
    def get_points(self, dict_point: dict = {}) -> tuple:
        pass

    def set_points(self, dict_points: dict) -> dict:
        pass

    def reset_config(self, dict_config: dict):
        self.dict_config = dict_config

    def reset_point(self, dict_point: dict):
        self.dict_point = dict_point

    def ping_target(self):
        return True

    @abstractmethod
    def configure(self):
        pass

    def search_points(self) -> dict:
        return {}

    def enable_logging(self, callback: Callable = None):
        self.callbacks['debug_log'] = callback

    def set_call_result(self, call_method: str, **kwargs):
        if isinstance(self.callbacks, dict):
            call_method = self.callbacks.get(call_method)
            if isinstance(call_method, Callable):
                call_method(**kwargs)