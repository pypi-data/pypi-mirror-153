__version__ = "0.1.0"
from nonebot import require, on_command, get_bot
from .data_source import R3nzSkin
from nonebot.adapters.onebot.v12 import Bot, Event

scheduler = require("nonebot_plugin_apscheduler").scheduler
GetLatest = on_command("skin")


@scheduler.add_job("interval", hours=1)
async def _():
    result = await R3nzSkin.skinGetLatest()

    if not R3nzSkin.isUpdate(result["tag_name"]):
        return

    try:
        bot = get_bot()
        bot.call_api(
            "send_group_msg", group_id="975663303", message=R3nzSkin.toMessage(result)
        )
    except:
        return
    else:
        R3nzSkin.writeVersion(result["tag_name"])


@GetLatest.handle()
async def _(bot: Bot, event: Event):
    result = await R3nzSkin.skinGetLatest()
    message = R3nzSkin.toMessage(result)
    await GetLatest.finish(message)
