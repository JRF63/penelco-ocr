from ocr.ocr import Notice, NoticeType
from PIL import Image

fp = "tests/data/penelco_1/0.jpg"
# fp = "tests/data/ngcp/0.jpg"
notice = Notice(Image.open(fp))
# print(notice.get_date())
print(notice.get_time())

fp = "tests/data/ngcp/1.jpg"
notice = Notice(Image.open(fp))
print(notice.get_time())

fp = "tests/data/ngcp/0.jpg"
notice = Notice(Image.open(fp))
print(notice.get_time())

fp = "tests/data/penelco_2/0.jpg"
notice = Notice(Image.open(fp))
print(notice.get_time())

# 5:30AM TO 7:30AM and 5:45PM TO 6:00PM

# def split(s, comments=False, posix=True):
#     """Split the string *s* using shell-like syntax."""
#     if s is None:
#         import warnings
#         warnings.warn("Passing None for 's' to shlex.split() is deprecated.",
#                       DeprecationWarning, stacklevel=2)
#     lex = shlex(s, posix=posix)
#     lex.whitespace_split = True
#     if not comments:
#         lex.commenters = ''
#     return list(lex)