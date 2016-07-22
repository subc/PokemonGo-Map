#!/bin/sh
# エラーなら停止
set -eu

echo "deploy start"

for f in poke-worker1; do
  echo "$f"
  ssh -l root $f "date"
  ssh -l root $f "cd /var/poke/pokemap && git pull origin master"
  ssh -l root $f "/usr/bin/supervisorctl -c /etc/supervisord.conf restart all"
done



