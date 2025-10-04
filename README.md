# mutable-print

Edit printed terminal text using ANSI escape codes.

## Why Mutable Print?

Traditional `print()` writes output that cannot be changed once printed.
`mutable-print` fixes that you can **modify**, **replace**, **append**, **clear**, or **transform** text after it’s been printed.

Perfect for:
- **Dynamic CLI output**: progress bars, live status updates, etc.
- **Retroactive edits**: fix or adjust lines even after more output follows.
- **Readable terminals**: no messy reprints or repeated lines.
- **Rich text operations**: prepend, append, regex replacement, upper/lower transforms.

All achieved using ANSI escape sequences to move the cursor and redraw content.

## Installation

```bash
pip install mutable-print
```

## Usage (API Overview)

### `mutable_print(*args: Any, sep: str = " ", end: str = "\n", file: Optional[TextIO] = None, flush: bool = False) -> mutable_print`

Creates a **mutable print object**, prints the initial content immediately, and returns a handle to modify it later.

```python
from mutable_print import mutable_print

line = mutable_print("Loading...", flush=True)
line("Done!")  # Update the same printed line
```

#### Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `*args` | `Any` | — | Values to print |
| `sep` | `str` | `" "` | Separator between values |
| `end` | `str` | `"\n"` | String appended at the end |
| `file` | `TextIO` | `sys.stdout` | Output stream |
| `flush` | `bool` | `False` | Whether to flush immediately |

#### Returns

A `mutable_print` instance that can be updated or transformed.

---

### `__call__(*args: Any, sep: str = " ", end: str = "\n") -> None`

Update the content and **reprint** from this line onward.

```python
line("Processing...", sep=" ", end="\n")
```

#### Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `*args` | `Any` | — | New values to print |
| `sep` | `str` | `" "` | Separator |
| `end` | `str` | `"\n"` | End string |

---

### `replace(old: str, new: str, count: int = -1) -> mutable_print`

Replace all (or a limited number of) occurrences of a substring in the current content.

```python
line.replace("fail", "success", 1)
```

#### Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `old` | `str` | — | Substring to replace |
| `new` | `str` | — | Replacement text |
| `count` | `int` | `-1` | Max occurrences (`-1` for all) |

---

### `append(*text: str) -> mutable_print`

Append text to the **end** of the content.

```python
line.append("...done")
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `*text` | `str` | Text strings to append |

---

### `prepend(*text: str) -> mutable_print`

Prepend text to the **beginning** of the content.

```python
line.prepend("[INFO]")
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `*text` | `str` | Text strings to prepend |

---

### `clear() -> mutable_print`

Clear the current content (sets it to an empty string).

```python
line.clear()
```

---

### `set(*text: str) -> mutable_print`

Replace the entire content with new text.

```python
line.set("New content")
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `*text` | `str` | Text strings to set as new content |

---

### `upper() -> mutable_print`

Convert the current content to **uppercase**.

```python
line.upper()
```

---

### `lower() -> mutable_print`

Convert the current content to **lowercase**.

```python
line.lower()
```

---

### `regex_replace(pattern: str | re.Pattern[str], replacement: str, flags: int = 0) -> mutable_print`

Perform a **regular expression** substitution on the content.

```python
line.regex_replace(r"\d+", "42")
```

#### Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `pattern` | `str` \| `re.Pattern` | — | Regex pattern |
| `replacement` | `str` | — | Replacement string (supports backrefs) |
| `flags` | `int` | `0` | Regex flags (e.g. `re.IGNORECASE`) |

---

### `get() -> str`

Retrieve the current content.

```python
text = line.get()
```

---

### `__str__() -> str`

String representation of the current content. Called automatically by `str(line)`.

---

### `__repr__() -> str`

Developer-friendly representation of the object:

```python
mutable_print('Your content here')
```

# Examples

1. [Basic Update](https://github.com/PcoiDev/mutable-print/blob/main/examples/basic-update.py)
2. [Clean and Efficient Loading](https://github.com/PcoiDev/mutable-print/blob/main/examples/loading-dots.py)
3. [Replace Text](https://github.com/PcoiDev/mutable-print/blob/main/examples/replace.py)
4. [Append / Prepend](https://github.com/PcoiDev/mutable-print/blob/main/examples/append-preend.py)
5. [Clearing and Retrieving Content](https://github.com/PcoiDev/mutable-print/blob/main/examples/clear.py)
6. [Colored Text](https://github.com/PcoiDev/mutable-print/blob/main/examples/colors.py)

## How it works?

Internally, mutable-print:
- Keeps a **global list** of all printed lines.
- Calculates the cursor position relative to past prints.
- Moves the cursor up using `\033[A` and clears lines with `\033[2K`.
- Reprints from the updated index to maintain correct order.

This enables **retroactive edits** even after printing additional lines.

## Credits

Developed with ❤️ by [PcoiDev](https://pcoi.dev)
Uses only standard Python modules (`sys`, `re`, `typing`).

## License

This project is licensed under the [`MIT License`](https://github.com/PcoiDev/rich-style/blob/main/LICENSE).