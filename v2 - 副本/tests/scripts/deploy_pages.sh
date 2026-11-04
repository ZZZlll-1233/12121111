#!/usr/bin/env bash
# 构建文档站并推送到 gitee pages 分支
#
# 前提：Gitee Pages 服务已开启，分支设为 pages，首页为 index.html

set -euo pipefail

echo "==> 构建文档"
pip install -q ".[docs]"
mkdocs build --strict

# pages 分支必须保留一个 .nojekyll 文件，否则部分静态服务器会忽略下划线开头的目录
touch site/.nojekyll

echo "==> 推送 pages 分支"
git add -f site/
git commit -m "docs: 更新文档站 ($(date +%Y-%m-%d))" || echo "文档无变化，跳过提交"
git push origin HEAD:pages

echo "==> 完成，稍等 1-2 分钟后访问 https://YOUR_USER.gitee.io/pystrkit/"