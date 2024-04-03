# -*- coding:utf-8 -*-
# @FileName : __init__.py.py
# @Time : 2024/1/28 16:35
# @Author :fiv
from pathlib import Path

from enum import Enum

PROJECT_PATH = Path(__file__).parent.parent.absolute()


class PATH(Enum):
    DATA_PATH = PROJECT_PATH / "data"
    OUTPUT_PATH = PROJECT_PATH / "output"

    def __truediv__(self, other):
        return self.value / other


def check_exist():
    for path in PATH:
        if not path.value.exists():
            path.value.mkdir(parents=True, exist_ok=True)


check_exist()

# if __name__ == '__main__':
#     for i in PATH:
#         print(i)
#         print(i.value)
#         print(i.name)
#         print(i.__class__)
#         print(i.__class__.__name__)
