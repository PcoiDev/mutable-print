from typing import Any, Optional, TextIO, List
import sys
import re
from .core.combine_text import combine_text

class mutable_print:
    __slots__ = ('args', 'sep', 'end', 'file', 'flush', 'content', 'index', 
                 '_cached_output', '_line_start', '_col_start')
    
    _global_prints: List['mutable_print'] = []
    _original_stdout: TextIO = sys.stdout
    _original_write: Optional[Any] = None
    _lines_used: int = 0
    _buffer: List[List[str]] = [[]]
    _cursor_line: int = 0
    _cursor_col: int = 0
    
    def __init__(
        self,
        *args: Any,
        sep: str = ' ',
        end: str = '\n',
        file: Optional[TextIO] = None,
        flush: bool = False
    ) -> None:
        if mutable_print._original_write is None:
            mutable_print._original_write = sys.stdout.write
            mutable_print._setup_intercept()
        
        self.args = args
        self.sep = sep
        self.end = end
        self.file = file or mutable_print._original_stdout
        self.flush = flush
        self.content = sep.join(map(str, args))
        self.index = len(mutable_print._global_prints)
        self._cached_output = ""
        self._line_start = mutable_print._cursor_line
        self._col_start = mutable_print._cursor_col
        
        mutable_print._global_prints.append(self)
        self._print_and_update_buffer()
    
    @classmethod
    def _setup_intercept(cls):
        """Setup stdout interception for regular prints"""
        class InterceptedStdout:
            def write(self, text):
                # For regular prints, update buffer tracking
                if not text or text.startswith('\033['):
                    return cls._original_write(text)
                
                for char in text:
                    if char == '\n':
                        cls._cursor_line += 1
                        cls._cursor_col = 0
                        if cls._cursor_line >= len(cls._buffer):
                            cls._buffer.append([])
                    elif char == '\r':
                        cls._cursor_col = 0
                    else:
                        # Ensure buffer line exists
                        while cls._cursor_line >= len(cls._buffer):
                            cls._buffer.append([])
                        
                        line = cls._buffer[cls._cursor_line]
                        while cls._cursor_col >= len(line):
                            line.append(' ')
                        
                        if cls._cursor_col < len(line):
                            line[cls._cursor_col] = char
                        else:
                            line.append(char)
                        cls._cursor_col += 1
                
                cls._lines_used = max(cls._lines_used, cls._cursor_line + 1)
                return cls._original_write(text)
            
            def flush(self):
                return cls._original_stdout.flush()
            
            def __getattr__(self, name):
                return getattr(cls._original_stdout, name)
        
        sys.stdout = InterceptedStdout()
    
    def _print_and_update_buffer(self) -> None:
        """Print content and update buffer tracking"""
        output = self.content + self.end
        self._cached_output = output
        
        # Store position
        start_line = mutable_print._cursor_line
        start_col = mutable_print._cursor_col
        self._line_start = start_line
        self._col_start = start_col
        
        # Update buffer with our content
        for char in output:
            if char == '\n':
                mutable_print._cursor_line += 1
                mutable_print._cursor_col = 0
                if mutable_print._cursor_line >= len(mutable_print._buffer):
                    mutable_print._buffer.append([])
            else:
                while mutable_print._cursor_line >= len(mutable_print._buffer):
                    mutable_print._buffer.append([])
                
                line = mutable_print._buffer[mutable_print._cursor_line]
                while mutable_print._cursor_col >= len(line):
                    line.append(' ')
                
                if mutable_print._cursor_col < len(line):
                    line[mutable_print._cursor_col] = char
                else:
                    line.append(char)
                mutable_print._cursor_col += 1
        
        mutable_print._lines_used = max(mutable_print._lines_used, mutable_print._cursor_line + 1)
        
        # Write the output
        mutable_print._original_write(output)
        if self.flush:
            mutable_print._original_stdout.flush()
    
    @classmethod
    def _quick_update(cls, obj: 'mutable_print') -> None:
        """Optimized update for a single mutable_print object"""
        new_output = obj.content + obj.end
        old_output = obj._cached_output
        
        # Save cursor position
        saved_line = cls._cursor_line
        saved_col = cls._cursor_col
        
        # Calculate movement needed
        lines_up = saved_line - obj._line_start
        
        # Build single escape sequence for movement
        move_seq = ""
        if lines_up > 0:
            move_seq = f"\033[{lines_up}A"
        elif lines_up < 0:
            move_seq = f"\033[{-lines_up}B"
        
        # Move to column
        if obj._col_start == 0:
            move_seq += "\r"
        else:
            move_seq += f"\r\033[{obj._col_start}C"
        
        # Clear old content and write new
        old_len = len(old_output.replace('\n', ''))
        new_len = len(new_output.replace('\n', ''))
        
        if old_len > new_len:
            # Write new content then clear extra characters
            write_seq = move_seq + new_output.rstrip('\n')
            clear_needed = old_len - new_len
            write_seq += ' ' * clear_needed
            # Move back to where cursor should be after new content
            write_seq += '\b' * clear_needed
            if new_output.endswith('\n'):
                write_seq += '\n'
        else:
            write_seq = move_seq + new_output
        
        # Return cursor in same operation
        if saved_line > obj._line_start:
            write_seq += f"\033[{saved_line - obj._line_start}B"
        
        if saved_col > 0:
            write_seq += f"\r\033[{saved_col}C"
        else:
            write_seq += "\r"
        
        # Write everything in one go
        cls._original_write(write_seq)
        cls._original_stdout.flush()
        
        # Update cached output
        obj._cached_output = new_output
        
        # Update buffer - clear old content first
        temp_line = obj._line_start
        temp_col = obj._col_start
        
        # Clear old content in buffer
        for char in old_output:
            if char == '\n':
                # Clear rest of line
                if temp_line < len(cls._buffer):
                    line = cls._buffer[temp_line]
                    while temp_col < len(line):
                        line[temp_col] = ' '
                        temp_col += 1
                temp_line += 1
                temp_col = 0
            else:
                if temp_line < len(cls._buffer) and temp_col < len(cls._buffer[temp_line]):
                    cls._buffer[temp_line][temp_col] = ' '
                temp_col += 1
        
        # Write new content in buffer
        temp_line = obj._line_start
        temp_col = obj._col_start
        
        for char in new_output:
            if char == '\n':
                temp_line += 1
                temp_col = 0
                if temp_line >= len(cls._buffer):
                    cls._buffer.append([])
            else:
                while temp_line >= len(cls._buffer):
                    cls._buffer.append([])
                
                line = cls._buffer[temp_line]
                while temp_col >= len(line):
                    line.append(' ')
                line[temp_col] = char
                temp_col += 1
    
    def __call__(self, *args: Any, sep: Optional[str] = None, end: Optional[str] = None) -> None:
        """Update content with new values"""
        self.args = args
        if sep is not None:
            self.sep = sep
        if end is not None:
            self.end = end
        self.content = self.sep.join(map(str, args))
        mutable_print._quick_update(self)
    
    def _update(self) -> None:
        """Internal update method"""
        mutable_print._quick_update(self)
    
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