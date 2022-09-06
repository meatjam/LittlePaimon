from typing import Optional, List

from pydantic import BaseModel, Field


class MatcherInfo(BaseModel):
    pm_name: str
    """命令名称"""
    pm_description: Optional[str]
    """命令描述"""
    pm_usage: Optional[str]
    """命令用法"""
    pm_priority: int = 99
    """命令优先级"""
    pm_show: bool = True
    """是否展示"""


class PluginInfo(BaseModel):
    name: str
    """插件名称"""
    module_name: str
    """插件模块名称"""
    description: Optional[str]
    """插件描述"""
    usage: Optional[str]
    """插件用法"""
    status: Optional[bool]
    """插件状态（无用项）"""
    show: bool = True
    """是否展示"""
    priority: int = 99
    """展示优先级"""
    matchers: Optional[List[MatcherInfo]] = []
    """命令列表"""


class Config(BaseModel):
    CookieWeb_enable: bool = Field(True, alias='启用CookieWeb')
    CookieWeb_url: str = Field('http://127.0.0.1:13579/LittlePaimon/cookie', alias='CookieWeb地址')

    sim_gacha_cd_group: int = Field(30, alias='模拟抽卡群冷却')
    sim_gacha_cd_member: int = Field(60, alias='模拟抽卡群员冷却')
    sim_gacha_max: int = Field(5, alias='模拟抽卡单次最多十连数')

    auto_myb_enable: bool = Field(True, alias='米游币自动获取开关')
    auto_myb_hour: int = Field(8, alias='米游币开始执行时间(小时)')
    auto_myb_minute: int = Field(0, alias='米游币开始执行时间(分钟)')

    auto_sign_enable: bool = Field(True, alias='米游社自动签到开关')
    auto_sign_hour: int = Field(0, alias='米游社签到开始时间(小时)')
    auto_sign_minute: int = Field(5, alias='米游社签到开始时间(分钟)')

    ssbq_enable: bool = Field(True, alias='实时便签检查开关')
    ssbq_begin: int = Field(0, alias='实时便签停止检查开始时间')
    ssbq_end: int = Field(6, alias='实时便签停止检查结束时间')
    ssbq_check: int = Field(16, alias='实时便签检查间隔')

    AI_voice_cooldown: int = Field(10, alias='原神语音合成冷却')

    ys_auto_update: int = Field(24, alias='ys自动更新小时')
    ysa_auto_update: int = Field(24, alias='ysa自动更新小时')
    ysd_auto_update: int = Field(6, alias='ysd自动更新小时')

    cloud_genshin_enable: bool = Field(True, alias='云原神自动签到开关')
    cloud_genshin_hour: int = Field(7, alias='云原神签到时间(小时)')

    request_event: bool = Field(True, alias='启用好友和群请求通知')
    auto_add_friend: bool = Field(False, alias='自动接受好友请求')
    auto_add_group: bool = Field(False, alias='自动接受群邀请')
    notice_event: bool = Field(True, alias='启用好友和群欢迎消息')
