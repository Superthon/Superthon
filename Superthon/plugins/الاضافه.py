import asyncio
import csv
import random

from telethon import functions
from telethon.errors.rpcerrorlist import (
    UserAlreadyParticipantError,
    UserNotMutualContactError,
    UserPrivacyRestrictedError,
)
from telethon.tl import functions
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerUser

from Superthon import Superthon

from ..core.managers import edit_delete, edit_or_reply


@Superthon.ar_cmd(pattern="انضمام ([\s\S]*)")
async def lol(event):
    a = event.text
    bol = a[5:]
    sweetie = "- جاري الانضمام الى المجموعة انتظر قليلا  ."
    await event.reply(sweetie, parse_mode=None, link_preview=None)
    try:
        await Superthon(functions.channels.JoinChannelRequest(bol))
        await event.edit("**- تم الانضمام بنجاح  **")
    except Exception as e:
        await event.edit(str(e))


@Superthon.ar_cmd(pattern="اضافه ([\s\S]*)")
async def _(event):
    to_add_users = event.pattern_match.group(1)
    if not event.is_channel and event.is_group:
        for user_id in to_add_users.split(" "):
            try:
                await event.client(
                    functions.messages.AddChatUserRequest(
                        chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000
                    )
                )
            except Exception as e:
                return await edit_delete(event, f"`{str(e)}`", 5)
    else:
        for user_id in to_add_users.split(" "):
            try:
                await event.client(
                    functions.channels.InviteToChannelRequest(
                        channel=event.chat_id, users=[user_id]
                    )
                )
            except Exception as e:
                return await edit_delete(event, f"`{e}`", 5)

    await edit_or_reply(event, f"**{to_add_users} تم اضافته بنجاح **")


@Superthon.ar_cmd(pattern="ضيف ([\s\S]*)", groups_only=True)
async def get_users(event):
    legen_ = event.text[10:]
    Superthon_chat = legen_.lower
    restricted = ["@Super_thon", "@Super_thon"]
    Superthon = await edit_or_reply(event, f"**جارِ اضأفه الاعضاء من  ** {legen_}")
    if Superthon_chat in restricted:
        return await Superthon.edit(
            event, "**- لا يمكنك اخذ اعضاء من جموعة السورس **"
        )
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        await Superthon.edit("** تتم العملية انتظر قليلا ...**")
    else:
        await Superthon.edit("** تتم العملية انتظر قليلا ...**")
    if event.is_private:
        return await Superthon.edit("- لا يمكنك اضافه الاعضاء هنا")
    s = 0
    f = 0
    error = "None"
    await Superthon.edit(
        "** حالة الأضافة:**\n\n** تتم جمع معلومات المستخدمين  ...**"
    )
    async for user in event.client.iter_participants(event.pattern_match.group(1)):
        try:
            if error.startswith("Too"):
                return await Superthon.edit(
                    f"**حالة الأضافة انتهت مع الأخطاء**\n- (**ربما هنالك ضغط على الأمر حاول مجددا لاحقا **) \n**الخطأ** : \n`{error}`\n\n• اضافة `{s}` \n• خطأ بأضافة `{f}`"
                )
            tol = f"@{user.username}"
            lol = tol.split("`")
            await Superthon(InviteToChannelRequest(channel=event.chat_id, users=lol))
            s = s + 1
            await Superthon.edit(
                f"**تتم الأضافة **\n\n• اضيف `{s}` \n•  خطأ بأضافة `{f}` \n\n**× اخر خطأ:** `{error}`"
            )
        except Exception as e:
            error = str(e)
            f = f + 1
    return await Superthon.edit(
        f"**اكتملت الأضافة ✅** \n\n• تم بنجاح اضافة `{s}` \n• خطأ بأضافة `{f}`"
    )


@Superthon.ar_cmd(pattern="تجميع الاعضاء$")
async def scrapmem(event):
    chat = event.chat_id
    xx = await edit_or_reply(event, "** تتم العملية انتظر قليلا  .**")
    members = await event.client.get_participants(chat, aggressive=True)
    with open("members.csv", "w", encoding="UTF-8") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(["user_id", "hash"])
        for member in members:
            writer.writerow([member.id, member.access_hash])
    await xx.edit("** تم تجميع الاعضاء بنجاح ،**")


@Superthon.ar_cmd(pattern="اضف الاعضاء$")
async def admem(event):
    xx = await edit_or_reply(event, "** اضافه 0 من الاعضاء  ؟..**")
    chat = await event.get_chat()
    users = []
    with open("members.csv", encoding="UTF-8") as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {"id": int(row[0]), "hash": int(row[1])}
            users.append(user)
    n = 0
    for user in users:
        n += 1
        if n % 30 == 0:
            await xx.edit(
                f"** لقد قمت بأضافه 30 عضو لا يمكنك الاضافه اكثر الان انتظر :** `{900/60}` **دقيقة**"
            )
            await asyncio.sleep(900)
        try:
            userin = InputPeerUser(user["id"], user["hash"])
            await event.client(InviteToChannelRequest(chat, [userin]))
            await asyncio.sleep(random.randrange(5, 7))
            await xx.edit(f"** تم اكمال العمليه جار أضافه** `{n}` **من الاعضاء**")
        except TypeError:
            n -= 1
            continue
        except UserAlreadyParticipantError:
            n -= 1
            continue
        except UserPrivacyRestrictedError:
            n -= 1
            continue
        except UserNotMutualContactError:
            n -= 1
            continue


# Superthon
