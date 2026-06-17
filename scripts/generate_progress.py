#!/usr/bin/env python3
"""
generate_progress.py — 根据 metadata/problems.yaml 生成 docs/progress.md 刷题进度页。

用法：
    python scripts/generate_progress.py [--solved ID1,ID2,...]

--solved 参数传入已完成的题目 ID 列表（逗号分隔）。
默认全部未做。

示例：
    python scripts/generate_progress.py --solved 1,11,15,20,21
"""

import sys
import argparse
from pathlib import Path
from collections import defaultdict

METADATA_PATH = Path(__file__).parent.parent / "metadata" / "problems.yaml"
PROGRESS_PATH = Path(__file__).parent.parent / "docs" / "progress.md"


def load_problems() -> list[dict]:
    """加载题目数据。"""
    try:
        import yaml
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("problems", [])
    except ImportError:
        print("警告: 未安装 pyyaml，跳过进度页生成")
        print("安装方法: pip install pyyaml")
        sys.exit(1)


def generate_progress(problems: list[dict], solved_ids: set[int]) -> str:
    """生成进度页内容。"""
    total = len(problems)
    solved_count = len(solved_ids & set(p.get("id", 0) for p in problems))
    rate = f"{solved_count / total * 100:.1f}%" if total > 0 else "0%"

    # 按难度统计
    diff_stats = defaultdict(lambda: {"total": 0, "solved": 0})
    for p in problems:
        pid = p.get("id", 0)
        diff = p.get("difficulty", "Unknown")
        diff_stats[diff]["total"] += 1
        if pid in solved_ids:
            diff_stats[diff]["solved"] += 1

    lines = [
        "# 刷题进度",
        "",
        f"> 总进度：{solved_count} / {total} ({rate})",
        "",
        "## 难度分布",
        "",
        "| Difficulty | Total | Solved | Rate |",
        "| ---------- | ----- | ------ | ---- |",
    ]

    for diff in ["Easy", "Medium", "Hard"]:
        stats = diff_stats.get(diff, {"total": 0, "solved": 0})
        diff_rate = f"{stats['solved'] / stats['total'] * 100:.1f}%" if stats["total"] > 0 else "0%"
        lines.append(f"| {diff} | {stats['total']} | {stats['solved']} | {diff_rate} |")

    lines.extend([
        "",
        "## 已完成",
        "",
    ])

    # 按 ID 排序
    sorted_problems = sorted(problems, key=lambda p: p.get("id", 0))
    solved_problems = [p for p in sorted_problems if p.get("id", 0) in solved_ids]

    if solved_problems:
        for p in solved_problems:
            pid = p.get("id", 0)
            slug = p.get("slug", "")
            title = p.get("title", "")
            diff = p.get("difficulty", "")
            emoji = {"Easy": "✅", "Medium": "🟡", "Hard": "🔴"}.get(diff, "📝")
            lines.append(f"- {emoji} [{title}](/problems/{pid:04d}-{slug})")
    else:
        lines.append("> 暂无已完成题目，加油！")

    lines.extend([
        "",
        "## 待完成",
        "",
    ])

    unsolved = [p for p in sorted_problems if p.get("id", 0) not in solved_ids]
    if unsolved:
        for p in unsolved[:30]:  # 只显示前30道
            pid = p.get("id", 0)
            slug = p.get("slug", "")
            title = p.get("title", "")
            lines.append(f"- ⬜ [{title}](/problems/{pid:04d}-{slug})")

        if len(unsolved) > 30:
            lines.append(f"- ... 还有 {len(unsolved) - 30} 题")

    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="生成刷题进度页")
    parser.add_argument("--solved", default="", help="已做题目的 ID 列表，逗号分隔")
    args = parser.parse_args()

    if not METADATA_PATH.exists():
        print(f"错误: 找不到元数据文件 {METADATA_PATH}")
        sys.exit(1)

    problems = load_problems()
    if not problems:
        print("错误: 未找到任何题目数据")
        sys.exit(1)

    # 解析已做题
    solved_ids = set()
    if args.solved:
        for sid in args.solved.split(","):
            sid = sid.strip()
            if sid.isdigit():
                solved_ids.add(int(sid))

    print(f"题目总数: {len(problems)}")
    print(f"已做: {len(solved_ids)}")

    content = generate_progress(problems, solved_ids)
    PROGRESS_PATH.write_text(content, encoding="utf-8")
    print(f"已生成 {PROGRESS_PATH}")
    print("完成！")


if __name__ == "__main__":
    main()
