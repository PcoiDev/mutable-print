# Mutable Print Documentation

A Python library that allows you to retroactively modify printed content in the terminal using ANSI escape sequences.

## Installation

```bash
pip install mutable-print
```

## Credits

Created and maintained by the mutable-print development team.

## License

This project is licensed under the MIT License.

## Overview

`mutable_print` is a replacement for Python's built-in `print()` function that stores printed content and allows you to modify it after it has been displayed. This is particularly useful for creating dynamic terminal UIs, progress bars, and loading animations.

## Basic Usage

## API Reference

### Constructor

```python
mutable_print(
    *args: Any,
    sep: str = ' ',
    end: str = '\n',
    file: Optional[TextIO] = None,
    flush: bool = False
) -> mutable_print
```

Creates a new mutable print object with the same signature as the built-in `print()` function.

**Parameters:**
- `*args: Any` - Values to print
- `sep: str` - String inserted between values (default: `' '`)
- `end: str` - String appended after the last value (default: `'\n'`)
- `file: Optional[TextIO]` - File object to write to (default: `sys.stdout`)
- `flush: bool` - Whether to forcibly flush the stream (default: `False`)

**Returns:** `mutable_print` instance

### Methods

#### `__call__(*args: Any, sep: str = ' ', end: str = '\n') -> None`

Update the print content with new values.

```python
mutable = mutable_print("Hello")
mutable("World")
```

**Parameters:**
- `*args: Any` - New values to print
- `sep: str` - New separator between values (default: `' '`)
- `end: str` - New string appended after the last value (default: `'\n'`)

#### `replace(old: str, new: str, count: int = -1) -> mutable_print`

Replace occurrences of a substring in the content.

```python
mutable = mutable_print("Hello World")
mutable.replace("World", "Python")
```

**Parameters:**
- `old: str` - Substring to replace
- `new: str` - Replacement string
- `count: int` - Maximum number of occurrences to replace (default: `-1` for all)

**Returns:** `mutable_print` - Self for method chaining

#### `append(*text: str) -> mutable_print`

Append text to the end of the content.

```python
mutable = mutable_print("Hello")
mutable.append("World", "!")
```

**Parameters:**
- `*text: str` - Text strings to append

**Returns:** `mutable_print` - Self for method chaining

#### `prepend(*text: str) -> mutable_print`

Prepend text to the beginning of the content.

```python
mutable = mutable_print("World")
mutable.prepend("Hello", " ")
```

**Parameters:**
- `*text: str` - Text strings to prepend

**Returns:** `mutable_print` - Self for method chaining

#### `clear() -> mutable_print`

Clear the content completely.

```python
mutable = mutable_print("Hello World")
mutable.clear()
```

**Returns:** `mutable_print` - Self for method chaining

#### `set(*text: str) -> mutable_print`

Replace the entire content with new text.

```python
mutable = mutable_print("Old text")
mutable.set("New", "text")
```

**Parameters:**
- `*text: str` - Text strings to set as new content

**Returns:** `mutable_print` - Self for method chaining

#### `upper() -> mutable_print`

Convert all content to uppercase.

```python
mutable = mutable_print("hello")
mutable.upper()
```

**Returns:** `mutable_print` - Self for method chaining

#### `lower() -> mutable_print`

Convert all content to lowercase.

```python
mutable = mutable_print("HELLO")
mutable.lower()
```

**Returns:** `mutable_print` - Self for method chaining

#### `regex_replace(pattern: str | re.Pattern[str], replacement: str, flags: int = 0) -> mutable_print`

Replace content using regular expressions.

```python
mutable = mutable_print("Hello123World456")
mutable.regex_replace(r'\d+', '-')
```

**Parameters:**
- `pattern: str | re.Pattern[str]` - Regular expression pattern to match (string or compiled pattern)
- `replacement: str` - Replacement string (can include backreferences)
- `flags: int` - Optional regex flags (e.g., `re.IGNORECASE`) (default: `0`)

**Returns:** `mutable_print` - Self for method chaining

#### `get() -> str`

Get the current content as a string.

```python
mutable = mutable_print("Hello World")
content = mutable.get()
```

**Returns:** `str` - Current content string

## Method Chaining

All modifier methods return `self`, allowing you to chain multiple operations:

```python
mutable = mutable_print("hello world")
mutable.upper().replace("WORLD", "PYTHON").append("!")
```

## How It Works

`mutable_print` uses ANSI escape sequences to move the cursor up and clear lines, then reprints all content from the modified point forward. This creates the illusion of modifying previously printed content while maintaining compatibility with standard terminal output.

## Limitations

- Works best in terminals that support ANSI escape sequences
- May not work properly in non-interactive environments or certain IDEs
- Performance may degrade with a large number of mutable print objects