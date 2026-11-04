"""pytest 全局 fixture。

这里只做一件事：每个用例前后清空宽度缓存。
因为 _text 模块里的缓存是模块级全局状态，不清的话用例之间会互相污染，
表现为「单独跑通过、一起跑偶发失败」——这类 bug 极难查，提前防掉。
"""

from __future__ import annotations

from typing import Iterator

import pytest


@pytest.fixture(autouse=True)
def _clear_width_cache() -> Iterator[None]:
    from pystrkit._text import _WIDTH_CACHE

    _WIDTH_CACHE.clear()
    yield
    _WIDTH_CACHE.clear()
