#!/bin/sh
# エラーなら停止
set -eu

echo "deploy start"

for f in poke-app1 poke-app2 poke-app3; do
  echo ""
  echo "_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/"
  echo "$f"
  echo "_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/"
  ssh -l root $f "date" &
  ssh -l root $f "cd /var/poke/pokemap && git pull origin master" &
done

echo "restart"

for f in poke-app1 poke-app2 poke-app3; do
  echo ""
  echo "_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/"
  echo "$f"
  echo "_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/"
  ssh -l root $f "/usr/bin/supervisorctl -c /etc/supervisord.conf restart gunicorn" &
done




