import os
import json
import pandas as pd


class FileType(object):
    def __init__(self, path: str, encoding: str = 'utf-8'):
        self.path = path
        self.encoding = encoding

    def exists(self):
        return os.path.exists(self.path)

    def get(self, **kwargs):
        return None

    def load(self, **kwargs):
        return self.get(**kwargs) if self.exists() else None


class Json(FileType):
    def get(self, **kwargs):
        return pd.DataFrame(json.load(open(self.path, mode='r', encoding=self.encoding)))


class Csv(FileType):
    def get(self, **kwargs):
        return pd.read_csv(self.path, encoding=self.encoding)


class Xlsx(FileType):
    def get(self, sheet_name='Sheet1'):
        return pd.read_excel(self.path, sheet_name=sheet_name)


class Xls(FileType):
    def get(self, **kwargs):
        sheet_name = kwargs.get('sheet_name')
        return pd.read_excel(self.path, sheet_name=sheet_name, engine='xlrd')


class FileTableLoader(object):
    def __init__(self, path: str, encoding: str = 'utf-8'):
        self._path = path
        self._encoding = encoding

    def json(self):
        _ins = Json(path=self._path, encoding=self._encoding)
        _out = _ins.load()
        del _ins
        return _out

    def csv(self):
        _ins = Csv(path=self._path, encoding=self._encoding)
        _out = _ins.load()
        del _ins
        return _out

    def xlsx(self, sheet_name='Sheet1'):
        _ins = Xlsx(path=self._path, encoding=self._encoding)
        _out = _ins.load(sheet_name=sheet_name)
        del _ins
        return _out

    def xls(self, sheet_name='Sheet1'):
        _ins = Xls(path=self._path, encoding=self._encoding)
        _out = _ins.load(sheet_name=sheet_name)
        del _ins
        return _out

    def load(self) -> pd.DataFrame:
        file_type = self._path.split('.')[-1]
        return eval(f'self.{file_type}()')

    @property
    def data(self) -> pd.DataFrame:
        return self.load()
