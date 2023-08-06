import importlib
import site


def try_import(lib):
    try:
        importlib.reload(site)
        globals()[lib] = importlib.import_module(lib)
        importlib.import_module(lib)
    except Exception as _:
        # print(f'Failed to import {lib}')
        return False
    return True
