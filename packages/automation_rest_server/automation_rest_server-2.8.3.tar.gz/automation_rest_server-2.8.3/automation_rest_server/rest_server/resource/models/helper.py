# coding=utf-8
# pylint: disable=invalid-name
import threading
import ctypes
import inspect
from flask_restful import fields


resource_fields = {
    'data': fields.List(fields.String, default=None),
    'msg': fields.String,
    'state': fields.Integer
}


class MyThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, daemon=None):
        super(MyThread, self).__init__()
        self.args = args
        self.target = target
        self.result = None
        self._stop_event = threading.Event()

    def run(self):
        self.result = self.target(*self.args)
        print("MyThread result:", self.result)

    def get_result(self):
        try:
            return list(self.result)
        except BaseException:
            return None

    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        # if res == 0:
        #     raise ValueError("invalid thread id")
        if res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop(self):
        # self._stop_event.set()
        self._async_raise(self.ident, SystemExit)

    def stopped(self):
        return self._stop_event.is_set()
