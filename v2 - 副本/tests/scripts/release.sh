#!/usr/bin/env bash
# 一键发版：改版本号 -> 跑测试 -> 打标签 -> 推送到 Gitee -> 重建文档站
#
# 用法：
#   bash scripts/release.sh 0.2.0
#
# 前提：已完成实名认证、配置好 SSH 免密、main 分支是最新。

set -euo pipefail

VERSION="${1:-}"

if [[ -z "$VERSION" ]]; then
  echo "用法: bash scripts/release.sh <版本号，例如 0.2.0>"
  exit 1
fi

if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "错误: 版本号必须是 x.y.z 格式，当前为 '$VERSION'"
  exit 1
fi

echo "==> 准备发布 v$VERSION"

# 1. 确认工作区干净，避免把半成品打进去
if [[ -n "$(git status --porcelain)" ]]; then
  echo "错误: 工作区有未提交的改动，请先提交或 stash"
  git status --short
  exit 1
fi

# 2. 切到 main 并同步远端
git checkout main
git pull origin main

# 3. 更新 pyproject.toml 里的版本号（两处：version 和 changelog 链接不用动）
sed -i.bak "s/^version = \".*\"/version = \"$VERSION\"/" pyproject.toml
sed -i.bak "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" src/pystrkit/__init__.py
rm -f pyproject.toml.bak src/pystrkit/__init__.py.bak

# 4. 跑测试，不通过就不发
echo "==> 运行测试"
pytest -q

echo "==> 提交版本变更"
git add pyproject.toml src/pystrkit/__init__.py CHANGELOG.md
git commit -m "release: v$VERSION"

# 5. 打标签并推送
echo "==> 打标签 v$VERSION"
git tag -a "v$VERSION" -m "Release v$VERSION"
git push origin main
git push origin "v$VERSION"

# 6. 重建文档站并推到 pages 分支
echo "==> 重建文档站"
bash scripts/deploy_pages.sh

echo ""
echo "完成。Release 页面: https://gitee.com/YOUR_USER/pystrkit/releases"
echo "剩余手动动作: 在 Releases 页面点「创建 Release」，选择标签 v$VERSION 并粘贴 CHANGELOG 内容。"