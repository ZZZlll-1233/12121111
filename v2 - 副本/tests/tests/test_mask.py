"""脱敏测试。

重点测「非法输入原样返回」这条契约——它决定了这个函数能不能安全地
用在日志链路里。
"""

from __future__ import annotations

import pytest

from pystrkit import mask_id_card, mask_phone


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("13812345678", "138****5678"),
        ("138-1234-5678", "138****5678"),
        (" 13812345678 ", "138****5678"),
        ("15900001111", "159****1111"),
    ],
)
def test_mask_phone(value: str, expected: str) -> None:
    assert mask_phone(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("110101199003071234", "110101********1234"),
        ("11010119900307123X", "110101********123X"),
    ],
)
def test_mask_id_card(value: str, expected: str) -> None:
    assert mask_id_card(value) == expected


@pytest.mark.parametrize(
    "value",
    ["", "12345", "23812345678", "abcdefghijk", "1101011990030712"],
)
def test_invalid_phone_returns_original(value: str) -> None:
    assert mask_phone(value) == value


@pytest.mark.parametrize("value", ["", "1234", "abcdefghijklmnopqr", "11010119900307123"])
def test_invalid_id_card_returns_original(value: str) -> None:
    assert mask_id_card(value) == value


def test_custom_keep_length() -> None:
    assert mask_phone("13812345678", keep_head=0, keep_tail=4) == "*******5678"
