#!/usr/bin/env python3
"""将按目录组织的 Markdown 文档合并并转换为 Word。"""

import os
import re
import subprocess
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_REFERENCE_DOCX = SKILL_DIR / "assets" / "reference.docx"
INDEX_FILE_NAME = "index.md"
NUMBERED_DIRECTORY_RE = re.compile(r"^\d{3}(?:[ _.-]*)")


def get_working_dir():
    """获取当前执行上下文的工作目录。"""
    return Path.cwd().resolve()


def title_from_directory(name):
    """移除目录开头的三位排序编号及其分隔符。"""
    return NUMBERED_DIRECTORY_RE.sub("", name).strip()


def natural_sort_key(name):
    """按名称中的数字自然排序。"""
    return [
        (0, int(part)) if part.isdigit() else (1, part.casefold())
        for part in re.split(r"(\d+)", name)
        if part
    ]


def child_directories(path):
    """返回非隐藏子目录，按自然顺序排列。"""
    return sorted(
        (child for child in path.iterdir() if child.is_dir() and not child.name.startswith(".")),
        key=lambda child: natural_sort_key(child.name),
    )


def discover_documents(root_dir=None):
    """发现根目录下包含 ``index.md`` 的一级文档目录。"""
    root_dir = Path(get_working_dir() if root_dir is None else root_dir)
    return [
        path for path in child_directories(root_dir) if (path / INDEX_FILE_NAME).is_file()
    ]


def collect_markdown(path, level=0):
    """递归收集目录正文及自动生成的标题。"""
    sections = []
    if level:
        sections.append(f"{'#' * level} {title_from_directory(path.name)}")

    index_file = path / INDEX_FILE_NAME
    if index_file.is_file():
        content = index_file.read_text(encoding="utf-8").strip()
        if content:
            sections.append(content)

    for child in child_directories(path):
        sections.extend(collect_markdown(child, level + 1))
    return sections


def combine_document(source_dir, output_file):
    """合并一个文档目录为单个 Markdown 文件。"""
    content = "\n\n".join(collect_markdown(Path(source_dir)))
    Path(output_file).write_text(f"{content}\n" if content else "", encoding="utf-8")


def pandoc_args(markdown_file, docx_file, root_dir=None):
    """构建通用的 Pandoc DOCX 转换参数。"""
    root_dir = Path(get_working_dir() if root_dir is None else root_dir)
    args = [
        "pandoc",
        str(markdown_file),
        "--output",
        str(docx_file),
        "--from",
        "markdown",
        "--toc",
        "--metadata",
        "toc-title:目录",
    ]

    # 优先使用目标目录或工作区下的 reference.docx，不存在时自动回退到 skill 内部自带的 template
    reference_doc = root_dir / "reference.docx"
    if not reference_doc.is_file() and DEFAULT_REFERENCE_DOCX.is_file():
        reference_doc = DEFAULT_REFERENCE_DOCX

    if reference_doc.is_file():
        args.extend(["--reference-doc", str(reference_doc)])

    image_dir = root_dir / "image"
    if image_dir.is_dir():
        args.extend(["--resource-path", os.pathsep.join((str(root_dir), str(image_dir)))])
    return args


def convert_document(markdown_file, docx_file, root_dir=None):
    """调用 Pandoc 将合并后的 Markdown 转换为 Word。"""
    root_dir = Path(get_working_dir() if root_dir is None else root_dir)
    markdown_file = Path(markdown_file)
    if not markdown_file.is_file():
        raise ValueError(f"合并文件不存在: {markdown_file.name}，请先执行 combine")

    try:
        subprocess.run(pandoc_args(markdown_file, docx_file, root_dir=root_dir), check=True, cwd=root_dir)
    except FileNotFoundError:
        raise RuntimeError("Pandoc 未安装或不在系统环境变量中。请安装 Pandoc。") from None


def parse_targets(names):
    """解析指定的文档目录；未指定时自动发现。支持目录名、相对路径或绝对路径。"""
    working_dir = get_working_dir()
    if not names:
        return discover_documents(working_dir)

    targets = []
    for raw in ",".join(names).split(","):
        name = raw.strip()
        if not name:
            continue
        path = Path(name)
        if not path.is_absolute():
            # 优先从当前工作目录相对解析
            cand = working_dir / path
            if cand.exists():
                path = cand
            else:
                path = path.resolve()
        else:
            path = path.resolve()

        if not path.is_dir():
            raise ValueError(f"文档目录不存在: {name}")
        if not (path / INDEX_FILE_NAME).is_file():
            raise ValueError(f"文档目录缺少 {INDEX_FILE_NAME}: {name}")
        targets.append(path)
    return targets


def main(argv=None):
    """执行合并、转换或完整构建。"""
    args = list(sys.argv[1:] if argv is None else argv)
    mode = "all"
    if args and args[0].lower() in {"combine", "convert"}:
        mode = args.pop(0).lower()

    try:
        documents = parse_targets(args)
        if not documents:
            raise ValueError("根目录下没有找到包含 index.md 的文档目录")

        for document_dir in documents:
            parent_dir = document_dir.parent
            markdown_file = parent_dir / f"{document_dir.name}.md"
            docx_file = parent_dir / f"{document_dir.name}.docx"
            if mode in {"all", "combine"}:
                print(f"合并 '{document_dir.name}' -> '{markdown_file.name}' ...")
                combine_document(document_dir, markdown_file)
            if mode in {"all", "convert"}:
                print(f"转换 '{markdown_file.name}' -> '{docx_file.name}' ...")
                convert_document(markdown_file, docx_file, root_dir=parent_dir)
    except (RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"错误: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
