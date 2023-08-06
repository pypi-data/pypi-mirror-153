from johnsnowlabs.abstract_base.lib_resolvers import try_import_lib

# TODO this could be NLU?
if try_import_lib('nlu', True):
    import nlu
else:
    print(f'If you want to fix this problem, Do <TODO ?????>')
