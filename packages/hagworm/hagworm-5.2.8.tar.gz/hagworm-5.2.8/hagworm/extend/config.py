# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import dataclasses

from configparser import RawConfigParser

from .base import Utils
from .event import EventDispatcher


class HostType(str):

    @classmethod
    def decode(cls, val):

        if not val:
            return None

        host, port = val.split(r':', 2)
        return host.strip(), int(port.strip())


class JsonType(str):

    @classmethod
    def decode(cls, val):

        if not val:
            return None

        return Utils.json_decode(val)


class StrListType(str):

    @classmethod
    def decode(cls, val):
        return Utils.split_str(val)


class IntListType(str):

    @classmethod
    def decode(cls, val):
        return Utils.split_int(val)


class FloatListType(str):

    @classmethod
    def decode(cls, val):
        return Utils.split_float(val)


class Field:

    __slots__ = [r'section']

    def __init__(self, section):

        self.section = section


class ConfigureMetaclass(type):
    """配置类元类，增加dataclass修饰
    """

    def __new__(mcs, name, bases, attrs):
        return dataclasses.dataclass(init=False)(
            type.__new__(mcs, name, bases, attrs)
        )


class ConfigureBase(metaclass=ConfigureMetaclass):
    """配置类
    """

    __slots__ = [r'_event_dispatcher']

    def __init__(self):

        super().__init__()

        self._event_dispatcher = EventDispatcher()

    def __setattr__(self, key, value):

        super().__setattr__(key, value)

        if key in self.__dataclass_fields__:
            self._event_dispatcher.dispatch(key, value)

    def add_listener(self, key, _callable):
        return self._event_dispatcher.add_listener(key, _callable)

    def remove_listener(self, key, _callable):
        return self._event_dispatcher.remove_listener(key, _callable)


class Configure(ConfigureBase):
    """配置类
    """

    __slots__ = [r'_parser']

    def __init__(self):

        super().__init__()

        self._parser = RawConfigParser()

    def _init_options(self):

        for _key, _field in self.__dataclass_fields__.items():

            _type = _field.type
            _section = _field.default.section

            if _type is str:
                self.__setattr__(_key, self._parser.get(_section, _key))
            elif _type is int:
                self.__setattr__(_key, self._parser.getint(_section, _key))
            elif _type is float:
                self.__setattr__(_key, self._parser.getfloat(_section, _key))
            elif _type is bool:
                self.__setattr__(_key, self._parser.getboolean(_section, _key))
            else:
                self.__setattr__(_key, _type.decode(self._parser.get(_section, _key)))

    def get_option(self, section, option):

        return self._parser.get(section, option)

    def get_options(self, section):

        parser = self._parser

        options = {}

        for option in parser.options(section):
            options[option] = parser.get(section, option)

        return options

    def set_options(self, section, **options):

        if not self._parser.has_section(section):
            self._parser.add_section(section)

        for option, value in options.items():
            self._parser.set(section, option, value)

        self._init_options()

    def read(self, files):

        self._parser.clear()
        self._parser.read(files, r'utf-8')

        self._init_options()

    def read_str(self, val):

        self._parser.clear()
        self._parser.read_string(val)

        self._init_options()

    def read_dict(self, val):

        self._parser.clear()
        self._parser.read_dict(val)

        self._init_options()
