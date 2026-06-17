# LeetCode Top150

## Progress

| Difficulty | Total | Solved |
| ---------- | ----- | ------ |
| Easy       | 50    | 0      |
| Medium     | 80    | 0      |
| Hard       | 20    | 0      |

> 总进度：0 / 150 (0%)

## About

本仓库记录 [LeetCode Top 150](https://leetcode.com/studytop/) 刷题过程，特点：

- **按 Tag 组织**：所有题目按标签维度分类，方便针对性练习
- **多语言题解**：Java / Go / Python / C++ / Rust / TypeScript 六种语言
- **单一数据源**：`metadata/problems.yaml` 是唯一数据源，标签页和进度页自动生成
- **静态站点**：VitePress + GitHub Pages 自动部署

## Language Support

- Java
- Go
- Python
- C++
- Rust
- TypeScript

## Tag Navigation

<!-- tags-nav-start -->

- [Array](/tags/array)
- [Hash Table](/tags/hash-table)
- [Linked List](/tags/linked-list)
- [Tree](/tags/tree)
- [Graph](/tags/graph)
- [Dynamic Programming](/tags/dp)
- [Greedy](/tags/greedy)
- [Heap](/tags/heap)
- [Backtracking](/tags/backtracking)

<!-- tags-nav-end -->

## Structure

```
leetcode-top150/
├── docs/              # VitePress 站点源码
│   ├── problems/      # 题目题解 (MD)
│   ├── tags/          # 标签页 (自动生成)
│   └── .vitepress/    # VitePress 配置
├── solutions/         # 多语言代码实现
├── metadata/          # 唯一数据源 (YAML)
└── scripts/           # 自动化脚本
```

## Quick Start

```bash
# 安装依赖
npm install

# 本地开发
npm run dev

# 构建
npm run build
```

## Auto-Generated Pages

以下页面由 `scripts/` 下的脚本自动生成，**不要手动编辑**：

- `docs/progress.md` — 刷题进度统计
- `docs/tags/*.md` — 各标签题目列表
- `docs/index.md` — 站点首页统计

生成命令：

```bash
python scripts/generate_tags.py
python scripts/generate_progress.py
python scripts/generate_sidebar.py
```
