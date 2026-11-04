# 快速开始

## 安装

```bash
pip install pystrkit
```

从源码安装（想参与开发时用这个）：

```bash
git clone https://gitee.com/YOUR_USER/pystrkit.git
cd pystrkit
pip install -e ".[dev]"
```

## 一、人民币金额转大写

财务、发票、合同场景刚需。

```python
from pystrkit import to_rmb_upper

to_rmb_upper("1234.56")        # '壹仟贰佰叁拾肆元伍角陆分'
to_rmb_upper(100)              # '壹佰元整'
to_rmb_upper("1.05")           # '壹元零伍分'  ← 角位为 0 时补零
to_rmb_upper("-88.80")         # '负捌拾捌元捌角整'
to_rmb_upper("100000001")      # '壹亿零壹元整'
```

!!! tip "金额计算请用字符串或 Decimal"
    `to_rmb_upper(0.1 + 0.2)` 会得到 `零元叁角整` 而不是 `0.30000000000000004`，
    因为内部用 `Decimal(str(amount))` 转换。但如果你是**先算再加**，
    务必自己用 `Decimal` 算：`Decimal("0.1") + Decimal("0.2")`。

## 二、敏感信息脱敏

```python
from pystrkit import mask_id_card, mask_phone

mask_phone("13812345678")           # '138****5678'
mask_phone("138-1234-5678")         # '138****5678'  自动去掉分隔符
mask_id_card("110101199003071234")  # '110101********1234'

# 格式非法时原样返回，不抛异常
mask_phone("12345")                 # '12345'
```

自定义保留位数：

```python
mask_phone("13812345678", keep_head=0, keep_tail=4)   # '*******5678'
```

## 三、按显示宽度截断

`len("中文")` 是 2，但在等宽字体下占 4 个字符位。排版时请用这个函数。

```python
from pystrkit import truncate_by_width

truncate_by_width("中文文本处理工具库", 6)   # '中文…'
truncate_by_width("hello world", 8)         # 'hello w…'
truncate_by_width("短文本", 20)               # '短文本'（没超长，原样返回）
```

终端表格对齐：

```python
rows = [("张三", "北京市朝阳区望京街道"), ("Alice", "Shanghai")]
for name, address in rows:
    print(f"{truncate_by_width(name, 8):<8} | {truncate_by_width(address, 16)}")
```

输出：

```text
张三       | 北京市朝阳区望…
Alice    | Shanghai
```

## 四、中英混排字数统计

```python
from pystrkit import count_words

count_words("你好, world")            # 3
count_words("Python 是最好的语言")     # 7  ← 6 个汉字 + 1 个英文单词
count_words("don't stop")            # 2  ← 缩写算一个词
```

## 五、URL slug

```python
from pystrkit import to_slug

to_slug("Hello, Gitee! 开源 项目")   # 'hello-gitee'
to_slug("【2026】年度报告")           # '2026'
```

!!! warning "中文会被移除"
    本库刻意不做拼音转换（那需要额外依赖）。如果标题是中文，
    请在外部先过一遍 `pypinyin` 再调用本函数。