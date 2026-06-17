#!/usr/bin/env python3
"""
generate_tags.py — 根据 metadata/problems.yaml 自动生成 docs/tags/ 下的标签页。

每个标签页按难度分组列出题目，例如：

    # Array

    ## Easy
    - Two Sum
    - Merge Sorted Array

    ## Medium
    - Container With Most Water

用法：
    python scripts/generate_tags.py
"""

import sys
from pathlib import Path
from collections import defaultdict

METADATA_PATH = Path(__file__).parent.parent / "metadata" / "problems.yaml"
TAGS_DIR = Path(__file__).parent.parent / "docs" / "tags"
TAGS_META_PATH = Path(__file__).parent.parent / "metadata" / "tags.yaml"


def load_problems() -> list[dict]:
    """加载题目数据。"""
    try:
        import yaml
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("problems", [])
    except ImportError:
        print("警告: 未安装 pyyaml，跳过标签页生成")
        print("安装方法: pip install pyyaml")
        sys.exit(1)


def load_tag_meta() -> dict:
    """加载标签元数据。"""
    try:
        import yaml
        with open(TAGS_META_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("tags", {})
    except (ImportError, FileNotFoundError):
        return {}


def generate_tag_page(tag: str, problems: list[dict], tag_meta: dict) -> str:
    """生成单个标签页内容。"""
    tag_info = tag_meta.get(tag, {})
    tag_name = tag_info.get("name", tag.replace("-", " ").title())
    tag_desc = tag_info.get("description", "")

    # 按难度分组
    by_difficulty = defaultdict(list)
    for p in problems:
        if tag in p.get("tags", []):
            by_difficulty[p.get("difficulty", "Unknown")].append(p)

    # 难度排序
    diff_order = {"Easy": 0, "Medium": 1, "Hard": 2}
    sorted_difficulties = sorted(by_difficulty.keys(), key=lambda d: diff_order.get(d, 99))

    lines = [f"# {tag_name}"]
    if tag_desc:
        lines.append("")
        lines.append(tag_desc)

    for diff in sorted_difficulties:
        lines.append("")
        lines.append(f"## {'Easy' if diff == 'Easy' else 'Medium' if diff == 'Medium' else 'Hard'}")
        lines.append("")
        for p in sorted(by_difficulty[diff], key=lambda x: x.get("id", 0)):
            pid = p.get("id", 0)
            slug = p.get("slug", "")
            title = p.get("title", "")
            lines.append(f"- [{title}](/problems/{pid:04d}-{slug})")

    lines.append("")
    return "\n".join(lines)


def main():
    if not METADATA_PATH.exists():
        print(f"错误: 找不到元数据文件 {METADATA_PATH}")
        sys.exit(1)

    problems = load_problems()
    tag_meta = load_tag_meta()

    # 收集所有出现过的 tag
    all_tags = set()
    for p in problems:
        for tag in p.get("tags", []):
            all_tags.add(tag)

    # 也加载 tags.yaml 中定义的 tag
    for tag in tag_meta:
        all_tags.add(tag)

    TAGS_DIR.mkdir(parents=True, exist_ok=True)

    # 删除旧文件（不在新列表中的）
    existing = {f.stem for f in TAGS_DIR.glob("*.md")}
    for old_tag in existing:
        if old_tag not in all_tags:
            (TAGS_DIR / f"{old_tag}.md").unlink(missing_ok=True)

    count = 0
    for tag in sorted(all_tags):
        # 过滤掉不属于 top150 的题目
        top150_problems = [p for p in problems if tag in p.get("tags", [])]

        if not top150_problems:
            continue

        content = generate_tag_page(tag, top150_problems, tag_meta)
        (TAGS_DIR / f"{tag}.md").write_text(content, encoding="utf-8")
        count += 1
        print(f"  生成: {tag}.md ({len(top150_problems)} 题)")

    print(f"\n共生成 {count} 个标签页")
    print("完成！")


if __name__ == "__main__":
    main()
