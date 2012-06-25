# Taken from Python 2.7 with permission from/by the original author.
import sys

def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in xrange(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)

def get_apppath(appname):
    def get(base, parts):
        if not parts:
            return base
        base = os.path.join(base, parts[0])
        if not (os.path.isfile(os.path.join(base, "__init__.py")) or (os.path.join(base, "__init__.pyc"))):
            return None
        return get(base, parts[1:])

    import sys
    import os
    parts = appname.split(".")
    for base in sys.path:
        result = get(base, parts)    
        if not get(base, parts) is None:
            return os.path.join(base, *parts)
    raise Exception("No such app: %s" % appname)

def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]
