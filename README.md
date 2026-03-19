# mutable-print

**Edit printed terminal text after it's already been printed.**

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/mutable-print)](https://pypi.org/project/mutable-print/)

---

## What is mutable-print?

Once you call `print()`, that line is done — you can't touch it. If you want to show a progress bar, a live status, or just update a value in place, you're stuck reprinting the same line over and over, which looks messy.

`mutable-print` fixes that. It gives you a handle to any line you've printed, so you can update, replace, append, clear, or transform it at any point — even after printing more lines below it.

```bash
pip install mutable-print
```

---

## Your first mutable line

```python
from mutable_print import mutable_print

line = mutable_print("Loading...", flush=True)
# ... do some work ...
line("Done!")
```

`mutable_print` works exactly like Python's built-in `print`, except it returns an object you can use to edit the line later. Calling that object like a function replaces the content.

---

## Updating content

### Calling the object directly

The simplest way to update a line — just call it like a function with new content.

```python
line("Processing 3/10...")
line("Processing 7/10...")
line("All done!")
```

You can also change `sep` and `end` at the same time. If you leave them out, the current values are kept.

---

### `line.set(*text)`

Replace the entire content with something new. Equivalent to calling the object directly, but chainable.

```python
line.set("New content here")
```

---

### `line.replace(old, new, count=-1)`

Replace occurrences of a substring inside the current content. By default replaces all of them — pass `count` to limit it.

```python
line.replace("FAILED", "OK")
line.replace("x", "✓", 1)  # only the first one
```

---

### `line.regex_replace(pattern, replacement, flags=0)`

Same idea as `replace`, but with a regex pattern. Supports backreferences and all standard `re` flags.

```python
line.regex_replace(r"\d+", "??")
line.regex_replace(r"(\w+) error", r"\1 warning", flags=re.IGNORECASE)
```

---

## Adding content

### `line.append(*text)`

Adds text to the end of the current content.

```python
line.append(" ✓")
```

---

### `line.prepend(*text)`

Adds text to the beginning of the current content.

```python
line.prepend("[INFO] ")
```

---

## Other operations

### `line.upper()` / `line.lower()`

Converts the current content to uppercase or lowercase.

```python
line.upper()  # "hello world" → "HELLO WORLD"
```

---

### `line.clear()`

Wipes the content entirely — sets it to an empty string.

```python
line.clear()
```

---

### `line.get()`

Returns the current content as a string, without printing anything.

```python
status = line.get()
```

---

## Chaining

All methods except `get()` return the `mutable_print` instance, so you can chain operations together.

```python
line.prepend("[WARN] ").replace("timeout", "slow response").upper()
```

---

## Full API reference

### `mutable_print(*args, sep=" ", end="\n", file=None, flush=False)`

Creates the mutable print object and immediately prints the initial content.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `*args` | `Any` | — | Values to print |
| `sep` | `str` | `" "` | Separator between values |
| `end` | `str` | `"\n"` | String appended at the end |
| `file` | `TextIO` | `sys.stdout` | Output stream |
| `flush` | `bool` | `False` | Whether to flush immediately |

---

### Method summary

| Method | What it does |
|---|---|
| `line(...)` | Replace content and reprint |
| `line.set(*text)` | Replace content (chainable) |
| `line.replace(old, new, count=-1)` | Substring replacement |
| `line.regex_replace(pattern, repl, flags=0)` | Regex replacement |
| `line.append(*text)` | Add to the end |
| `line.prepend(*text)` | Add to the beginning |
| `line.upper()` | Uppercase |
| `line.lower()` | Lowercase |
| `line.clear()` | Wipe content |
| `line.get()` | Return content as string |

---

## How it works

Internally, `mutable-print` keeps a global list of everything that's been printed. When you update a line, it calculates how many lines up that content lives, moves the cursor back using ANSI escape codes (`\033[A`), clears from there, and reprints everything from that point downward.

This is what makes retroactive edits work correctly — even if you've printed ten more lines after the one you're editing, the update lands in the right place and the rest of the output follows cleanly.

Uses only standard Python modules: `sys`, `re`, and `typing`.