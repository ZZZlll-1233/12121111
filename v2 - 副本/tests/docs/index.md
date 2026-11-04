# pystrkit

零依赖的中文文本处理工具库。

## 30 秒上手

```python
from pystrkit import to_rmb_upper, mask_phone, truncate_by_width

to_rmb_upper("1234.56")         # '壹仟贰佰叁拾肆元伍角陆分'
mask_phone("13812345678")       # '138****5678'
truncate_by_width("中文文本", 6)   # '中文…'
```

## 核心特性

<div class="grid cards" markdown>

- **零第三方依赖**

    只有 Python 3.9+ 标准库。可以直接进任何项目，包括依赖审查严格的政企环境。

- **完整类型标注**

    通过 mypy strict 检查，附带 `py.typed`，你的编辑器能自动补全参数类型。

- **文档即测试**

    所有 docstring 里的示例都会被 pytest 执行。文档不会腐坏。

</div>

## 安装

```bash
pip install pystrkit
```

## 下一步

- [快速开始](quickstart.md) —— 5 分钟跑通全部功能
- [API 参考](api.md) —— 每个函数的参数与边界行为
- [常见问题](faq.md) —— 已知限制与踩坑