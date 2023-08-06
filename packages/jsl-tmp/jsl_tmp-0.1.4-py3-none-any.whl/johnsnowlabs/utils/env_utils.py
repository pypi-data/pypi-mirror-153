import importlib
import site
import os

def try_import(lib):
    try:
        importlib.reload(site)
        globals()[lib] = importlib.import_module(lib)
        importlib.import_module(lib)
    except Exception as _:
        # print(f'Failed to import {lib}')
        return False
    return True



def is_running_in_databricks():
    """ Check if the currently running Python Process is running in Databricks or not
     If any Environment Variable name contains 'DATABRICKS' this will return True, otherwise False"""
    for k in os.environ.keys():
        if 'DATABRICKS' in k:
            return True
    return False