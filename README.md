# docxspace

`docxspace` 是一个结构化 Markdown 文档组织与构建工具（Skill），支持将多层级编号目录与 Markdown 文件自动合并并编译为精美排版的 Word（`.docx`）文档。

## 特性

- 📂 **结构化管理**：通过带 3 位数字前缀的目录（如 `001概述/`、`002接口/`）管理章节层级与顺序。
- 🔄 **自动标题提取**：自动从目录名提取标题，无需在 `index.md` 重复书写一级/二级标题。
- 📄 **合并与转换分离**：
  - `combine`：纯 Python 标准库支持，零额外依赖合并完整 Markdown。
  - `convert`：借助 Pandoc 及自定义样式模板（`reference.docx`）生成美观 Word 文档。

## 目录规范

```text
workspace-root/
├── image/               # 公共文档图片
├── reference.docx       # 可选：自定义 Word 样式模板（默认使用 skill 内部模板）
└── <文档名称>/          # 顶层文档目录
    ├── index.md         # 文档元数据（标题、作者、日期）及前言
    ├── 001章节名/       # 3 位数字前缀用于排序，自动作为章节标题
    │   ├── index.md     # 章节内容
    │   └── 001子节/     # 子章节
    │       └── index.md
    └── 002下一章/
        └── index.md
```

## 快速使用

### 1. 依赖要求

- Python 3（合并 Markdown）
- [Pandoc](https://pandoc.org/)（可选，生成 `.docx` 时需要）

### 2. 常用构建命令

无需将 `build.py` 和 `reference.docx` 复制到项目工作区，直接通过 skill 脚本路径调用即可（例如 `~/.claude/skills/docxspace/scripts/build.py` 或 `<skill_dir>/scripts/build.py`）：

```bash
# 构建当前工作区下所有文档（生成合并后的 .md 和 .docx）
python3 ~/.claude/skills/docxspace/scripts/build.py

# 仅合并 Markdown（无需 Pandoc）
python3 ~/.claude/skills/docxspace/scripts/build.py combine

# 构建指定文档
python3 ~/.claude/skills/docxspace/scripts/build.py <文档目录名>

# 仅合并指定文档
python3 ~/.claude/skills/docxspace/scripts/build.py combine <文档目录名>

# 将已合并的 Markdown 转换为 docx
python3 ~/.claude/skills/docxspace/scripts/build.py convert <文档目录名>
```
