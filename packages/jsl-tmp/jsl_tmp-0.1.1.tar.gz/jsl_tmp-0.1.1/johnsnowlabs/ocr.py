from johnsnowlabs.utils.lib_resolvers import try_import_lib

if try_import_lib('sparkocr', True):
    from sparkocr.transformers import *
    from sparkocr.enums import *
    import sparkocr
    sparkocr
else:
    print(f'OCR : If you want to fix this problem, Do <TODO ?????>')
