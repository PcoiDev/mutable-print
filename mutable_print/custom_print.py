from typing import Any, Optional, TextIO, Callable
from .mutable_print import mutable_print

_original_print: Callable[..., None] = print


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


def enable_custom_print() -> None:
    """
    Enable custom print interception.
    
    Replaces the built-in print function with the mutable_print version.
    """
    if not mutable_print._intercept_mode:
        mutable_print._intercept_mode = True
        mutable_print._original_write = mutable_print._original_stdout.write
        import builtins
        builtins.print = _intercepted_print


def disable_custom_print() -> None:
    """
    Disable custom print interception.
    
    Restores the original built-in print function.
    """
    if mutable_print._intercept_mode:
        mutable_print._intercept_mode = False
        import builtins
        builtins.print = _original_print


def toggle_custom_print() -> None:
    """
    Toggle custom print interception on/off.
    
    If currently enabled, disables it. If currently disabled, enables it.
    """
    if mutable_print._intercept_mode:
        disable_custom_print()
    else:
        enable_custom_print()


def is_custom_print_enabled() -> bool:
    """
    Check if custom print interception is currently enabled.
    
    Returns:
        True if custom print is enabled, False otherwise
    """
    return mutable_print._intercept_mode