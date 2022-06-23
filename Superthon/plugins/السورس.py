from telethon import Button, events

from Superthon import Superthon
from . import *
from ..Config import Config

ROZ_PIC = "https://telegra.ph/file/10482dc7e71323552d4e7.jpg"
RAZAN = Config.TG_BOT_USERNAME
ROZ_T = (
    f"** سورس سوبرثون يعمل بنجاح **\n"
    f"**   - اصدار التليثون :** `1.23.0\n`"
    f"**   - اصدار سوبرثون :** `4.0.0`\n"
    f"**   - البوت المستخدم :** `{RAZAN}`\n"
    f"**   - اصدار البايثون :** `3.9.6\n`"
    f"**   - المستخدم :** {mention}\n"
)

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        await bot.get_me()
        if query.startswith("السورس") and event.query.user_id == bot.uid:
            buttons = [
                [
                    Button.url("↯︙قناة السورس", "https://t.me/Superthon"),
                    Button.url("↯︙مطور السورس", "https://t.me/KaaJBot"),
                ]
            ]
            if ROZ_PIC and ROZ_PIC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(
                    ROZ_PIC, text=ROZ_T, buttons=buttons, link_preview=False
                )
            elif ROZ_PIC:
                result = builder.document(
                    ROZ_PIC,
                    title="Superthon - Superthon",
                    text=ROZ_T,
                    buttons=buttons,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    title="Superthon - Superthon",
                    text=ROZ_T,
                    buttons=buttons,
                    link_preview=False,
                )
            await event.answer([result] if result else None)


@Superthon.ar_cmd(pattern="السورس")
async def repo(event):
    RR7PP = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(Super_thon, "السورس")
    await response[0].click(event.chat_id)
    await event.delete()


# edit by ~ @Superthon
