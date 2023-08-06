# Copyright (c) Vyoma Systems Private Limited
# See LICENSE.vyoma for details

""" utils """
import sys
import os
import subprocess
import shlex
from reporg.log import logger
from threading import Timer

def cmd_null(command, timeout=500):
    logger.warning('$ timeout={1} {0} '.format(' '.join(shlex.split(command)), timeout))
    x = subprocess.Popen(shlex.split(command),
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL,
                         )
    timer = Timer(timeout, x.kill)
    try:
        timer.start()
        out, err = x.communicate()
    finally:
        timer.cancel()
        
    return x.returncode

def cmd(command, timeout=500):
    logger.warning('$ timeout={1} {0} '.format(' '.join(shlex.split(command)), timeout))
    x = subprocess.Popen(shlex.split(command),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         )
    timer = Timer(timeout, x.kill)
    try:
        timer.start()
        out, err = x.communicate()
    finally:
        timer.cancel()
        
    out = out.rstrip()
    err = err.rstrip()
    if x.returncode != 0:
        if out:
            logger.error(out.decode("ascii"))
        if err:
            logger.error(err.decode("ascii"))
    else:
        if out:
            logger.debug(out.decode("ascii"))
        if err:
            logger.debug(err.decode("ascii"))
    return (x.returncode, out.decode("ascii"), err.decode("ascii"))

def cmd_file(command, filename, timeout=500):
    cmd = command.split(' ')
    cmd = [x.strip(' ') for x in cmd]
    cmd = [i for i in cmd if i] 
    logger.warning('$ {0} > {1}'.format(' '.join(cmd), filename))
    fp = open(filename, 'w')
    x = subprocess.Popen(cmd, stdout=fp, stderr=fp)
    timer = Timer(timeout, x.kill)
    try:
        timer.start()
        stdout, stderr = x.communicate()
    finally:
        timer.cancel()
    
    fp.close()

    return (x.returncode, None, None)

def check_environ(env_list):
    exit = 0
    for env in env_list:
        if env in os.environ:
            logger.info(f'Env variable : {env} = {os.environ[env]}')
        else:
            logger.info(f'Env variable : {env} not defined')
            exit = 1
    if exit:
        logger.error('Please re-run after setting the envronment variables')
        sys.exit(40)
