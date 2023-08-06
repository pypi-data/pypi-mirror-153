from johnsnowlabs.abstract_base.lib_resolvers import try_import_lib

if try_import_lib('nlu', True):
    import nlu as nlu
    from sparknlp.base import *
    from sparknlp.annotator import *
else:
    pass
