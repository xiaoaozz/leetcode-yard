#!/usr/bin/env python3
"""
sync_problem_stats.py — 同步题目统计数据（通过率等），并检查缺失语言实现。

功能：
1. 检查哪些题目缺少某些语言的实现
2. 输出统计报告
3. 可选：从 LeetCode API 获取最新通过率（需要 leetcode-cli 或手动输入）

用法：
    python scripts/sync_problem_stats.py [--check-missing] [--update-rates]
"""

import sys
import json
from pathlib import Path
from collections import defaultdict

METADATA_PATH = Path(__file__).parent.parent / "metadata" / "problems.yaml"
SOLUTIONS_DIR = Path(__file__).parent.parent / "solutions"
LANGUAGES = ["java", "golang", "python", "cpp", "rust", "typescript"]

# 语言对应的文件扩展名
EXT_MAP = {
    "java": ".java",
    "golang": ".go",
    "python": ".py",
    "cpp": ".cpp",
    "rust": ".rs",
    "typescript": ".ts",
}


def load_problems() -> list[dict]:
    """加载题目数据。"""
    try:
        import yaml
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("problems", [])
    except ImportError:
        print("警告: 未安装 pyyaml")
        sys.exit(1)


def check_missing_solutions(problems: list[dict]) -> list[dict]:
    """检查哪些题目缺少某些语言的实现。"""
    missing_list = []

    for p in problems:
        pid = p.get("id", 0)
        slug = p.get("slug", "")

        # 尝试多种可能的文件名格式
        possible_names = []

        # snake_case
        possible_names.append(f"{pid:04d}_{slug}")

        # CamelCase (Java 风格)
        parts = slug.split("-")
        camel = "".join(w.capitalize() for w in parts)
        possible_names.append(f"{pid:04d}_{camel}")

        has_any = False
        missing_langs = []

        for lang in LANGUAGES:
            ext = EXT_MAP[lang]
            lang_dir = SOLUTIONS_DIR / lang

            found = False
            for name in possible_names:
                filepath = lang_dir / f"{name}{ext}"
                if filepath.exists():
                    found = True
                    break

            if not found:
                missing_langs.append(lang)

            if found:
                has_any = True

        if has_any and missing_langs:
            missing_list.append({
                "id": pid,
                "slug": slug,
                "title": p.get("title", ""),
                "missing": missing_langs,
            })

    return missing_list


def generate_report(problems: list[dict]) -> str:
    """生成统计报告。"""
    total = len(problems)

    # 按难度统计
    diff_count = defaultdict(int)
    tag_count = defaultdict(int)
    for p in problems:
        diff_count[p.get("difficulty", "Unknown")] += 1
        for tag in p.get("tags", []):
            tag_count[tag] += 1

    # 按通过率区间统计
    rate_ranges = {"0-30%": 0, "30-50%": 0, "50-70%": 0, "70%+": 0}
    for p in problems:
        rate = p.get("accepted_rate", 0)
        if rate < 30:
            rate_ranges["0-30%"] += 1
        elif rate < 50:
            rate_ranges["30-50%"] += 1
        elif rate < 70:
            rate_ranges["50-70%"] += 1
        else:
            rate_ranges["70%+"] += 1

    lines = [
        "# 题目统计报告",
        "",
        "## 总体概况",
        "",
        f"- 总题目数: {total}",
        f"- 标签数: {len(tag_count)}",
        "",
        "## 难度分布",
        "",
    ]

    for diff in ["Easy", "Medium", "Hard"]:
        count = diff_count.get(diff, 0)
        pct = f"{count / total * 100:.1f}%" if total > 0 else "0%"
        lines.append(f"- {diff}: {count} ({pct})")

    lines.extend([
        "",
        "## 通过率分布",
        "",
    ])

    for rng, count in rate_ranges.items():
        lines.append(f"- {rng}: {count}")

    lines.extend([
        "",
        "## 热门标签 Top 10",
        "",
    ])

    for tag, count in sorted(tag_count.items(), key=lambda x: -x[1])[:10]:
        lines.append(f"- {tag}: {count} 题")

    lines.append("")
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="同步题目统计信息")
    parser.add_argument("--check-missing", action="store_true", help="检查缺失的语言实现")
    parser.add_argument("--report", action="store_true", help="生成统计报告")
    args = parser.parse_args()

    if not METADATA_PATH.exists():
        print(f"错误: 找不到元数据文件 {METADATA_PATH}")
        sys.exit(1)

    problems = load_problems()

    if args.report:
        report = generate_report(problems)
        print(report)

    if args.check_missing:
        print("检查缺失的语言实现...")
        missing = check_missing_solutions(problems)

        if missing:
            print(f"\n发现 {len(missing)} 道题目缺少部分语言实现：\n")
            for m in missing:
                title = f"{m['id']:04d} - {m['title']}"
                langs = ", ".join(m["missing"])
                print(f"  {title}")
                print(f"    缺少: {langs}")
        else:
            print("\n所有题目六种语言均已实现！🎉")

    if not args.check_missing and not args.report:
        # 默认同时运行两项
        print(generate_report(problems))
        missing = check_missing_solutions(problems)
        if missing:
            print(f"\n缺失实现: {len(missing)} 道题")
            for m in missing[:5]:
                langs = ", ".join(m["missing"])
                print(f"  {m['id']:04d} {m['title']}: {langs}")
        else:
            print("\n所有题目六种语言均已实现！🎉")


if __name__ == "__main__":
    main()
