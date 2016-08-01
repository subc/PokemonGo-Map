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
