import datetime
import os
import random
import sys

from officy import JsonFile
from rumit import Rumit

# git clone https://github.com/liujuanjuan1984/mixin-sdk-python
mixin_dirpath = r"D:\Jupyter\mixin-sdk-python"
sys.path.insert(0, mixin_dirpath)
import mixinsdk
from mixinsdk.clients.http_client import AppConfig, HttpClient_AppAuth
from mixinsdk.types.message import pack_message, pack_text_data

from examples._example_vars import CNB_ASSET_ID, MY_USER_ID, user_config_FILE

rum = Rumit(port=58356)
xin = HttpClient_AppAuth(AppConfig.from_file(user_config_FILE))

MY_GROUP_ID = "e81c28a6-47aa-3aa0-97d2-62ac1754c90f"  # "b807ebea-4b46-4cf6-89c5-3a810ba9d32e"

# send message to group

text = 'hi'

msg = pack_message(pack_text_data(text), MY_GROUP_ID)
r = xin.api.send_messages(msg)
print(r)
