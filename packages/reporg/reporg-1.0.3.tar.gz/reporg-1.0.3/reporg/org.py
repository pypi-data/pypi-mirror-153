# Copyright (c) Vyoma Systems Private Limited
# See LICENSE.vyoma for details

import sys
import os
import shutil
import yaml
import git 

from reporg.log import *
from reporg.utils import *
from reporg.constants import *
from reporg.__init__ import __version__

def org(dir, clean, list):

    logger.info('****** Repository Organizer {0} *******'.format(__version__ ))
    logger.info('Copyright (c) 2022, Vyoma Systems Private Limited')
    logger.info('All Rights Reserved.')
    
    clone_list = dict()
    with open(list) as list_handle:
      clone_list = yaml.safe_load(list_handle)
    
    patch_dir = os.path.dirname(list)
    if clean:
      for repo in clone_list:
        repo_path = dir + '/' + repo
        logger.info('Cleaning dir : {0}'.format(repo_path))
        shutil.rmtree(repo_path, ignore_errors=True, onerror=None)  
    else:
      for repo in clone_list:
        repo_path = dir + '/' + repo
        logger.info('Cleaning dir : {0}'.format(repo_path))
        shutil.rmtree(repo_path, ignore_errors=True, onerror=None)
      for repo in clone_list:
        logger.info('Cloning : {0} '.format(repo))
        repo_url = clone_list[repo]['name']
        repo_path = dir + '/' + repo
        checkout_str = clone_list[repo]['branch']
        rg = git.Repo.clone_from(repo_url, repo_path, no_checkout=True)
        logger.info('clone done : {0} '.format(repo))
        rg.git.checkout(checkout_str)
        logger.info('checkout done : {0} '.format(repo))
        rg.git.submodule('update', '--init')
        #for submodule in rg.submodules:
        #  submodule.update(init=True)
        logger.info('submodule done : {0} '.format(repo))
        if 'patch' in clone_list[repo]:
          logger.info(clone_list[repo]['patch'])
          if clone_list[repo]['patch']:
            patch_file = clone_list[repo]['patch']
            for path in patch_file:
              file_path = patch_dir + '/' + str(patch_file[path])
              apply_path = dir + '/' + path
              logger.info('Apply {0} to {1}'.format(file_path, apply_path))
              repo_patched = git.Repo(apply_path)
              logger.info(repo_patched.git.apply(file_path))
