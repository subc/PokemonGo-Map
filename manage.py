# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from app import create_app
from command.map_update import MapUpdate

manager = Manager(create_app)

# manage.py option
manager.add_option('-c', '--config', dest='config', required=False)

######################
# コマンド追加
######################
# runserver
manager.add_command('runserver', Server(use_reloader=True))
manager.add_command('up', MapUpdate())


if __name__ == "__main__":
    manager.run()