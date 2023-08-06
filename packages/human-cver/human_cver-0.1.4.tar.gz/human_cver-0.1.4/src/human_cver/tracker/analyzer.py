import pickle
from typing import List
import os.path as osp
from .track_base import BaseTrackObj
from ..tools.logger import Logger


class TrackfileReader(object):
    def __init__(self, trackfile: str) -> None:
        assert osp.exists(trackfile)

        self.info_dict = dict()

        self.obj_list = []
        with open(trackfile, "rb") as fr:
            while True:
                try:
                    obj = pickle.load(fr)

                    name = obj._name
                    if name is not None:
                        if name not in self.info_dict:
                            self.info_dict[name] = []

                        self.info_dict[name].append(len(self.obj_list))
                        self.obj_list.append(obj)
                except EOFError:
                    break

    def get_obj(self, name: str, step: int) -> BaseTrackObj:
        if name in self.info_dict:
            k = self.info_dict[name][step]
            return self.obj_list[k]
        else:
            Logger.error(f"name={name} is bad")

    def get_length(self, name):
        return len(self.info_dict[name])

    def keys(self):
        return self.info_dict.keys()

def load_trackfile(trackfile) -> List[BaseTrackObj]:
    obj_list = []
    with open(trackfile, "rb") as fr:
        while True:
            try:
                obj = pickle.load(fr)
                obj_list.append(obj)
            except EOFError:
                break
    return obj_list


def analyzer(trackfile):
    obj_list = load_trackfile(trackfile)
    for obj in obj_list:
        obj.show()
