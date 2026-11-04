"""人民币大写转换测试。

用例挑选原则：每组都覆盖一类边界。
- 0 与「整」的收尾
- 亿元级跨段
- 中间跨段补零（1 亿零 1）
- 角为 0 分不为 0 的补零
- 负数
- 四舍五入到分
"""

from __future__ import annotations

from decimal import Decimal

import pytest

from pystrkit import to_rmb_upper


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        (0, "零元整"),
        ("0.00", "零元整"),
        (1, "壹元整"),
        ("10", "壹拾元整"),
        ("100", "壹佰元整"),
        ("1000", "壹仟元整"),
        ("1234.56", "壹仟贰佰叁拾肆元伍角陆分"),
        ("1.05", "壹元零伍分"),
        ("0.05", "零元零伍分"),
        ("0.50", "零元伍角整"),
        ("0.5", "零元伍角整"),
        ("-88.80", "负捌拾捌元捌角整"),
        ("10001", "壹万零壹元整"),
        ("100000000", "壹亿元整"),
        ("100000001", "壹亿零壹元整"),
        ("123456789.09", "壹亿贰仟叁佰肆拾伍万陆仟柒佰捌拾玖元零玖分"),
        (Decimal("0.005"), "零元零壹分"),
    ],
)
def test_to_rmb_upper(amount: object, expected: str) -> None:
    assert to_rmb_upper(amount) == expected  # type: ignore[arg-type]


def test_rejects_garbage_input() -> None:
    with pytest.raises(ValueError, match="无法解析为金额"):
        to_rmb_upper("不是金额")


def test_rejects_overflow() -> None:
    with pytest.raises(ValueError, match="超出支持范围"):
        to_rmb_upper("1" + "0" * 20)
