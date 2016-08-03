#!/bin/sh
# エラーなら停止
set -eu

echo "deploy start sup"

# worker1
ssh -l root poke-worker1 "rm -rf /var/log/supervisor/*"
ssh -l root poke-worker1 "rm -rf /etc/supervisord.d/*"
ssh -l root poke-worker1 "cp /var/poke/pokemap/config/supervisord/up/0/* /etc/supervisord.d/"
echo "worker1 finish"

# worker2
ssh -l root poke-worker2 "rm -rf /var/log/supervisor/*"
ssh -l root poke-worker2 "rm -rf /etc/supervisord.d/*"
ssh -l root poke-worker2 "cp /var/poke/pokemap/config/supervisord/up/1/* /etc/supervisord.d/"
echo "worker2 finish"

# worker3
ssh -l root poke-worker3 "rm -rf /var/log/supervisor/*"
ssh -l root poke-worker3 "rm -rf /etc/supervisord.d/*"
ssh -l root poke-worker3 "cp /var/poke/pokemap/config/supervisord/up/2/* /etc/supervisord.d/"
echo "worker3 finish"

# worker4
ssh -l root poke-worker4 "rm -rf /var/log/supervisor/*"
ssh -l root poke-worker4 "rm -rf /etc/supervisord.d/*"
ssh -l root poke-worker4 "cp /var/poke/pokemap/config/supervisord/up/3/* /etc/supervisord.d/"
echo "worker4 finish"
