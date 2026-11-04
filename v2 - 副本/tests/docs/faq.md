# 常见问题

## `to_rmb_upper` 为什么用 Decimal？

因为浮点数有精度问题。`0.1 + 0.2` 在 Python 里等于 `0.30000000000000004`，
转成大写会得到「零元叁角整」——角位被吃掉了，财务上直接是错的。

所以内部实现是 `Decimal(str(amount))`，把浮点数先转成字符串再解析，
绕开二进制浮点误差。但注意：**你自己在做加减法时也必须用 Decimal**，
本函数只能保证最后一步不出错。

```python
from decimal import Decimal
from pystrkit import to_rmb_upper

total = Decimal("0.1") + Decimal("0.2")   # 正确
to_rmb_upper(total)                        # 零元叁角整

to_rmb_upper(0.1 + 0.2)                    # 输入已经错了，救不回来
```

## 为什么脱敏函数不抛异常？

脱敏经常用在日志链路。一条脏数据导致整条日志处理抛异常，代价远大于「没脱成」。

如果你需要严格校验，自己加断言：

```python
from pystrkit import mask_phone

result = mask_phone(raw)
assert "*" in result or not raw.isdigit(), "手机号格式异常"
```

## `to_slug` 为什么不支持中文？

转拼音需要 `pypinyin` 之类的库，会破坏「零依赖」这个核心约束。
需要的话在外面处理：

```python
from pypinyin import lazy_pinyin
from pystrkit import to_slug

title = "中文文本处理工具库"
pinyin = "-".join(lazy_pinyin(title))
to_slug(pinyin)     # 'zhong-wen-wen-ben-chu-li-gong-ju-ku'
```

## 截断宽度为什么不用 `len()`？

`len("中文")` 返回 2，因为 Python 的字符串是 Unicode 字符序列。
但在等宽字体下，一个汉字占 2 个 ASCII 字符位。
做终端表格时用 `len()` 算，中文列会全线错位。

`truncate_by_width` 依据 `unicodedata.east_asian_width()` 判断：
`W`（宽）和 `F`（全角）算 2，其余算 1。

## 支持哪些 Python 版本？

3.9 及以上。开发环境测试了 3.9 / 3.11 / 3.13。

## 有依赖吗？

运行时零依赖。开发依赖（pytest、ruff、mypy 等）放在 `[dev]` 可选组里，
不影响使用者。

## 能贡献吗？

能。先读 [贡献者行为准则](https://gitee.com/YOUR_USER/pystrkit/blob/main/CODE_OF_CONDUCT.md)，
然后从 `good first issue` 标签的 Issue 入手。提 PR 前请确保这四条命令全绿：

```bash
pytest && ruff check . && ruff format --check . && mypy
```