import os
import re
import sys
from typing import Any, Callable, List, Optional, Pattern, TextIO, Tuple, Union

if os.name == "nt":
    os.system("")

Record = Tuple[str, Any]


class mutable_print:
    __slots__ = (
        "sep",
        "end",
        "file",
        "flush",
        "content",
        "_managed",
        "_record_index",
        "_cached_output",
    )

    _records: List[Record] = []
    _original_stdout: TextIO = sys.stdout
    _original_write: Optional[Callable[[str], int]] = None
    _intercept_installed: bool = False
    _capture_enabled: bool = True

    class _InterceptedStdout:
        def write(self, text: str) -> int:
            cls = mutable_print
            if text and cls._capture_enabled:
                cls._capture_static_write(text)

            if cls._original_write is None:
                return 0

            return cls._original_write(text)

        def flush(self) -> None:
            mutable_print._original_stdout.flush()

        def __getattr__(self, name: str) -> Any:
            return getattr(mutable_print._original_stdout, name)

    def __init__(
        self,
        *args: Any,
        sep: str = " ",
        end: str = "\n",
        file: Optional[TextIO] = None,
        flush: bool = False,
    ) -> None:
        self.sep = sep
        self.end = end
        self.flush = flush
        self.content = sep.join(str(arg) for arg in args)
        self._managed = False
        self._record_index = -1
        self._cached_output = self._output()

        target_stream = file if file is not None else sys.stdout

        if self._is_stdout_stream(target_stream):
            self._ensure_stdout_intercept()
            self.file = sys.stdout
            self._managed = True
            self._record_index = len(self._records)
            self._records.append(("mutable", self))
            self._write_stdout(self._cached_output, flush=self.flush)
            return

        self.file = target_stream
        self.file.write(self._cached_output)
        if self.flush:
            self.file.flush()

    @classmethod
    def _is_stdout_stream(cls, stream: TextIO) -> bool:
        if cls._intercept_installed:
            return stream is sys.stdout or stream is cls._original_stdout
        return stream is sys.stdout

    @classmethod
    def _ensure_stdout_intercept(cls) -> None:
        if cls._intercept_installed:
            return

        cls._original_stdout = sys.stdout
        cls._original_write = cls._original_stdout.write
        sys.stdout = cls._InterceptedStdout()
        cls._intercept_installed = True

    @classmethod
    def _capture_static_write(cls, text: str) -> None:
        if not text:
            return

        if cls._records and cls._records[-1][0] == "static":
            cls._records[-1] = ("static", cls._records[-1][1] + text)
            return

        cls._records.append(("static", text))

    @classmethod
    def _write_stdout(cls, text: str, flush: bool = False) -> None:
        if cls._original_write is None:
            cls._original_stdout = sys.stdout
            cls._original_write = cls._original_stdout.write

        previous_capture_state = cls._capture_enabled
        cls._capture_enabled = False

        try:
            cls._original_write(text)
        finally:
            cls._capture_enabled = previous_capture_state

        if flush:
            cls._original_stdout.flush()

    def _output(self) -> str:
        return self.content + self.end

    @classmethod
    def _record_output(cls, record: Record, use_cached: bool) -> str:
        kind, payload = record

        if kind == "static":
            return payload

        if use_cached:
            return payload._cached_output

        return payload._output()

    @classmethod
    def _render_from(cls, index: int, use_cached: bool) -> str:
        return "".join(cls._record_output(record, use_cached) for record in cls._records[index:])

    @classmethod
    def _line_start_index(cls, index: int) -> int:
        start_index = index

        while start_index > 0:
            previous_output = cls._record_output(cls._records[start_index - 1], use_cached=True)
            if previous_output.endswith("\n"):
                break
            start_index -= 1

        return start_index

    @staticmethod
    def _line_count(text: str) -> int:
        if not text:
            return 0

        new_line_count = text.count("\n")
        if text.endswith("\n"):
            return new_line_count

        return new_line_count + 1

    @staticmethod
    def _build_clear_sequence(line_count: int) -> str:
        if line_count <= 0:
            return ""

        sequence_parts: List[str] = []

        for line_number in range(line_count):
            sequence_parts.append("\033[2K")
            if line_number < line_count - 1:
                sequence_parts.append("\n")

        if line_count > 1:
            sequence_parts.append("\033[{0}A\r".format(line_count - 1))
        else:
            sequence_parts.append("\r")

        return "".join(sequence_parts)

    @classmethod
    def _sync_cached_outputs(cls, start_index: int) -> None:
        for kind, payload in cls._records[start_index:]:
            if kind == "mutable":
                payload._cached_output = payload._output()

    @classmethod
    def _reprint_from(cls, index: int, flush: bool = True) -> None:
        if index < 0 or index >= len(cls._records):
            return

        start_index = cls._line_start_index(index)
        old_suffix = cls._render_from(start_index, use_cached=True)
        new_suffix = cls._render_from(start_index, use_cached=False)

        if old_suffix:
            lines_up = old_suffix.count("\n")

            if lines_up > 0:
                cls._write_stdout("\033[{0}A\r".format(lines_up))
            else:
                cls._write_stdout("\r")

            cls._write_stdout(cls._build_clear_sequence(cls._line_count(old_suffix)))

        cls._write_stdout(new_suffix, flush=flush)
        cls._sync_cached_outputs(start_index)

    def __call__(self, *args: Any, sep: Optional[str] = None, end: Optional[str] = None) -> None:
        if sep is not None:
            self.sep = sep

        if end is not None:
            self.end = end

        self.content = self.sep.join(str(arg) for arg in args)
        self._update()

    def _update(self) -> None:
        if self._managed:
            self._reprint_from(self._record_index, flush=True)
            return

        output = self._output()
        isatty = getattr(self.file, "isatty", None)

        if callable(isatty) and isatty():
            self.file.write("\r\033[2K" + output)
        else:
            self.file.write(output)

        self.file.flush()
        self._cached_output = output

    def replace(self, old: str, new: str, count: int = -1) -> "mutable_print":
        self.content = self.content.replace(old, new, count)
        self._update()
        return self

    def append(self, *text: str) -> "mutable_print":
        self.content += " ".join(str(part) for part in text)
        self._update()
        return self

    def prepend(self, *text: str) -> "mutable_print":
        self.content = " ".join(str(part) for part in text) + self.content
        self._update()
        return self

    def clear(self) -> "mutable_print":
        self.content = ""
        self._update()
        return self

    def set(self, *text: str) -> "mutable_print":
        self.content = " ".join(str(part) for part in text)
        self._update()
        return self

    def upper(self) -> "mutable_print":
        self.content = self.content.upper()
        self._update()
        return self

    def lower(self) -> "mutable_print":
        self.content = self.content.lower()
        self._update()
        return self

    def regex_replace(
        self,
        pattern: Union[str, Pattern[str]],
        replacement: str,
        flags: int = 0,
    ) -> "mutable_print":
        if isinstance(pattern, str):
            compiled_pattern = re.compile(pattern, flags)
        else:
            compiled_pattern = pattern

        self.content = compiled_pattern.sub(replacement, self.content)
        self._update()
        return self

    def get(self) -> str:
        return self.content

    def __str__(self) -> str:
        return self.content

    def __repr__(self) -> str:
        return "mutable_print({0!r})".format(self.content)
