from typing import List, Dict
from nonebot import on_command
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from LittlePaimon.utils import scheduler
from LittlePaimon.utils.message import CommandObjectID, CommandSwitch
from nonebot.log import logger
from LittlePaimon.database import GeneralSub

SCHEDULER_ID_PREFIX = 'groupNameCount'
KEY_PLACEMENT_STRING = '{n}'
HOUR = 0
MINUTE = 0

__plugin_meta__ = PluginMetadata(
    name='群名倒计时',
    description='群名倒计时',
    usage=f'群名倒计时 on [名称(天数位置放个{KEY_PLACEMENT_STRING})] [起始天数] /off',
    extra={
        'author': 'meatjam',
        'version': '1.0',
        'priority': 11,
    }
)

group_name_count = on_command('群名倒计时', priority=8, block=True, state={
    'pm_name': '群名倒计时',
    'pm_description': '群名倒计时',
    'pm_usage': f'群名倒计时 on [名称(天数位置放个{KEY_PLACEMENT_STRING})] [起始天数] /off',
    'pm_priority': 3
})


@group_name_count.handle()
async def _(bot: Bot, event: GroupMessageEvent, sub_id=CommandObjectID(), switch=CommandSwitch()):
    raw_msg = event.raw_message
    jod_id = f'{SCHEDULER_ID_PREFIX}{sub_id}'
    sub_data = {
        'sub_id': sub_id,
        'sub_type': event.message_type,
        'sub_event': '群名倒计时'
    }
    if switch:
        i = raw_msg.find('on')
        if i == -1:
            return
        options: List[str] = raw_msg[i + 2:].strip().split(' ')
        if len(options) != 2:
            return
        text, days = options
        placement_index = text.find(KEY_PLACEMENT_STRING)
        if placement_index == -1:
            return
        try:
            days = int(days)
        except Exception as e:
            return

        await GeneralSub.update_or_create(**sub_data,
            defaults={'sub_hour': HOUR,
                      'sub_minute': MINUTE})
        if scheduler.get_job(jod_id):
            scheduler.remove_job(jod_id)
        days = {'value': days}
        scheduler.add_job(
            func=change_group_name,
            trigger='cron',
            hour=HOUR,
            minute=MINUTE,
            id=jod_id,
            args=(sub_data['sub_id'], sub_data['sub_type'], jod_id, event.group_id, placement_index, text, days, bot),
            misfire_grace_time=10
        )
        logger.info('群名倒计时', '', {sub_data['sub_type']: sub_id, 'time': f'{HOUR}:{MINUTE}'}, '订阅成功', True)
        await bot.set_group_name(group_id=event.group_id,
            group_name=f'{text[:placement_index]}{days["value"]}{text[placement_index + len(KEY_PLACEMENT_STRING):]}')
        await group_name_count.finish(
            f'群名倒计时订阅成功， 将在每日{str(HOUR).rjust(2, "0")}:{str(MINUTE).rjust(2, "0")}修改群名'
        )
    else:
        if sub := await GeneralSub.get_or_none(**sub_data):
            await sub.delete()
            logger.info('群名倒计时', '', {sub_data['sub_type']: sub_id}, '取消订阅成功', True)
            await group_name_count.finish(f'群名倒计时订阅已取消')
        else:
            await group_name_count.finish(f'当前会话未开启群名倒计时订阅')


async def change_group_name(sub_id: int, sub_type: str, jod_id: str, group_id: int, placement_index: int, text: str, days: Dict[str, int], bot: Bot):
    try:
        days["value"] -= 1
        if days["value"] <= 0:
            if scheduler.get_job(jod_id):
                scheduler.remove_job(jod_id)
                await group_name_count.finish(f'群名倒计时已结束，订阅自动取消')
            return
        await bot.set_group_name(group_id=group_id,
            group_name=f'{text[:placement_index]}{days["value"]}{text[placement_index + len(KEY_PLACEMENT_STRING):]}')
        logger.info('群名倒计时', '', {sub_type: sub_id}, '修改成功', True)
    except Exception as e:
        logger.info('群名倒计时', '', {sub_type: sub_id}, f'修改失败: {e}', False)
