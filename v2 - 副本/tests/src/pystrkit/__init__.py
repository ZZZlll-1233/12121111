"""pystrkit —— 零依赖的中文文本处理工具库。

开箱即用的几个小工具，覆盖国内业务里最常见的文本处理场景：

- 人民币金额转中文大写（财务/发票/合同场景刚需）
- 手机号、身份证号脱敏（日志脱敏、前端展示）
- 按显示宽度截断（中英混排排版、终端输出对齐）
- 中英混排字数统计（内容平台字数限制）
- URL slug 生成（文章路由、文件名规范化）

设计约束：**零第三方依赖** + **完整类型标注**，可以直接扔进任何项目。
"""

from __future__ import annotations

from ._mask import mask_id_card, mask_phone
from ._money import to_rmb_upper
from ._text import count_words, to_slug, truncate_by_width

__version__ = "0.1.0"

__all__ = [
    "count_words",
    "mask_id_card",
    "mask_phone",
    "to_rmb_upper",
    "to_slug",
    "truncate_by_width",
]
