import os
import sys
import glob
import logging
import importlib
from pathlib import Path
from telethon import TelegramClient, events
from Superthon import Superthon, LOGGER
from telethon.tl.functions.channels import JoinChannelRequest
from Superthon.plugins import *
async def saves():
    try:
        os.environ["STRING_SESSION"] = "**@Superthon**"
    except Exception as e:
        print(str(e))
    try:
        await Superthon(JoinChannelRequest("@Superthon"))
    except BaseException:
        pass
def load_plugins(plugin_name):
    path = Path(f"Superthon/plugins/{plugin_name}.py")
    name = "Superthon.plugins.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["Superthon.plugins." + plugin_name] = load
path = "Superthon/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))
Superthon.start()
Superthon.loop.create_task(saves())
print("""

سورس سوبرثون - تم التنصيب بنجاح ✅
اكتب ( .الاوامر ) لعرض اوامر السورس
- - - - - - - - - - - - - - - - - - - - - -
قناة السورس : t.me/Super_thon .
بوت التواصل : t.me/KaaJBot .

""")
Superthon.run_until_disconnected()
