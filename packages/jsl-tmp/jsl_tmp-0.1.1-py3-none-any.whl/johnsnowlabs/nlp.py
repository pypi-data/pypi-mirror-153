from johnsnowlabs.utils.lib_resolvers import try_import_lib
from sparknlp.base import *
from sparknlp.annotator import *

if try_import_lib('nlu',True):
    import nlu
else:
    print(f'If you want to fix this problem, Do <TODO ?????>')
