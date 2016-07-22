#!/usr/bin/env bash
# 停止コマンド
ps -ax |pgrep -f 'run_worker'|xargs kill
ps -ax |pgrep -f 'worker.py'|xargs kill
ps -ax |pgrep -f 'manage.py up' |xargs kill
