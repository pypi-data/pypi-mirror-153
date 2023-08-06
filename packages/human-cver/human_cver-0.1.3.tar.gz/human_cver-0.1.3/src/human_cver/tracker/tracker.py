import os
import os.path as osp
import pickle
import time
from typing import Union

import numpy as np

from ..tools.logger import Logger
from .track_base import BaseTrackObj
from .track_image import ImageTrackObj
from .track_number import NumberTrackObj
from .track_numpy import NumpyTrackObj


class Tracker(object):

    __filename = ""
    __start_time = None
    __is_open = False

    @staticmethod
    def trackfile(
        filename: str,
        open=True,
        clear=True,
    ) -> None:
        """设置track文件 *.pkl"""

        Tracker.__filename = filename
        Tracker.__start_time = time.time()

        path = osp.dirname(osp.abspath(filename))
        if not osp.exists(path):
            os.makedirs(path, exist_ok=True)

        Logger.warn(f"trackfile: {filename}")

        if clear and osp.exists(filename):
            os.remove(filename)

        if open:
            Tracker.open()

    @staticmethod
    def open() -> None:
        """开启记录功能"""
        Tracker.__is_open = True
        Logger.info("Tracker is opened!")

    @staticmethod
    def close() -> None:
        """关闭记录功能"""
        Tracker.__is_open = False
        Logger.info("Tracker is closed!")

    @staticmethod
    def is_open() -> bool:
        return Tracker.__is_open

    @staticmethod
    def track_obj(obj: BaseTrackObj, step=None) -> None:
        if not Tracker.is_open():
            return
        if not Tracker._check_file():
            return

        # 自动记录时间信息
        t = time.time()
        obj._time = t - Tracker.__start_time
        obj._abs_time = t
        obj._step = step
        with open(Tracker.__filename, "ab") as fw:
            pickle.dump(obj, fw)

    def track_img(img: np.ndarray, name: str = None, step: int = None) -> None:
        if Tracker.is_open():
            Tracker.track_obj(ImageTrackObj(img, name=name), step)

    def track_number(
        data: Union[float, int], name: str = None, step: int = None
    ) -> None:
        if Tracker.is_open():
            Tracker.track_obj(NumberTrackObj(data, name=name), step)

    def track_numpy(data: np.ndarray, name: str = None, step: int = None) -> None:
        if Tracker.is_open():
            Tracker.track_obj(NumpyTrackObj(data, name=name), step)

    @staticmethod
    def _check_file():
        if not Tracker.__filename:
            Logger.error("trackfile first!")
            return False
        return True
