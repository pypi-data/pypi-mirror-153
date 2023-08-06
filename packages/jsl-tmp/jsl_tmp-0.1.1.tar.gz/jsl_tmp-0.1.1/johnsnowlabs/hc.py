from johnsnowlabs.utils.lib_resolvers import try_import_lib
from sparknlp_jsl.annotator import *
from sparknlp_jsl.base import *

if try_import_lib('spark_nlp_jsl',True):
    from sparknlp_jsl.annotator import *
    from sparknlp_jsl.base import *
else:
    print(f'NLP :If you want to fix this problem, Do <TODO ?????>')
