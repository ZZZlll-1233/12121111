"""人民币金额转中文大写。

财务/发票/合同的硬性要求。这里采用中国人民银行规定的标准写法：
- 数字：零壹贰叁肆伍陆柒捌玖
- 单位：拾佰仟万亿，元角分
- 角位为 0 但分位不为 0 时补「零」，如 1.05 → 壹元零伍分
- 分位为 0 时以「整」结尾，如 100.50 → 壹佰元伍角整

金额一律先转成 Decimal 再量化到分，**不直接用 float 参与运算**，
否则 0.1 + 0.2 那类误差会实打实出现在发票金额上。
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

_DIGITS = "零壹贰叁肆伍陆柒捌玖"
_PLACES = ("", "拾", "佰", "仟")
_SECTIONS = ("", "万", "亿", "万亿")

_MAX_SECTIONS = len(_SECTIONS)


def _section_to_upper(value: int) -> str:
    """把 0~9999 转大写，末尾的零会被吞掉。"""
    result = ""
    for index, char in enumerate(str(value).zfill(4)):
        digit = int(char)
        place = _PLACES[3 - index]
        if digit == 0:
            # 内部零只补一次，且末尾不补
            if result and not result.endswith("零"):
                result += "零"
        else:
            result += _DIGITS[digit] + place
    return result.rstrip("零")


def _int_to_upper(value: int) -> str:
    """把非负整数转中文大写（不含「元」）。"""
    if value == 0:
        return "零"

    sections: list[int] = []
    rest = value
    while rest > 0:
        sections.append(rest % 10000)
        rest //= 10000

    if len(sections) > _MAX_SECTIONS:
        raise ValueError(f"金额超出支持范围（最大 {10 ** (4 * _MAX_SECTIONS) - 1}）")

    result = ""
    for index in range(len(sections) - 1, -1, -1):
        section = sections[index]
        if section == 0:
            continue
        # 本段不足 4 位（如 1 亿零 1 中的「1」），需要在前面补零
        if result and section < 1000:
            result += "零"
        result += _section_to_upper(section) + _SECTIONS[index]
    return result


def to_rmb_upper(amount: Decimal | int | float | str) -> str:
    """把金额转成人民币中文大写。

    支持 int / float / str / Decimal 四种入参；字符串入参最安全（无浮点误差）。

    >>> to_rmb_upper("1234.56")
    '壹仟贰佰叁拾肆元伍角陆分'
    >>> to_rmb_upper(100)
    '壹佰元整'
    >>> to_rmb_upper("1.05")
    '壹元零伍分'
    >>> to_rmb_upper("0.50")
    '零元伍角整'
    >>> to_rmb_upper("-88.80")
    '负捌拾捌元捌角整'
    """
    try:
        value = Decimal(str(amount))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"无法解析为金额：{amount!r}") from exc

    # 量化到分，四舍五入（财务口径常用 ROUND_HALF_UP）
    value = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    cents = int(value * 100)

    prefix = ""
    if cents < 0:
        prefix = "负"
        cents = -cents

    yuan, remainder = divmod(cents, 100)
    jiao, fen = divmod(remainder, 10)

    result = prefix
    if yuan > 0 or (jiao == 0 and fen == 0):
        result += _int_to_upper(yuan) + "元"

    if jiao == 0 and fen == 0:
        return result + "整"

    result += "零元" if yuan == 0 else ""
    if jiao > 0:
        result += _DIGITS[jiao] + "角"
    else:
        # 角位为 0 但分位不为 0，必须补零：1.05 → 壹元零伍分
        result += "零"

    if fen > 0:
        result += _DIGITS[fen] + "分"
    else:
        result += "整"

    return result
