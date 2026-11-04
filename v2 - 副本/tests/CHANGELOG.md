# 更新日志

本文件遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 规范，
版本号遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)。

## [未发布]

### 待办

- [ ] 邮箱脱敏
- [ ] 银行卡号脱敏
- [ ] 姓名脱敏（姓保留、名打码）

## [0.1.0] - 2026-10-20

首个公开版本。

### 新增

- `to_rmb_upper()`：人民币金额转中文大写，支持亿级金额、负数、四舍五入到分
- `mask_phone()`：手机号脱敏，兼容 `-` 和空格分隔写法
- `mask_id_card()`：身份证脱敏，末位 `X` 正常保留
- `truncate_by_width()`：按显示宽度截断，中文按 2 宽度计
- `count_words()`：中英混排字数统计
- `to_slug()`：生成 URL 友好的 slug

### 说明

- 公开 API 零第三方依赖，仅要求 Python 3.9+
- 通过 mypy strict 检查，附带 `py.typed` 标记

[未发布]: https://gitee.com/YOUR_USER/pystrkit/compare/v0.1.0...HEAD
[0.1.0]: https://gitee.com/YOUR_USER/pystrkit/releases/tag/v0.1.0
