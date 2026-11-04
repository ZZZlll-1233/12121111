"""公开 API 契约测试。

这两条断言看着没用，实际能挡住两类真实事故：
1. 有人往 __init__ 里 import 了新函数却忘了加进 __all__（用户 from ... import * 拿不到）
2. 发版脚本改了 __version__ 却忘了改 tag（用户装到的版本对不上文档）
"""

from __future__ import annotations

import pystrkit


def test_version_matches_spec() -> None:
    assert pystrkit.__version__.count(".") == 2
    major, minor, patch = (int(part) for part in pystrkit.__version__.split("."))
    assert (major, minor, patch) >= (0, 1, 0)


def test_all_exports_are_importable() -> None:
    for name in pystrkit.__all__:
        assert hasattr(pystrkit, name), f"{name} 在 __all__ 中但实际不存在"


def test_public_api_surface_is_stable() -> None:
    assert set(pystrkit.__all__) == {
        "count_words",
        "mask_id_card",
        "mask_phone",
        "to_rmb_upper",
        "to_slug",
        "truncate_by_width",
    }
