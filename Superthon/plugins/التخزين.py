import asyncio

from Superthon import Superthon
from Superthon.core.logger import logging

from ..Config import Config
from ..core.managers import edit_delete
from ..helpers.tools import media_type
from ..helpers.utils import _format
from ..sql_helper import no_log_pms_sql
from ..sql_helper.globals import addgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)


class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0


LOG_CHATS_ = LOG_CHATS()


@Superthon.ar_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def monito_p_m_s(event):  # sourcery no-metrics
    if Config.PM_LOGGER_GROUP_ID == -100:
        return
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        return
    sender = await event.get_sender()
    if not sender.bot:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id) and chat.id != 777000:
            if LOG_CHATS_.RECENT_USER != chat.id:
                LOG_CHATS_.RECENT_USER = chat.id
                if LOG_CHATS_.NEWPM:
                    if LOG_CHATS_.COUNT > 1:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                " رسالة جديده", f"{LOG_CHATS_.COUNT} رسائل"
                            )
                        )
                    else:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                " رسالة جديده", f"{LOG_CHATS_.COUNT} رسائل"
                            )
                        )
                    LOG_CHATS_.COUNT = 0
                LOG_CHATS_.NEWPM = await event.client.send_message(
                    Config.PM_LOGGER_GROUP_ID,
                    f"{_format.mentionuser(sender.first_name , sender.id)} قام بأرسال رسالة جديده \nالايدي : `{chat.id}`",
                )
            try:
                if event.message:
                    await event.client.forward_messages(
                        Config.PM_LOGGER_GROUP_ID, event.message, silent=True
                    )
                LOG_CHATS_.COUNT += 1
            except Exception as e:
                LOGS.warn(str(e))


@Superthon.ar_cmd(incoming=True, func=lambda e: e.mentioned, edited=False, forword=None)
async def log_tagged_messages(event):
    hmm = await event.get_chat()
    from .afk import AFK_

    if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") == "false":
        return
    if (
        (no_log_pms_sql.is_approved(hmm.id))
        or (Config.PM_LOGGER_GROUP_ID == -100)
        or ("on" in AFK_.USERAFK_ON)
        or (await event.get_sender() and (await event.get_sender()).bot)
    ):
        return
    full = None
    try:
        full = await event.client.get_entity(event.message.from_id)
    except Exception as e:
        LOGS.info(str(e))
    messaget = media_type(event)
    resalt = f" المجموعه : </b><code>{hmm.title}</code>"
    if full is not None:
        resalt += f"\n<b> المرسل : </b> {_format.htmlmentionuser(full.first_name , full.id)}"
    if messaget is not None:
        resalt += f"\n<b> رسالة جديدة : </b><code>{messaget}</code>"
    else:
        resalt += f"\n<b> رسالة جديدة: </b>{event.message.message}"
    resalt += f"\n<b> رابط الرساله : </b><a href = 'https://t.me/c/{hmm.id}/{event.message.id}'> اضغط هنا</a>"
    if not event.is_private:
        await event.client.send_message(
            Config.PM_LOGGER_GROUP_ID,
            resalt,
            parse_mode="html",
            link_preview=False,
        )


@Superthon.ar_cmd(pattern="خزن(?:\s|$)([\s\S]*)")
async def log(log_text):
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"#لوك / ايدي الدردشه : {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await log_text.client.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit(" يجب عليك الرد على شي لحفظه في كروب التخزين")
            return
        await log_text.edit(" تم التخزين و حفظه في كروب التخزين بنجاح")
    else:
        await log_text.edit(" عزيزي هذه الميزه تطلب تفعيل فار التخزين اولا")
    await asyncio.sleep(2)
    await log_text.delete()


@Superthon.ar_cmd(pattern="تفعيل التخزين$")
async def set_no_log_p_m(event):
    if Config.PM_LOGGER_GROUP_ID != -100:
        chat = await event.get_chat()
        if no_log_pms_sql.is_approved(chat.id):
            no_log_pms_sql.disapprove(chat.id)
            await edit_delete(event, "** تم تفعيل التخزين لهذه الدردشه بنجاح **", 5)


@Superthon.ar_cmd(pattern="تعطيل التخزين$")
async def set_no_log_p_m(event):
    if Config.PM_LOGGER_GROUP_ID != -100:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id):
            no_log_pms_sql.approve(chat.id)
            await edit_delete(event, "** تم تعطيل التخزين لهذه الدردشه بنجاح **", 5)


@Superthon.ar_cmd(pattern="تخزين الخاص (تشغيل|ايقاف)$")
async def set_pmlog(event):
    input_str = event.pattern_match.group(1)
    if input_str == "ايقاف":
        h_type = False
    elif input_str == "تشغيل":
        h_type = True
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        PMLOG = False
    else:
        PMLOG = True
    if PMLOG:
        if h_type:
            await event.edit("** تخزين رسائل الخاص بالفعل مُمكنة **")
        else:
            addgvar("PMLOG", h_type)
            await event.edit("** تم تعطيل تخزين رسائل الخاص بنجاح **")
    elif h_type:
        addgvar("PMLOG", h_type)
        await event.edit("** تم تفعيل تخزين رسائل الخاص بنجاح **")
    else:
        await event.edit("** تخزين رسائل الخاص بالفعل معطلة **")


@Superthon.ar_cmd(pattern="تخزين الكروبات (تشغيل|ايقاف)$")
async def set_grplog(event):
    input_str = event.pattern_match.group(1)
    if input_str == "ايقاف":
        h_type = False
    elif input_str == "تشغيل":
        h_type = True
    if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") == "false":
        GRPLOG = False
    else:
        GRPLOG = True
    if GRPLOG:
        if h_type:
            await event.edit("** تخزين رسائل الكروبات بالفعل مُمكنة **")
        else:
            addgvar("GRPLOG", h_type)
            await event.edit("** تم تعطيل تخزين رسائل الكروبات بنجاح **")
    elif h_type:
        addgvar("GRPLOG", h_type)
        await event.edit("** تم تفعيل تخزين رسائل الكروبات بنجاح **")
    else:
        await event.edit("** تخزين رسائل الكروبات بالفعل معطلة **")
