# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Holbos.Deng
# Github: https://github.com/holbos-deng
# Email: 2292861292@qq.com
# CreateDate: 2022/6/6 11:56
# Description: 
import re
from typing import Tuple, List


class Math:
    __index_tuple = (0, 0)
    __text = None

    def __init__(self, reg, text):
        self.__index_tuple = reg
        self.__text = text

    def span(self) -> Tuple[int, int]:
        return self.__index_tuple

    def text(self) -> str:
        return self.__text

    def __repr__(self):
        return f"<rex_plus.Match object; span={self.span()}, match='{self.text()}'>"


def search_all(pattern: str, s: str) -> List[Math]:
    result_all = []
    len_s, cs = len(s), s
    last_index = 0
    while s:
        r = re.search(pattern, s)
        if r:
            current_index_tuple = r.span()

            current_index_tuple = (current_index_tuple[0] + last_index, current_index_tuple[1] + last_index)
            last_index = current_index_tuple[1]

            _match = Math(current_index_tuple, r.group())
            result_all.append(_match)
            s = cs[current_index_tuple[1]:]
        else:
            s = None
    return result_all or None
