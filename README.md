# Mutable Print Documentation

A Python library that allows you to retroactively modify printed content in the terminal using ANSI escape sequences.

## Installation

```bash
pip install mutable-print
```

## Quick Start

```python
from mutable_print import mutable_print

# Create a mutable print
p = mutable_print("Hello, World!")

# Modify it later
p.replace("World", "Python")  # Output updates to "Hello, Python!"
p.append(" How are you?")     # Output updates to "Hello, Python! How are you?"
```

## Features

- **Retroactive Modification**: Change printed content after it's been displayed
- **Method Chaining**: Fluently chain multiple modifications
- **Print Interception**: Optionally intercept all `print()` calls
- **ANSI Escape Sequences**: Uses terminal control codes for real-time updates

## Core API

### `mutable_print`

The main class for creating mutable print objects.

#### Constructor

```python
mutable_print(*args, sep=' ', end='\n', file=None, flush=False)
```

**Parameters:**
- `*args`: Values to print (same as built-in `print()`)
- `sep`: String inserted between values (default: `' '`)
- `end`: String appended after the last value (default: `'\n'`)
- `file`: File object to write to (default: `stdout`)
- `flush`: Whether to forcibly flush the stream (default: `False`)

**Example:**
```python
p = mutable_print("Loading", "data", sep="...", end="...\n")
```

### Modification Methods

All modification methods return `self` for method chaining.

#### `replace(old, new, count=-1)`

Replace occurrences of a substring.

```python
p = mutable_print("Hello World")
p.replace("World", "Universe")  # "Hello Universe"
p.replace("l", "L", count=1)    # "HeLlo Universe"
```

#### `append(*text)`

Append text to the end of the content.

```python
p = mutable_print("Loading")
p.append(".", ".", ".")  # "Loading . . ."
```

#### `prepend(*text)`

Prepend text to the beginning of the content.

```python
p = mutable_print("World")
p.prepend("Hello", " ")  # "Hello  World"
```

#### `set(*text)`

Replace the entire content with new text.

```python
p = mutable_print("Old text")
p.set("Completely", "new", "text")  # "Completely new text"
```

#### `clear()`

Clear the content completely.

```python
p = mutable_print("Remove this")
p.clear()  # ""
```

#### `upper()`

Convert all content to uppercase.

```python
p = mutable_print("hello world")
p.upper()  # "HELLO WORLD"
```

#### `lower()`

Convert all content to lowercase.

```python
p = mutable_print("HELLO WORLD")
p.lower()  # "hello world"
```

#### `regex_replace(pattern, replacement, flags=0)`

Replace content using regular expressions.

```python
import re

p = mutable_print("Error: 404 - Not Found")
p.regex_replace(r'\d+', '500')  # "Error: 500 - Not Found"
p.regex_replace(r'error', 'Warning', flags=re.IGNORECASE)  # "Warning: 500 - Not Found"
```

### Utility Methods

#### `get()`

Get the current content as a string.

```python
p = mutable_print("Hello")
content = p.get()  # "Hello"
```

#### `__call__(*args, sep=' ', end='\n')`

Update the print content (alternative to `set()`).

```python
p = mutable_print("Initial")
p("Updated", "content")  # "Updated content"
```

## Print Interception

Enable global print interception to make all `print()` calls mutable.

### `enable_custom_print()`

Replace the built-in `print()` function with mutable_print.

```python
from mutable_print import enable_custom_print

enable_custom_print()
print("This is now mutable!")  # Returns a mutable_print object
```

### `disable_custom_print()`

Restore the original built-in `print()` function.

```python
from mutable_print import disable_custom_print

disable_custom_print()
print("Back to normal")  # Regular print behavior
```

### `toggle_custom_print()`

Toggle print interception on/off.

```python
from mutable_print import toggle_custom_print

toggle_custom_print()  # Enables if disabled, disables if enabled
```

### `is_custom_print_enabled()`

Check if custom print interception is currently enabled.

```python
from mutable_print import is_custom_print_enabled

if is_custom_print_enabled():
    print("Custom print is active")
```

## Advanced Examples

### Progress Bar

```python
from mutable_print import mutable_print
import time

p = mutable_print("[          ] 0%")

for i in range(1, 11):
    time.sleep(0.2)
    bars = "=" * i
    spaces = " " * (10 - i)
    p.set(f"[{bars}{spaces}] {i * 10}%")

p.set("[==========] 100% Complete!")
```

### Loading Animation

```python
from mutable_print import mutable_print
import time

p = mutable_print("Loading")
dots = ["", ".", "..", "..."]

for _ in range(12):
    for dot in dots:
        p.set(f"Loading{dot}")
        time.sleep(0.2)

p.set("Loading complete!")
```

### Status Updates

```python
from mutable_print import mutable_print

status = mutable_print("Status: Idle")

status.set("Status: Connecting...")
# ... connection code ...
status.set("Status: Connected ✓")

status.set("Status: Processing...")
# ... processing code ...
status.set("Status: Complete ✓")
```

### Method Chaining

```python
from mutable_print import mutable_print

p = mutable_print("hello world")
p.upper().replace("WORLD", "PYTHON").prepend("[INFO] ")
# Result: "[INFO] HELLO PYTHON"
```

### Multiple Mutable Prints

```python
from mutable_print import mutable_print

p1 = mutable_print("Line 1")
p2 = mutable_print("Line 2")
p3 = mutable_print("Line 3")

# Modify any line - all subsequent lines will be reprinted
p1.set("Updated Line 1")  # All three lines reprint
p2.append(" - Modified")  # Lines 2 and 3 reprint
p3.clear()                # Only line 3 reprints
```

## How It Works

The library uses ANSI escape sequences to manipulate the terminal cursor:

1. **Storage**: All mutable prints are stored in a global list with their index
2. **Modification**: When you modify a print, it calculates how many lines need to be reprinted
3. **Reprinting**: The cursor moves up, clears lines, and reprints all content from the modified index onwards

**ANSI Codes Used:**
- `\033[A` - Move cursor up one line
- `\033[2K` - Clear entire line
- `\r` - Move cursor to beginning of line

## Limitations

- **Terminal Support**: Requires a terminal that supports ANSI escape sequences
- **Windows**: Works best on Windows 10+ with modern terminals (Windows Terminal, PowerShell 7+)
- **File Output**: ANSI escape sequences will appear as text when redirecting to files
- **Line Wrapping**: May not work correctly if terminal lines wrap
- **Concurrent Output**: Does not handle output from other sources (threads, subprocesses)

## Requirements

- Python 3.8+
- Terminal with ANSI escape sequence support

## License

MIT License
