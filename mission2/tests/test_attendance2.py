import pytest
import io
import os
from contextlib import redirect_stdout

import sys

sys.path.append('C:\\PythonProject')

from mission2.attendance import AttendanceSystem


def act(attendance_file, sut):
    buf = io.StringIO()
    with redirect_stdout(buf):
        sut.show_result(attendance_file)
        actual = buf.getvalue().rstrip()  # 맨 끝 "\n" 제거
    return actual


def test_빈파일():
    sut = AttendanceSystem()
    attendance_file = "C:\\PythonProject\\mission2\\tests\\EmptyFile.txt"
    with open(attendance_file, "w") as f:
        pass

    expected = "\nRemoved player\n=============="

    actual = act(attendance_file, sut)

    os.remove(attendance_file)
    assert actual == expected


def test_파일이없을때():
    sut = AttendanceSystem()
    attendance_file = "NotExistsFilename.txt"
    expected = "파일을 찾을 수 없습니다."

    actual = act(attendance_file, sut)

    assert actual == expected


def test_기대한출력_나오는지():
    sut = AttendanceSystem()
    attendance_file = "C:\\PythonProject\\mission2\\tests\\input.txt"
    with open("C:\\PythonProject\\mission2\\tests\\expected.txt", encoding='utf-8') as f:
        expected = f.read()

    actual = act(attendance_file, sut)

    assert actual == expected
