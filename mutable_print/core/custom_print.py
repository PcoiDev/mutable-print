from typing import Any, Optional, TextIO
from ..mutable_print import mutable_print
import builtins

def _intercepted_print(*args: Any, **kwargs: Any) -> None:
    """
    Intercept print calls and redirect them to mutable_print.
    
    Args:
        *args: Positional arguments to print
        **kwargs: Keyword arguments (sep, end, file, flush)
    """
    sep: str = kwargs.get('sep', ' ')
    end: str = kwargs.get('end', '\n')
    file: Optional[TextIO] = kwargs.get('file', None)
    flush: bool = kwargs.get('flush', False)
    mutable_print(*args, sep=sep, end=end, file=file, flush=flush)

mutable_print._original_write = mutable_print._original_stdout.write
builtins.print = _intercepted_print