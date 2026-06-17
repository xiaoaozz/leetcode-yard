#!/usr/bin/env python3
"""
generate_sidebar.py — 根据 metadata/problems.yaml 自动生成 docs/.vitepress/config.ts 的 sidebar 配置。

用法：
    python scripts/generate_sidebar.py
"""

import sys
import os
import re
from pathlib import Path

METADATA_PATH = Path(__file__).parent.parent / "metadata" / "problems.yaml"
CONFIG_PATH = Path(__file__).parent.parent / "docs" / ".vitepress" / "config.mts"


def parse_yaml_problems(path: Path) -> list[dict]:
    """解析 YAML 中的 problems 列表（轻量解析，不依赖 pyyaml）。"""
    try:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("problems", [])
    except ImportError:
        print("警告: 未安装 pyyaml，尝试轻量解析...")
        return _parse_yaml_lite(path)


def _parse_yaml_lite(path: Path) -> list[dict]:
    """轻量 YAML 解析器，用于没有 pyyaml 的环境。"""
    problems = []
    current = {}
    current_tags = []
    in_tags = False

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.rstrip()
            if not stripped or stripped.startswith("#"):
                continue

            indent = len(line) - len(line.lstrip())

            if stripped.strip() == "problems:":
                continue

            if indent == 2 and stripped.strip().startswith("- id:"):
                if current and "id" in current:
                    if current_tags:
                        current["tags"] = current_tags
                    problems.append(current)
                current = {}
                current_tags = []
                in_tags = False
                val = stripped.split(":", 1)[1].strip()
                current["id"] = int(val)

            elif indent == 4 and in_tags:
                if stripped.strip().startswith("- "):
                    current_tags.append(stripped.strip()[2:].strip())
                else:
                    in_tags = False
                    if current_tags:
                        current["tags"] = current_tags

            elif indent == 4 and stripped.strip().startswith("tags:"):
                in_tags = True

            elif indent == 4 and ":" in stripped:
                in_tags = False
                if current_tags:
                    current["tags"] = current_tags
                    current_tags = []
                key, val = stripped.strip().split(":", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if val.isdigit():
                    val = int(val)
                current[key] = val

        if current and "id" in current:
            if current_tags:
                current["tags"] = current_tags
            problems.append(current)

    return problems


def generate_sidebar(problems: list[dict]) -> str:
    """生成 config.ts 中的 sidebar 配置。"""
    # 按 ID 排序
    problems.sort(key=lambda p: p.get("id", 0))

    # 生成 problem sidebar 项
    problem_items = []
    for p in problems:
        pid = p.get("id", 0)
        slug = p.get("slug", "")
        title = p.get("title", "")
        difficulty = p.get("difficulty", "")
        emoji = {"Easy": "✅", "Medium": "🟡", "Hard": "🔴"}.get(difficulty, "📝")

        problem_items.append(
            f'      {{ text: "{emoji} {pid:04d} - {title}", link: "/problems/{pid:04d}-{slug}" }},'
        )

    sidebar = f"""import {{ defineConfig }} from 'vitepress'

export default defineConfig({{
  title: 'LeetCode Top150',
  description: '多语言题解 · 标签驱动 · 自动生成',
  lang: 'zh-CN',

  ignoreDeadLinks: true,

  themeConfig: {{
    nav: [
      {{ text: '首页', link: '/' }},
      {{ text: '题解', link: '/problems/0001-two-sum' }},
      {{ text: '路线', link: '/roadmap' }},
      {{ text: '进度', link: '/progress' }},
    ],

    sidebar: {{
      '/problems/': [
        {{
          text: '题解',
          collapsed: false,
          items: [
{chr(10).join(problem_items)},
          ],
        }},
      ],
      '/tags/': [
        {{
          text: '标签导航',
          collapsed: false,
          items: [
            {{ text: 'Array', link: '/tags/array' }},
            {{ text: 'Hash Table', link: '/tags/hash-table' }},
            {{ text: 'Linked List', link: '/tags/linked-list' }},
            {{ text: 'Tree', link: '/tags/tree' }},
            {{ text: 'Graph', link: '/tags/graph' }},
            {{ text: 'DFS', link: '/tags/dfs' }},
            {{ text: 'BFS', link: '/tags/bfs' }},
            {{ text: 'Heap', link: '/tags/heap' }},
            {{ text: 'Greedy', link: '/tags/greedy' }},
            {{ text: 'DP', link: '/tags/dp' }},
            {{ text: 'Backtracking', link: '/tags/backtracking' }},
          ],
        }},
      ],
    }},

    socialLinks: [
      {{ icon: 'github', link: 'https://github.com/zhaoaolin/leetcode-yard' }},
    ],

    footer: {{
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026 zhaoaolin',
    }},

    search: {{
      provider: 'local',
    }},

    lastUpdated: true,
  }},

  markdown: {{
    theme: {{
      light: 'github-light',
      dark: 'github-dark-dimmed',
    }},
  }},
}})
"""
    return sidebar


def main():
    if not METADATA_PATH.exists():
        print(f"错误: 找不到元数据文件 {METADATA_PATH}")
        sys.exit(1)

    problems = parse_yaml_problems(METADATA_PATH)
    if not problems:
        print("错误: 未找到任何题目数据")
        sys.exit(1)

    print(f"读取到 {len(problems)} 道题目")

    sidebar = generate_sidebar(problems)
    CONFIG_PATH.write_text(sidebar, encoding="utf-8")
    print(f"已生成 {CONFIG_PATH}")
    print("完成！")


if __name__ == "__main__":
    main()
