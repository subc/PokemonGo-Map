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

# worker5
ssh -l root poke-worker5 "rm -rf /var/log/supervisor/*"
ssh -l root poke-worker5 "rm -rf /etc/supervisord.d/*"
ssh -l root poke-worker5 "cp /var/poke/pokemap/config/supervisord/up/4/* /etc/supervisord.d/"
echo "worker5 finish"

# worker6
ssh -l root poke-worker6 "rm -rf /var/log/supervisor/*"
ssh -l root poke-worker6 "rm -rf /etc/supervisord.d/*"
ssh -l root poke-worker6 "cp /var/poke/pokemap/config/supervisord/up/5/* /etc/supervisord.d/"
echo "worker6 finish"

# worker7
ssh -l root poke-worker7 "rm -rf /var/log/supervisor/*"
ssh -l root poke-worker7 "rm -rf /etc/supervisord.d/*"
ssh -l root poke-worker7 "cp /var/poke/pokemap/config/supervisord/up/6/* /etc/supervisord.d/"
echo "worker7 finish"

# worker8
ssh -l root poke-worker8 "rm -rf /var/log/supervisor/*"
ssh -l root poke-worker8 "rm -rf /etc/supervisord.d/*"
ssh -l root poke-worker8 "cp /var/poke/pokemap/config/supervisord/up/7/* /etc/supervisord.d/"
echo "worker8 finish"

# worker9
ssh -l root poke-worker9 "rm -rf /var/log/supervisor/*"
ssh -l root poke-worker9 "rm -rf /etc/supervisord.d/*"
ssh -l root poke-worker9 "cp /var/poke/pokemap/config/supervisord/up/8/* /etc/supervisord.d/"
echo "worker9 finish"

# worker10
ssh -l root poke-worker10 "rm -rf /var/log/supervisor/*"
ssh -l root poke-worker10 "rm -rf /etc/supervisord.d/*"
ssh -l root poke-worker10 "cp /var/poke/pokemap/config/supervisord/up/9/* /etc/supervisord.d/"
echo "worker10 finish"

# worker11
ssh -l root poke-worker11 "rm -rf /var/log/supervisor/*"
ssh -l root poke-worker11 "rm -rf /etc/supervisord.d/*"
ssh -l root poke-worker11 "cp /var/poke/pokemap/config/supervisord/up/10/* /etc/supervisord.d/"
echo "worker11 finish"

# worker12
ssh -l root poke-worker12 "rm -rf /var/log/supervisor/*"
ssh -l root poke-worker12 "rm -rf /etc/supervisord.d/*"
ssh -l root poke-worker12 "cp /var/poke/pokemap/config/supervisord/up/11/* /etc/supervisord.d/"
echo "worker12 finish"

# worker13
ssh -l root poke-worker13 "rm -rf /var/log/supervisor/*"
ssh -l root poke-worker13 "rm -rf /etc/supervisord.d/*"
ssh -l root poke-worker13 "cp /var/poke/pokemap/config/supervisord/up/12/* /etc/supervisord.d/"
echo "worker13 finish"
