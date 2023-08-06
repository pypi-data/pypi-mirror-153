import importlib
import os

from . import global_setting


class DynamicSetting:

    def initialize(self):

        settings_path = os.environ.get('WINTERSWEET_SETTINGS_MODULE', 'wintersweet.framework.global_setting')

        self.__dict__['_settings'] = _Setting(settings_path)

    def __getattr__(self, item):

        if self.__dict__.get('_settings') is None:
            self.initialize()

        if hasattr(self._settings, item):
            val = getattr(self._settings, item)
            self.__dict__[item] = val
        else:
            val = None
        return val

    def __setattr__(self, key, value):
        if key == '_settings':
            self.__dict__.clear()
        else:
            if self.__dict__.get('_settings') is None:
                self.initialize()

            setattr(self._settings, key, value)
            self.__dict__[key] = value


class _Setting:

    def __init__(self, module_or_path):

        for item in dir(global_setting):
            if item.isupper():
                setattr(self, item, getattr(global_setting, item))

        if isinstance(module_or_path, str):
            mod = importlib.import_module(module_or_path)
        else:
            mod = module_or_path
        for item in dir(mod):
            if not item.startswith('_') and item.isupper():
                setattr(self, item, getattr(mod, item))


settings = DynamicSetting()

