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


firstbyte_client = ApiFirstByte(login=Config.FIRSTBYTE_LOGIN, password=Config.FIRSTBYTE_PASSWORD)

for ip, data in firstbyte_client.get_servers(with_pass=True).items():
    if ip == '185.217.199.160' or ip == '193.162.143.159':
        continue
    c = fabric.Connection(ip, port=22, user="root", connect_kwargs={'password': data["password"]})

    with open("Server.txt") as file_txt_command:
        txt_command = file_txt_command.read()

    for command in split_ssh_comand(txt_format=txt_command):
        c.run(command)
    for command in [
        'crontab -l 2>/dev/null| cat - <(echo "0 6 * * * sudo shutdown -r") | crontab -',
        'crontab -l 2>/dev/null| cat - <(echo "*/5 * * * * chmod +x /root/Insurance_RCA/run.py; cd /root/Insurance_RCA/ && run-one nohup python3.9 -u ./run.py > output.log &") | crontab -'
        ]:
        c.run(command)

    with pysftp.Connection(ip, username='root', password=data["password"], cnopts=cnopts) as sftp:
        sftp.makedirs("/root/Insurance_RCA")
        put_r_portable(sftp, f'{Config.GOOGLEDISC_DIR_ADDRESS}/Insurance/Insurance_RCA', '/root/Insurance_RCA/', preserve_mtime=False)