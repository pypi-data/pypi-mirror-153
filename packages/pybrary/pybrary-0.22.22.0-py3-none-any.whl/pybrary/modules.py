from importlib.util import spec_from_file_location
from importlib.util import module_from_spec

from . import debug

def load(mod_name, mod_file):
    debug('module.load name:%s file:%s', mod_name, mod_file)
    spec = spec_from_file_location(mod_name, mod_file)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    debug('module loaded : %s', mod)
    return mod
