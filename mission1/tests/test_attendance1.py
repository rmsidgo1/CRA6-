import pytest
import io
import os
from contextlib import redirect_stdout

import sys

sys.path.append('C:\\PythonProject')
print(sys.path)

from mission1.attendance import show_result


def act(attendance_file, sut):
    buf = io.StringIO()
    with redirect_stdout(buf):
        sut(attendance_file)
        actual = buf.getvalue().rstrip()  # 맨 끝 "\n" 제거
    return actual


def test_빈파일():
    sut = show_result

    attendance_file = "EmptyFile.txt"
    with open(attendance_file, "w") as f:
        pass
    expected = "\nRemoved player\n=============="

    actual = act(attendance_file, sut)

    os.remove(attendance_file)
    assert actual == expected


def test_파일이없을때():
    sut = show_result
    expected = "파일을 찾을 수 없습니다."

    attendance_file = "NotExistsFilename.txt"

    actual = act(attendance_file, sut)

    assert actual == expected


def test_기대한출력_나오는지():
    sut = show_result
    attendance_file = "C:\\PythonProject\\mission1\\tests\\input.txt"
    with open("C:\\PythonProject\\mission1\\tests\\expected.txt", encoding='utf-8') as f:
        expected = f.read()

    actual = act(attendance_file, sut)

    assert actual == expected
