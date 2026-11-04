# pystrkit

[![Gitee Stars](https://gitee.com/YOUR_USER/pystrkit/badge/star.svg?theme=white)](https://gitee.com/YOUR_USER/pystrkit/stargazers)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![CI](https://gitee.com/YOUR_USER/pystrkit/badges/master/build.svg)](https://gitee.com/YOUR_USER/pystrkit)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen.svg)](./tests)

> 零依赖的中文文本处理工具库。人民币大写、手机号脱敏、宽度截断、混排计数，拿来就能用。

---

## 30 秒上手

```python
from pystrkit import to_rmb_upper, mask_phone, truncate_by_width

to_rmb_upper("1234.56")        # '壹仟贰佰叁拾肆元伍角陆分'
mask_phone("13812345678")      # '138****5678'
truncate_by_width("中文文本", 6)  # '中文…'
```

就这些。不需要配置、不需要初始化、不需要读文档才能跑通第一行。

## 为什么还要造一个

这些功能每个项目都要写一遍，而且每次都写得不太一样：

- **人民币大写**：网上随便抄的版本，`1.05` 输出「壹元伍分」，财务直接打回来（标准写法是「壹元零伍分」）。
- **脱敏**：大多数实现会抛异常，用在日志上等于给自己埋雷。
- **截断**：用 `len()` 算中文长度，终端表格里中文列全线错位。

pystrkit 把这三类坑一次性填平，并且**零第三方依赖**——这一点决定了它能直接进任何项目，包括那些对依赖审查很严的政企环境。

## 安装

```bash
pip install pystrkit
```

从源码安装：

```bash
git clone https://gitee.com/YOUR_USER/pystrkit.git
cd pystrkit
pip install -e .
```

## 快速开始

```python
from pystrkit import (
    count_words,
    mask_id_card,
    mask_phone,
    to_rmb_upper,
    to_slug,
    truncate_by_width,
)

# 人民币金额转大写（支持 int / float / str / Decimal，推荐传字符串避开浮点误差）
to_rmb_upper("1234.56")   # '壹仟贰佰叁拾肆元伍角陆分'
to_rmb_upper(100)         # '壹佰元整'
to_rmb_upper("1.05")      # '壹元零伍分'
to_rmb_upper("-88.80")    # '负捌拾捌元捌角整'

# 脱敏（格式非法时原样返回，不会抛异常）
mask_phone("13812345678")          # '138****5678'
mask_id_card("110101199003071234") # '110101********1234'

# 按显示宽度截断（中文按 2 个宽度算）
truncate_by_width("中文文本处理工具库", 6)  # '中文…'
truncate_by_width("hello world", 8)        # 'hello w…'

# 中英混排字数统计
count_words("Python 是最好的语言")  # 7

# URL slug
to_slug("Hello, Gitee! 开源 项目")  # 'hello-gitee'
```

## API 一览

| 函数 | 说明 | 非法输入行为 |
| --- | --- | --- |
| `to_rmb_upper(amount)` | 人民币金额转中文大写 | 抛 `ValueError` |
| `mask_phone(value, keep_head=3, keep_tail=4)` | 手机号脱敏 | 原样返回 |
| `mask_id_card(value, keep_head=6, keep_tail=4)` | 身份证脱敏 | 原样返回 |
| `truncate_by_width(text, width, suffix="…")` | 按显示宽度截断 | 返回空串 |
| `count_words(text)` | 中英混排字数统计 | 返回 0 |
| `to_slug(text, max_length=60)` | 生成 URL slug | 返回空串 |

> **为什么脱敏不抛异常？** 脱敏通常跑在日志和展示路径上，一条脏数据不该把整个请求打断。
> 但金额转换必须抛——写错金额的后果是发票作废，不能静默吞掉。

## 典型场景

**发票/合同金额大写**

```python
from decimal import Decimal

from pystrkit import to_rmb_upper

total = Decimal("0.1") + Decimal("0.2")   # Decimal('0.3')，不会是 0.30000000000000004
print(to_rmb_upper(total))               # 零元叁角整
```

**日志脱敏**

```python
import logging

from pystrkit import mask_id_card, mask_phone


def safe(text: str) -> str:
    return mask_id_card(mask_phone(text))


logging.info("用户 %s 提交了订单", safe("13812345678"))
```

**终端表格对齐**

```python
from pystrkit import truncate_by_width

rows = [("张三", "北京市朝阳区"), ("Alice", "Shanghai")]
for name, city in rows:
    print(f"{truncate_by_width(name, 8):<8} | {truncate_by_width(city, 16)}")
```

## 文档与示例

- 完整文档：<https://YOUR_USER.gitee.io/pystrkit/>
- 可运行示例：[`examples/demo.py`](./examples/demo.py)

## 参与贡献

先读 [CONTRIBUTING.md](./CONTRIBUTING.md)。第一次贡献推荐从 `good first issue` 标签的 Issue 入手。

```bash
git clone https://gitee.com/YOUR_USER/pystrkit.git
cd pystrkit
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## 许可证

[Apache-2.0](./LICENSE)。你可以自由使用、修改、商用，只需保留版权声明。
