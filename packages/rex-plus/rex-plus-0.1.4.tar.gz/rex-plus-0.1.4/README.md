📦 rex-plus (for humans)
=======================

Plus version of re

Installation
-----

```bash
pip install -i https://mirrors.aliyun.com/pypi/simple/ --extra-index-url https://pypi.org/simple/ rex-plus
```

Example
-----

```python
import rex_plus
# 正则替换
# Partial replacement according to regular expression
rex_plus.sub('(限行)灯', ['线型'], '卧室有一盏限行灯')
# output: '卧室有一盏线型灯'
rex_plus.sub('(我是).*(限行)灯', ['卧室', '线型'], '卧室有一盏限行灯')
# output: 卧室有一盏线型灯
rex_plus.sub('(?:卧室)的(限行)灯', ['线型'], '卧室的限行灯')
# output: 卧室的线型灯
rex_plus.sub('(?:(我是)的)(限行)灯', ['卧室', '线型'], '卧室的限行灯')
# output: 卧室的线型灯
# 查询所有匹配项，并返回对应的index和text
rex_plus.search_all(r"\d", "__a1bb2ccc3")
# output: [<rex_plus.Match object; span=(3, 4), text='1'>, <rex_plus.Match object; span=(6, 7), text='2'>, <rex_plus.Match object; span=(10, 11), text='3'>]
```

To Do
-----

-   Be the best version of you.


More Resources
--------------

-   [rex-plus] on github.com
-   [Official Python Packaging User Guide](https://packaging.python.org)
-   [The Hitchhiker's Guide to Packaging]
-   [Cookiecutter template for a Python package]

License
-------

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any means.

  [rex-plus]: https://github.com/holbos-deng/rex_plus
  [PyPi]: https://docs.python.org/3/distutils/packageindex.html
  [Twine]: https://pypi.python.org/pypi/twine
  [image]: https://farm1.staticflickr.com/628/33173824932_58add34581_k_d.jpg
  [What is setup.py?]: https://stackoverflow.com/questions/1471994/what-is-setup-py
  [The Hitchhiker's Guide to Packaging]: https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/creation.html
  [Cookiecutter template for a Python package]: https://github.com/audreyr/cookiecutter-pypackage
