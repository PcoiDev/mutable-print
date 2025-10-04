from .custom_print import enable_custom_print, disable_custom_print, toggle_custom_print, is_custom_print_enabled
from .mutable_print import mutable_print

enable_custom_print()

__all__ = [
    "enable_custom_print",
    "disable_custom_print",
    "toggle_custom_print",
    "is_custom_print_enabled",
    
    "mutable_print"
]