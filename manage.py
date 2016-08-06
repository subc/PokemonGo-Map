# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from app import create_app
from command.map_update import MapUpdate
from command.check_worker import CheckWorker
from command.map_update_curl import MapUpdateCurl
from command.profile_point_access import ProfilePointAccess
from command.map_update_from_url import MapUpdateFromUrl
from command.map_update_from_url2 import MapUpdateFromUrl2

manager = Manager(create_app)

# manage.py option
manager.add_option('-c', '--config', dest='config', required=False)

######################
# コマンド追加
######################
# runserver
manager.add_command('runserver', Server(use_reloader=True))
manager.add_command('up_old2', MapUpdate())
manager.add_command('cw', CheckWorker())
manager.add_command('prof', ProfilePointAccess())
manager.add_command('up_dummy', MapUpdateCurl())  # dummy
manager.add_command('up_old_20160806', MapUpdateFromUrl())
manager.add_command('up', MapUpdateFromUrl2())


if __name__ == "__main__":
    manager.run()
