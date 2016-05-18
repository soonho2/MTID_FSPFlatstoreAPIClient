import os
from shutil import copyfile
import pwd
import grp

__author__ = 'Peter Hinson'

import config

# class DrupalWebUploader(object):
#     def login(self, username=config.DRUPAL_USERNAME, password=config.DRUPAL_PASSWORD):
#         pass

class DrupalUploader(object):
    def copy_file(self, filepath):
        if not filepath:
            return
        out_path = os.path.join(config.UPLOAD_PATH, os.path.basename(filepath))
        copyfile(filepath, out_path)
        #
        # uid = pwd.getpwnam("nobody").pw_uid
        # gid = grp.getgrnam("nogroup").gr_gid
        # path = out_path
        # os.chown(path, uid, gid)
