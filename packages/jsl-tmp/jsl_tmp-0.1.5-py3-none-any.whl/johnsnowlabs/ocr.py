from johnsnowlabs.abstract_base.lib_resolvers import try_import_lib

if try_import_lib('sparkocr', True):
    from sparkocr.transformers import *
    from sparkocr.enums import *
    import sparkocr
else:
    pass
