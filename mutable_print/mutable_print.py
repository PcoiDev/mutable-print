from typing import Any, Optional, TextIO, List, Tuple
import sys
import re
from .core.combine_text import combine_text

class mutable_print:
    __slots__ = ('args', 'sep', 'end', 'file', 'flush', 'content', 'index', '_cached_output')
    
    _global_prints: List['mutable_print'] = []
    _original_stdout: TextIO = sys.stdout
    _original_write: Optional[Any] = None
    _intercept_mode: bool = False
    
    def __init__(
        self,
        *args: Any,
        sep: str = ' ',
        end: str = '\n',
        file: Optional[TextIO] = None,
        flush: bool = False
    ) -> None:
        self.args: Tuple[Any, ...] = args
        self.sep: str = sep
        self.end: str = end
        self.file: TextIO = file or mutable_print._original_stdout
        self.flush: bool = flush
        self.content: str = sep.join(str(arg) for arg in args)
        self.index: int = len(mutable_print._global_prints)
        self._cached_output: str = self.content + self.end
        mutable_print._global_prints.append(self)
        self._print_initial()
    
    def _print_initial(self) -> None:
        mutable_print._original_write(self._cached_output)
        if self.flush:
            mutable_print._original_stdout.flush()
    
    @classmethod
    def _find_line_start(cls, index: int) -> Tuple[int, int]:
        """
        Find the start of the current line and count how many lines need clearing.
        Returns (start_index, lines_to_clear)
        """
        if index >= len(cls._global_prints):
            return index, 0
        
        # Find the beginning of the current line
        line_start = index
        for i in range(index - 1, -1, -1):
            if not cls._global_prints[i].end.endswith('\n'):
                line_start = i
            else:
                break
        
        # Count lines from line_start to end
        lines = 0
        on_same_line = False
        
        for i in range(line_start, len(cls._global_prints)):
            output = cls._global_prints[i]._cached_output
            
            if not on_same_line or i == line_start:
                # Starting a new line or first item
                newlines = output.count('\n')
                if newlines == 0:
                    if output:  # Non-empty output without newline
                        if i == len(cls._global_prints) - 1 or cls._global_prints[i + 1]._cached_output:
                            lines = max(lines, 1)
                    on_same_line = True
                else:
                    lines += newlines
                    on_same_line = not output.endswith('\n')
            else:
                # Continuing on same line
                newlines = output.count('\n')
                if newlines > 0:
                    lines += newlines
                    on_same_line = not output.endswith('\n')
        
        return line_start, lines
    
    @classmethod
    def _reprint_from(cls, start_index: int) -> None:
        """Efficiently reprint all mutable_print objects from start_index onwards."""
        if start_index >= len(cls._global_prints):
            return
        
        # Find actual start and lines to clear
        actual_start, lines_to_clear = cls._find_line_start(start_index)
        
        # Use minimal ANSI escape sequences
        if lines_to_clear > 0:
            # Move up and clear lines efficiently
            clear_sequence = '\033[F\033[2K' * lines_to_clear
            cls._original_write(clear_sequence)
        
        # Reprint from actual start with single write
        outputs = []
        for print_obj in cls._global_prints[actual_start:]:
            output = print_obj.content + print_obj.end
            print_obj._cached_output = output
            outputs.append(output)
        
        if outputs:
            cls._original_write(''.join(outputs))
            cls._original_stdout.flush()
    
    def __call__(self, *args: Any, sep: Optional[str] = None, end: Optional[str] = None) -> None:
        """Update content and reprint."""
        self.args = args
        if sep is not None:
            self.sep = sep
        if end is not None:
            self.end = end
        self.content = self.sep.join(str(arg) for arg in args)
        mutable_print._reprint_from(self.index)
    
    def _update(self) -> None:
        """Internal method to trigger reprint after content change."""
        mutable_print._reprint_from(self.index)
    
    def replace(self, old: str, new: str, count: int = -1) -> 'mutable_print':
        self.content = self.content.replace(old, new, count)
        self._update()
        return self
    
    def append(self, *text: str) -> 'mutable_print':
        self.content += combine_text(*text, separator=" ")
        self._update()
        return self
    
    def prepend(self, *text: str) -> 'mutable_print':
        self.content = combine_text(*text, separator=" ") + self.content
        self._update()
        return self
    
    def clear(self) -> 'mutable_print':
        self.content = ""
        self._update()
        return self
    
    def set(self, *text: str) -> 'mutable_print':
        self.content = combine_text(*text, separator=" ")
        self._update()
        return self
    
    def upper(self) -> 'mutable_print':
        self.content = self.content.upper()
        self._update()
        return self
    
    def lower(self) -> 'mutable_print':
        self.content = self.content.lower()
        self._update()
        return self
    
    def regex_replace(
        self,
        pattern: str | re.Pattern[str],
        replacement: str,
        flags: int = 0
    ) -> 'mutable_print':
        if isinstance(pattern, str):
            pattern = re.compile(pattern, flags)
        self.content = pattern.sub(replacement, self.content)
        self._update()
        return self
    
    def get(self) -> str:
        return self.content
    
    def __str__(self) -> str:
        return self.content
    
    def __repr__(self) -> str:
        return f"mutable_print({self.content!r})"