import os
from os.path import expanduser

home = expanduser("~")
JSL_HOME = f'{home}/.johnsnowlabs'

if not os.path.exists(JSL_HOME):
    os.mkdir(JSL_HOME)
