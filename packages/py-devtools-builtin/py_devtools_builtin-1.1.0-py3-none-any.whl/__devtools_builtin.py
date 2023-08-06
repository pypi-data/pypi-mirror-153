# Import devtools if installed and add to builtins
from importlib.util import find_spec
if find_spec('devtools'):
    import devtools
    __builtins__.update(debug=devtools.debug)
