# API 参考

## 金额

### `to_rmb_upper(amount)`

把金额转成人民币中文大写。

```python
def to_rmb_upper(amount: Decimal | int | float | str) -> str
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `amount` | `Decimal \| int \| float \| str` | 金额，四种类型都支持，推荐传字符串 |

**返回**：中文大写字符串。

**异常**：无法解析为金额、或金额超出 16 位整数范围时抛 `ValueError`。

**行为细节**：

- 先转 `Decimal` 再量化到分，四舍五入采用 `ROUND_HALF_UP`
- 角位为 0 而分位不为 0 时补「零」：`1.05` → `壹元零伍分`
- 分位为 0 时以「整」结尾：`100` → `壹佰元整`
- 元位为 0 且角分都不为 0 时输出「零元」：`0.05` → `零元零伍分`
- 负数前缀「负」：`-88.80` → `负捌拾捌元捌角整`

```python
to_rmb_upper("1234.56")     # '壹仟贰佰叁拾肆元伍角陆分'
to_rmb_upper("0.005")       # '零元零壹分'（四舍五入到分）
to_rmb_upper("1" + "0"*20)  # ValueError: 超出支持范围
```

## 脱敏

### `mask_phone(value, keep_head=3, keep_tail=4)`

手机号脱敏。格式不合法时**原样返回**。

```python
def mask_phone(value: str, keep_head: int = 3, keep_tail: int = 4) -> str
```

| 参数 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `value` | `str` | — | 手机号，11 位，1 开头且第二位为 3-9 |
| `keep_head` | `int` | `3` | 保留开头位数 |
| `keep_tail` | `int` | `4` | 保留结尾位数 |

```python
mask_phone("13812345678")                              # '138****5678'
mask_phone("138-1234-5678")                            # '138****5678'
mask_phone("13812345678", keep_head=0, keep_tail=4)    # '*******5678'
mask_phone("12345")                                    # '12345'
```

### `mask_id_card(value, keep_head=6, keep_tail=4)`

身份证脱敏，支持末位 `X`。格式不合法时原样返回。

```python
def mask_id_card(value: str, keep_head: int = 6, keep_tail: int = 4) -> str
```

```python
mask_id_card("110101199003071234")   # '110101********1234'
mask_id_card("11010119900307123X")   # '110101********123X'
```

!!! note "为什么脱敏不抛异常"
    脱敏通常跑在日志和展示路径上，一条脏数据不该把整个请求打断。
    但金额转换必须抛——写错金额的后果是发票作废，不能静默吞掉。

## 文本

### `truncate_by_width(text, width, suffix="…")`

按显示宽度截断。全角字符（中文）按 2 计，其余按 1 计。

```python
def truncate_by_width(text: str, width: int, suffix: str = "…") -> str
```

- `width <= 0` 时返回空串
- 文本本身就短于 `width` 时原样返回
- 宽度放不下 `suffix` 时退化为直接截断 `suffix` 本身
- **保证返回值宽度永远不超过 `width`**

```python
truncate_by_width("中文文本处理工具库", 6)   # '中文…'
truncate_by_width("hello world", 8)         # 'hello w…'
truncate_by_width("abc", 0)                 # ''
truncate_by_width("abc", 1)                 # '…'
```

### `count_words(text)`

中英混排字数统计。汉字算 1 字，英文单词（含缩写）算 1 词，标点不计数。

```python
def count_words(text: str) -> int
```

```python
count_words("你好, world")         # 3
count_words("Python 是最好的语言")   # 7
count_words("don't stop")         # 2
count_words("！！！")               # 0
```

### `to_slug(text, max_length=60)`

生成 URL 友好的 slug。中文会被移除，需外部做拼音转换。

```python
def to_slug(text: str, max_length: int = 60) -> str
```

```python
to_slug("Hello, Gitee! 开源 项目")   # 'hello-gitee'
to_slug("【2026】年度报告")           # '2026'
to_slug("a" * 100, max_length=10)    # 'aaaaaaaaaa'
```

### `display_width(text)`

计算显示宽度。这是内部函数，但偶尔会用到，所以导出了。

```python
def display_width(text: str) -> int
```

```python
display_width("abc")     # 3
display_width("中文")     # 4
```

## 模块信息

```python
import pystrkit

pystrkit.__version__    # '0.1.0'
pystrkit.__all__        # 公开导出的函数名列表
```