#!/bin/sh
# エラーなら停止
set -eu

echo "deploy start sup"

# app1
scp ./config/password.py poke-app1:/var/poke/pokemap/config/password.py
echo "app1 finish"

# app2
scp ./config/password.py poke-app2:/var/poke/pokemap/config/password.py
echo "app2 finish"

# app3
scp ./config/password.py poke-app3:/var/poke/pokemap/config/password.py
echo "app3 finish"


# worker1
scp ./config/password.py poke-worker1:/var/poke/pokemap/config/password.py
echo "worker1 finish"

# worker2
scp ./config/password.py poke-worker2:/var/poke/pokemap/config/password.py
echo "worker2 finish"

# worker3
scp ./config/password.py poke-worker3:/var/poke/pokemap/config/password.py
echo "worker3 finish"

# worker4
scp ./config/password.py poke-worker4:/var/poke/pokemap/config/password.py
echo "worker4 finish"

# worker5
scp ./config/password.py poke-worker5:/var/poke/pokemap/config/password.py
echo "worker5 finish"

# worker6
scp ./config/password.py poke-worker6:/var/poke/pokemap/config/password.py
echo "worker6 finish"

# worker7
scp ./config/password.py poke-worker7:/var/poke/pokemap/config/password.py
echo "worker7 finish"

# worker8
scp ./config/password.py poke-worker8:/var/poke/pokemap/config/password.py
echo "worker8 finish"

# worker9
scp ./config/password.py poke-worker9:/var/poke/pokemap/config/password.py
echo "worker9 finish"

# worker10
scp ./config/password.py poke-worker10:/var/poke/pokemap/config/password.py
echo "worker10 finish"

# worker11
scp ./config/password.py poke-worker11:/var/poke/pokemap/config/password.py
echo "worker11 finish"

# worker12
scp ./config/password.py poke-worker12:/var/poke/pokemap/config/password.py
echo "worker12 finish"

# worker13
scp ./config/password.py poke-worker13:/var/poke/pokemap/config/password.py
echo "worker13 finish"

