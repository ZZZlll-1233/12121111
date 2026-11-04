"""pystrkit 功能演示。

直接跑：

    python examples/demo.py

这个文件同时充当「活的文档」：README 里的示例就是从这里复制过去的，
所以只要它还能跑，README 就不会过时。
"""

from __future__ import annotations

from decimal import Decimal

from pystrkit import (
    count_words,
    mask_id_card,
    mask_phone,
    to_rmb_upper,
    to_slug,
    truncate_by_width,
)


def demo_money() -> None:
    print("== 人民币大写 ==")
    samples: list[Decimal | int | float | str] = [
        "1234.56",
        100,
        "1.05",
        "0.05",
        "100000001",
        "-88.80",
        Decimal("0.005"),
    ]
    for amount in samples:
        print(f"  {str(amount):>12} -> {to_rmb_upper(amount)}")


def demo_mask() -> None:
    print("\n== 脱敏 ==")
    print(f"  手机号     {mask_phone('13812345678')}")
    print(f"  带分隔符   {mask_phone('138-1234-5678')}")
    print(f"  身份证     {mask_id_card('110101199003071234')}")
    print(f"  非法输入   {mask_phone('12345')}  (原样返回，不抛异常)")


def demo_text() -> None:
    print("\n== 文本处理 ==")
    title = "中文文本处理工具库"
    for width in (4, 6, 8, 20):
        print(f"  截断到 {width:>2} 宽度: {truncate_by_width(title, width)}")
    print(f"  混排字数: {count_words('Python 是最好的语言')}")
    print(f"  slug:     {to_slug('Hello, Gitee! 开源 项目')}")


def demo_table() -> None:
    print("\n== 终端表格对齐 ==")
    rows = [("张三", "北京市朝阳区望京街道"), ("Alice", "Shanghai"), ("李四", "广州市天河区")]
    header = f"{'姓名':<8} | {'地址'}"
    print(f"  {header}")
    print(f"  {'-' * 8}-+-{'-' * 16}")
    for name, address in rows:
        print(f"  {truncate_by_width(name, 8):<8} | {truncate_by_width(address, 16)}")


def main() -> None:
    demo_money()
    demo_mask()
    demo_text()
    demo_table()


if __name__ == "__main__":
    main()
