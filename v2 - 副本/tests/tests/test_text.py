"""文本处理测试。"""

from __future__ import annotations

import pytest

from pystrkit import count_words, to_slug, truncate_by_width
from pystrkit._text import display_width


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", 0),
        ("abc", 3),
        ("中文", 4),
        ("中a文b", 6),
        ("…", 1),
    ],
)
def test_display_width(text: str, expected: int) -> None:
    assert display_width(text) == expected


@pytest.mark.parametrize(
    ("text", "width", "expected"),
    [
        ("中文文本处理工具库", 6, "中文…"),
        ("hello world", 8, "hello w…"),
        ("中英mix混合", 7, "中英mi…"),
        ("abc", 0, ""),
        ("abc", 1, "…"),
    ],
)
def test_truncate_by_width(text: str, width: int, expected: str) -> None:
    assert truncate_by_width(text, width) == expected


def test_truncate_keeps_short_text_untouched() -> None:
    assert truncate_by_width("短文本", 20) == "短文本"


def test_truncate_never_exceeds_width() -> None:
    for width in range(1, 20):
        result = truncate_by_width("中文abc混合文本示例", width)
        assert display_width(result) <= width


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", 0),
        ("你好, world", 3),
        ("Python 是最好的语言", 7),
        ("！！！", 0),
        ("don't stop", 2),
    ],
)
def test_count_words(text: str, expected: int) -> None:
    assert count_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello, Gitee! 开源 项目", "hello-gitee"),
        ("【2026】年度报告", "2026"),
        ("  Multiple   Spaces  ", "multiple-spaces"),
        ("纯中文标题", ""),
    ],
)
def test_to_slug(text: str, expected: str) -> None:
    assert to_slug(text) == expected


def test_to_slug_respects_max_length() -> None:
    long_text = "a" * 100
    assert len(to_slug(long_text, max_length=10)) == 10
