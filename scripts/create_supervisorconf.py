# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.password import ACCOUNTS
import codecs
from config.production import REDIS_HOSTS
from points import POINTS


F = """[program:{}]
command=/root/.virtualenvs/poke/bin/python /var/poke/pokemap/manage.py -c ./config/production.py up -p {}
user=root
autorestart=true
stdout_logfile=/var/log/supervisor/{}-supervisord.log ; 標準出力ログ
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=5
stdout_capture_maxbytes=1MB
redirect_stderr=true
"""


def create_file(ct):
    print("[+]start create file : {}".format(ct))
    _base_path = "/Users/ikeda/noah/maps/config/supervisord/up/"
    filename = "up{0:03d}".format(ct)
    body = F.format(filename, ct, filename)
    print(body)

    # set folder
    folder_name = ct % 13
    path = _base_path + str(folder_name) + "/" + filename + ".ini"

    with codecs.open(path, "w", "utf-8") as file:
        file.write(body)


print("start")
ct = 0
assert len(ACCOUNTS) >= len(POINTS), "{}:{}".format(len(ACCOUNTS), len(POINTS))

for x, y, _ in POINTS:
    create_file(ct)
    ct += 1
