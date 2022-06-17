"""
Ассинхронный деплой
"""

import asyncio, asyncssh, sys
import fabric
import os
from api_firstbyte import ApiFirstByte
from contextlib import suppress
import pysftp
from config import Config
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

def put_r_portable(sftp, localdir, remotedir, preserve_mtime=False):
    for entry in os.listdir(localdir):
        remotepath = remotedir + "/" + entry
        localpath = os.path.join(localdir, entry)
        if not os.path.isfile(localpath):
            try:
                sftp.mkdir(remotepath)
            except OSError:
                pass
            put_r_portable(sftp, localpath, remotepath, preserve_mtime)
        else:
            sftp.put(localpath, remotepath, preserve_mtime=preserve_mtime)

def split_ssh_comand(txt_format:str) -> list:
    edit_txt = txt_format.replace(";\\", ";").replace("\n", "")
    return edit_txt.split(";")


async def run_client(ip, data):
    print(f"ip:{ip}, pass:{data['password']}")
    with open("Server.txt") as file_txt_command:
        txt_command = file_txt_command.read()
    async with asyncssh.connect(ip, username="root", password=data["password"], known_hosts=None) as conn:
        result = await conn.run(txt_command, check=True)
        print(f"Завершено: ip:{ip}, pass:{data['password']}")

ioloop = asyncio.get_event_loop()
tasks = []
firstbyte_client = ApiFirstByte(login=Config.FIRSTBYTE_LOGIN, password=Config.FIRSTBYTE_PASSWORD)
for ip, data in firstbyte_client.get_servers(with_pass=True).items():
    if ip == '185.217.199.160' or ip == '193.162.143.159':
        continue
    ioloop.create_task(run_client(ip, data))

try:
    ioloop.run_forever()
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))
