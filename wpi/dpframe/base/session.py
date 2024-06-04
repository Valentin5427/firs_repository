#coding=utf-8
import collections
import json
from PyQt5.QtCore import Qt
from dpframe.tech.AttrDict import AttrDict

class Session(object):

    # Нельзя менять структуру существующих ключей, можно только добавлять новые (на любом уровне)
    _default = {
        u'mainwnd': {
            u'state': Qt.WindowMaximized,
            u'x': 1,
            u'y': 1,
            u'width': 1,
            u'height': 1
        },
        u'refs':[],
        u'active_ref': None,
        u'splitter': {},
        u'dialog':{}
    }

    def __init__(self, config):
        print(43454667, config)
        self._file_name = config.session.file
        self._load()

    @staticmethod
    def _merge(dst_dict, src_dict):
        for k, v in src_dict.items():
            dst_dict[k] = dst_dict.get(k, v)
            if isinstance(dst_dict[k], collections.Mapping) and dst_dict[k] != v:
                Session._merge(dst_dict[k], v)

    def _load(self):
        self.storage = AttrDict()
        try:
            with open(self._file_name) as pf:
                self.storage = json.loads(pf.read(), object_pairs_hook=AttrDict)
        except IOError:
            pass
        except ValueError:
            pass
        self._merge(self.storage, self._default)
        AttrDict.toAttrDict(self.storage)

    def save(self):
        with open(self._file_name, 'w') as pf:
            pf.write(json.dumps(self.storage))

