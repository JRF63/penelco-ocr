import os
import datetime

import pytest

from ocr.ocr import NoticeType, Notice
from PIL import Image

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(TESTS_DIR, 'data')

def create_notice(notice_type: NoticeType, index: int):
    dir_name = ""
    match notice_type:
        case NoticeType.NGCP:
            dir_name = "ngcp"
        case NoticeType.PENELCO_1:
            dir_name = "penelco_1"
        case NoticeType.PENELCO_2:
            dir_name = "penelco_2"

    file_name = os.path.join(DATA_DIR, dir_name, f"{index}.jpg")
    image = Image.open(file_name)
    return Notice(image)

@pytest.fixture(scope='session')
def test_notice_ngcp_0():
    return create_notice(NoticeType.NGCP, 0)

@pytest.fixture(scope='session')
def test_notice_penelco_1_0():
    return create_notice(NoticeType.PENELCO_1, 0)

@pytest.fixture(scope='session')
def test_notice_penelco_2_0():
    return create_notice(NoticeType.PENELCO_2, 0)

def test_notice_type_ngcp_0(test_notice_ngcp_0: Notice):
    assert test_notice_ngcp_0.notice_type == NoticeType.NGCP

def test_notice_type_penelco_1_0(test_notice_penelco_1_0: Notice):
    assert test_notice_penelco_1_0.notice_type == NoticeType.PENELCO_1

def test_notice_type_penelco_2_0(test_notice_penelco_2_0: Notice):
    assert test_notice_penelco_2_0.notice_type == NoticeType.PENELCO_2

def test_date_ngcp_0(test_notice_ngcp_0: Notice):
    assert test_notice_ngcp_0.get_date() == datetime.date(2023, 9, 17)

def test_date_penelco_1_0(test_notice_penelco_1_0: Notice):
    assert test_notice_penelco_1_0.get_date() == datetime.date(2023, 9, 1)

def test_date_penelco_2_0(test_notice_penelco_2_0: Notice):
    assert test_notice_penelco_2_0.get_date() == datetime.date(2023, 9, 16)

def test_time_ngcp_0(test_notice_ngcp_0: Notice):
    assert test_notice_ngcp_0.get_time() == [(datetime.time(7, 0), datetime.time(19, 0))]

def test_time_penelco_1_0(test_notice_penelco_1_0: Notice):
    assert test_notice_penelco_1_0.get_time() == [(datetime.time(9, 0), datetime.time(16, 0))]

def test_time_penelco_2_0(test_notice_penelco_2_0: Notice):
    assert test_notice_penelco_2_0.get_time() == [(datetime.time(8, 30), datetime.time(15, 30))]