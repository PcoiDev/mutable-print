from typing import Any, Optional, TextIO, List
import sys
import re
from .core.combine_text import combine_text

class mutable_print:
    """
    A print replacement that allows retroactive modification of printed content.
    
    This class intercepts print statements and stores them in a global list,
    allowing you to modify previously printed content by reprinting from that
    point forward with ANSI escape sequences.
    
    Attributes:
        args: Original arguments passed to the print call
        sep: Separator between arguments
        end: String appended after the last value
        file: File object to write to
        flush: Whether to forcibly flush the stream
        content: The string representation of the print content
        index: Position in the global prints list
    """
    
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
        """
        Initialize a mutable print object.
        
        Args:
            *args: Values to print
            sep: String inserted between values
            end: String appended after the last value
            file: File object to write to (defaults to stdout)
            flush: Whether to forcibly flush the stream
        """
        self.args: tuple[Any, ...] = args
        self.sep: str = sep
        self.end: str = end
        self.file: TextIO = file or mutable_print._original_stdout
        self.flush: bool = flush
        self.content: str = sep.join(str(arg) for arg in args)
        self.index: int = len(mutable_print._global_prints)
        mutable_print._global_prints.append(self)
        self._print_initial()
    
    def _print_initial(self) -> None:
        """Print the initial content to stdout."""
        output: str = self.content + self.end
        mutable_print._original_write(output)
        if self.flush:
            mutable_print._original_stdout.flush()
    
    def _get_line_count(self) -> int:
        """
        Calculate how many lines this print statement occupies.
        
        Returns:
            Number of lines occupied by this print
        """
        if not self.content:
            return 1 if self.end == '\n' else 0
        return self.content.count('\n') + (1 if self.end == '\n' else 0)
    
    @classmethod
    def _count_lines(cls, start_index: int) -> int:
        """
        Count total lines from a given index to the end.
        
        Args:
            start_index: Starting index in the global prints list
            
        Returns:
            Total number of lines from start_index onwards
        """
        return sum(p._get_line_count() for p in cls._global_prints[start_index:])
    
    @classmethod
    def _reprint_all_from(cls, start_index: int) -> None:
        """
        Reprint all content from a given index onwards.
        
        Uses ANSI escape sequences to move cursor up and clear lines,
        then reprints all content from the specified index.
        
        Args:
            start_index: Index to start reprinting from
        """
        total_lines: int = cls._count_lines(start_index)
        
        buffer: List[str] = []
        buffer.extend(['\033[A\033[2K'] * total_lines)
        buffer.append('\r')
        
        for print_obj in cls._global_prints[start_index:]:
            buffer.append(print_obj.content + print_obj.end)
        
        cls._original_write(''.join(buffer))
        cls._original_stdout.flush()
    
    def __call__(self, *args: Any, sep: str = ' ', end: str = '\n') -> None:
        """
        Update the print content and reprint.
        
        Args:
            *args: New values to print
            sep: New separator between values
            end: New string appended after the last value
        """
        self.args = args
        self.sep = sep
        self.end = end
        self.content = sep.join(str(arg) for arg in args)
        mutable_print._reprint_all_from(self.index)
    
    def replace(self, old: str, new: str, count: int = -1) -> 'mutable_print':
        """
        Replace occurrences of a substring in the content.
        
        Args:
            old: Substring to replace
            new: Replacement string
            count: Maximum number of occurrences to replace (-1 for all)
            
        Returns:
            Self for method chaining
        """
        self.content = self.content.replace(old, new, count)
        mutable_print._reprint_all_from(self.index)
        return self
    
    def append(self, *text: str) -> 'mutable_print':
        """
        Append text to the end of the content.
        
        Args:
            *text: Text strings to append
            
        Returns:
            Self for method chaining
        """
        self.content += combine_text(*text, separator=" ")
        mutable_print._reprint_all_from(self.index)
        return self
    
    def prepend(self, *text: str) -> 'mutable_print':
        """
        Prepend text to the beginning of the content.
        
        Args:
            *text: Text strings to prepend
            
        Returns:
            Self for method chaining
        """
        self.content = combine_text(*text, separator=" ") + self.content
        mutable_print._reprint_all_from(self.index)
        return self
    
    def clear(self) -> 'mutable_print':
        """
        Clear the content completely.
        
        Returns:
            Self for method chaining
        """
        self.content = ""
        mutable_print._reprint_all_from(self.index)
        return self
    
    def set(self, *text: str) -> 'mutable_print':
        """
        Replace the entire content with new text.
        
        Args:
            *text: Text strings to set as new content
            
        Returns:
            Self for method chaining
        """
        self.content = combine_text(*text, separator=" ")
        mutable_print._reprint_all_from(self.index)
        return self
    
    def upper(self) -> 'mutable_print':
        """
        Convert all content to uppercase.
        
        Returns:
            Self for method chaining
        """
        self.content = self.content.upper()
        mutable_print._reprint_all_from(self.index)
        return self
    
    def lower(self) -> 'mutable_print':
        """
        Convert all content to lowercase.
        
        Returns:
            Self for method chaining
        """
        self.content = self.content.lower()
        mutable_print._reprint_all_from(self.index)
        return self
    
    def regex_replace(
        self,
        pattern: str | re.Pattern[str],
        replacement: str,
        flags: int = 0
    ) -> 'mutable_print':
        """
        Replace content using regular expressions.
        
        Args:
            pattern: Regular expression pattern to match
            replacement: Replacement string (can include backreferences)
            flags: Optional regex flags (e.g., re.IGNORECASE)
            
        Returns:
            Self for method chaining
        """
        self.content = re.sub(pattern, replacement, self.content, flags=flags)
        mutable_print._reprint_all_from(self.index)
        return self
    
    def get(self) -> str:
        """
        Get the current content as a string.
        
        Returns:
            Current content string
        """
        return self.content
    
    def __str__(self) -> str:
        """
        String representation of the content.
        
        Returns:
            Current content string
        """
        return self.content
    
    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        
        Returns:
            Representation showing the class name and content
        """
        return f"mutable_print({self.content!r})"