#!/bin/sh
# エラーなら停止
set -eu

echo "deploy start"

for f in poke-worker1 poke-worker2 poke-worker3 poke-worker4; do
  echo ""
  echo "_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/"
  echo "$f"
  echo "_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/"
  ssh -l root $f "date"
  ssh -l root $f "cd /var/poke/pokemap && git pull origin master"
done

for f in poke-worker5 poke-worker6 poke-worker7 poke-worker8 poke-worker9 poke-worker10 poke-worker11 poke-worker12 poke-worker13; do
  echo ""
  echo "_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/"
  echo "$f"
  echo "_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/"
  ssh -l root $f "date"
  ssh -l root $f "cd /var/poke/pokemap && git pull origin master"
done

