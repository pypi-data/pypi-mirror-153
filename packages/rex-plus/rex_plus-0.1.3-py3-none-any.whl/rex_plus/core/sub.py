# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Holbos.Deng
# Github: https://github.com/holbos-deng
# Email: 2292861292@qq.com
# CreateDate: 2022/6/6 11:55
# Description:
import re


def sub(pattern: str, repl_list: list, string: str):
    matched_list = re.findall(pattern, string)

    if matched_list:
        max_index_of_replace_list = len(repl_list) - 1

        if isinstance(matched_list[0], (tuple, list)):
            for _matched_list in matched_list:
                for i, m in enumerate(_matched_list):
                    if m and i <= max_index_of_replace_list:
                        string = string.replace(m, repl_list[i], 1)
        else:
            for i, m in enumerate(matched_list):
                if m and i <= max_index_of_replace_list:
                    string = string.replace(m, repl_list[i], 1)
    return string
