import pytest
import io
from contextlib import redirect_stdout

from mission1.attendance import show_grade


def test_기대한출력_나오는지():
    sut = show_grade

    with open("expected.txt", encoding='utf-8') as f:
        expected = f.read()

    buf = io.StringIO()
    with redirect_stdout(buf):
        sut("input.txt")
        actual = buf.getvalue()

    assert actual == expected
