#!/bin/sh

# app 試験
# エラーなら停止
set -eu

for f in poke-app1 poke-app2 poke-app3; do
  echo ""
  echo "_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/"
  echo "$f"
  echo "_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/"
  ssh -l root $f "date"
  ssh -l root $f "ls -lta /var/log/nginx"
done

for f in poke-worker1 poke-worker2 poke-worker3 poke-worker4; do
  echo ""
  echo "_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/"
  echo "$f"
  echo "_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/"
  ssh -l root $f "date"
  ssh -l root $f "/usr/bin/supervisorctl -c /etc/supervisord.conf status"
done
