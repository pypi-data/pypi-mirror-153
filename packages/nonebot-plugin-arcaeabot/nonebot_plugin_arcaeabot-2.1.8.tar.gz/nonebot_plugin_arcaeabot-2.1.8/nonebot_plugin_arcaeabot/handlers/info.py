from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from ..matcher import arc
from ..data import UserInfo, ArcInfo


async def info_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] == "info":
        user_info = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)
        # Exception
        if not user_info:
            await arc.finish(MessageSegment.reply(event.message_id) + "你还没绑定呢！")

        arc_info = ArcInfo.get_or_none(ArcInfo.arcaea_id == user_info.arcaea_id)

        await arc.finish(
            MessageSegment.reply(event.message_id)
            + f"id: {user_info.arcaea_id}, 用户名: {arc_info.arcaea_name}。"
        )
