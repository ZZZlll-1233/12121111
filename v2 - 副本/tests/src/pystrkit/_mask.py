"""国内业务常见的敏感信息脱敏。

设计取舍：**格式不合法时原样返回，而不是抛异常**。
原因是脱敏多用在日志和展示路径上，抛异常会把一条正常的业务日志打断，
代价远大于「没脱成」。如果你希望严格校验，外面自己加断言。
"""

from __future__ import annotations

import re

# 中国大陆手机号：1 开头，第二位 3-9，共 11 位
_PHONE_RE = re.compile(r"^1[3-9]\d{9}$")
# 二代身份证：18 位，末位可为数字或 X
_ID_CARD_RE = re.compile(r"^\d{17}[\dXx]$")


def _mask_middle(text: str, keep_head: int, keep_tail: int) -> str:
    """保留头尾，中间替换为等长星号。"""
    if keep_head + keep_tail >= len(text):
        # 保留位数已经盖住全文，退化为只保留头部，避免切片重叠出 bug
        return text[:keep_head] + "*"

    head = text[:keep_head]
    tail = text[-keep_tail:] if keep_tail > 0 else ""
    stars = "*" * (len(text) - keep_head - keep_tail)
    return head + stars + tail


def mask_phone(value: str, keep_head: int = 3, keep_tail: int = 4) -> str:
    """手机号脱敏。格式不合法时原样返回。

    >>> mask_phone("13812345678")
    '138****5678'
    >>> mask_phone("138-1234-5678")
    '138****5678'
    >>> mask_phone("12345")
    '12345'
    """
    text = value.strip()
    # 兼容带分隔符的写法
    compact = text.replace("-", "").replace(" ", "")
    if not _PHONE_RE.match(compact):
        return value
    return _mask_middle(compact, keep_head, keep_tail)


def mask_id_card(value: str, keep_head: int = 6, keep_tail: int = 4) -> str:
    """身份证号脱敏。格式不合法时原样返回。

    >>> mask_id_card("110101199003071234")
    '110101********1234'
    >>> mask_id_card("11010119900307123X")
    '110101********123X'
    """
    text = value.strip()
    if not _ID_CARD_RE.match(text):
        return value
    return _mask_middle(text, keep_head, keep_tail)
