from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class SettingUnit:
    """ 基础设置单元 """
    name: str
    description: str
    pass


@dataclass(frozen=True)
class SettingCallbackUnit(SettingUnit):
    """ 回调设置单元 """
    type: str
    get_attr: Callable[[], str]
    set_attr: Callable[[str], None]
    pass


@dataclass(frozen=True)
class SettingTextUnit(SettingCallbackUnit):
    """ 文本设置单元 """
    regex: str = '.*'
    pass


@dataclass(frozen=True)
class SettingTextUnitTypes:
    """ 文本设置单元类型集 """
    INT: str = 'int'
    FLOAT: str = 'float'
    TEXT: str = 'text'
    pass


SettingTextUnitTypes = SettingTextUnitTypes()
""" 文本设置单元类型集 """


@dataclass(frozen=True)
class SettingOptionUnit(SettingCallbackUnit):
    """ 选项设置单元 """
    del_attr: Callable[[str], None] | None
    options: list[str]
    selected_indexes: list[int] | None
    pass


@dataclass(frozen=True)
class SettingOptionUnitTypes:
    """ 选项设置单元类型集 """
    COMBO: str = 'combo'
    SINGLE: str = 'single'
    MULTIPLE: str = 'multiple'
    pass


SettingOptionUnitTypes = SettingOptionUnitTypes()
""" 选项设置单元类型集 """


@dataclass(frozen=True)
class SettingGroupUnit(SettingUnit):
    """ 组设置单元 """
    units: list[SettingTextUnit | SettingOptionUnit]
    pass
