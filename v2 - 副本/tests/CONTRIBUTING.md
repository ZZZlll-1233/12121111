# 贡献指南

欢迎任何形式的贡献：报告 bug、改进文档、提交代码、回答问题。
第一次参与开源？从标签为 `good first issue` 的 Issue 开始。

## 三种贡献方式

**1. 报告问题**：[提交 Issue](https://gitee.com/YOUR_USER/pystrkit/issues/new)，选模板填写。
**2. 改进文档**：文档错别字、示例不完整，直接提 PR，不需要先开 Issue。
**3. 提交代码**：新功能请先开 Issue 讨论，避免写完被拒——这是对新人的保护，不是门槛。

## 本地环境

```bash
git clone https://gitee.com/YOUR_USER/pystrkit.git
cd pystrkit

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -e ".[dev]"
```

## 提交前必跑

```bash
pytest                    # 全部测试 + doctest
ruff check .              # 静态检查
ruff format --check .     # 格式检查
mypy                      # 类型检查
```

四条全绿再提 PR。CI 会跑同样的检查，红了会被挡下来。

## 代码规范

- **每个公开函数都要写 docstring，且带 doctest 示例**。doctest 会被 pytest 执行，文档不会腐坏。
- **新函数必须有对应测试**，覆盖率低于 90% CI 会失败。
- **公开 API 不得引入第三方依赖**。这是本库的核心约束。
- 类型标注要完整，`mypy` 跑的是 strict 模式。

## 提交信息格式

```
<类型>: <简短描述>

<可选正文>
```

类型：

| 类型 | 用途 |
| --- | --- |
| `feat` | 新功能 |
| `fix` | 修复缺陷 |
| `docs` | 文档改动 |
| `test` | 测试改动 |
| `refactor` | 重构 |
| `perf` | 性能优化 |
| `chore` | 构建/工具链 |

示例：

```
fix: 修正 1.05 转大写时缺失的零

财务规范要求角位为 0 时分位前必须补零，
原实现输出「壹元伍分」，现修正为「壹元零伍分」。
```

## PR 流程

1. 从 `main` 切分支：`git checkout -b feat/xxx`
2. 改动 + 加测试
3. 本地四条命令全绿
4. 推送并提 PR，标题遵循提交信息格式
5. 保持 PR 小而聚焦，一个大 PR 的合并速度通常是三个小 PR 的三分之一

## 行为准则

参与本项目的讨论请遵守 [贡献者行为准则](./CODE_OF_CONDUCT.md)。
