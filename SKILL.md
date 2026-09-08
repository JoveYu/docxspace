---
name: docxspace
description: Scaffold, write, organize, and build structured Markdown documentation spaces into combined Markdown and styled Word (.docx) documents. Use when creating new doc projects, organizing multi-chapter docs with numbered folders, or building Word docs with Pandoc.
---

# docxspace

Organize structured documentation spaces using directories and Markdown files, then build them into combined Markdown and professionally styled Word (`.docx`) documents via Pandoc.

## Core Capabilities

1. **Scaffold docxspace**: Initialize documentation directory structures and `index.md` files in any workspace (without polluting workspace with scripts or assets).
2. **Document Authoring & Structuring**: Organize chapters, sections, and metadata using numbered directory hierarchies.
3. **Build & Convert**: Merge multi-file documents and convert them into `.docx` directly using the skill's built-in script and reference template.

---

## Directory & Document Architecture

Each top-level directory containing an `index.md` represents an independent document:

```text
workspace-root/
├── image/               # Shared document images
├── reference.docx       # Optional: workspace-level Pandoc style template (falls back to skill's reference.docx)
└── <DocumentName>/       # Top-level document directory
    ├── index.md         # Document frontmatter / preface
    ├── 001ChapterName/  # 3-digit prefix for natural ordering
    │   ├── index.md     # Chapter content
    │   └── 001Section/  # Sub-sections
    │       └── index.md
    └── 002NextChapter/
        └── index.md
```

### Ordering & Headings Rules

- **Sorting Prefix**: Use a 3-digit number prefix to order directories: `001Overview`, `002-Interfaces`, `010 Appendix`.
- **Title Extraction**: The 3-digit prefix and any delimiter (`-`, `_`, `.`, space) are automatically stripped to generate the heading.
  - `001Overview` -> Heading `# Overview` (or `##` according to depth).
- **No Duplicate Headings in `index.md`**: Do **not** write the directory's generated title at the top of its `index.md`. The build script generates the heading automatically from the directory name.
- **Top-level `index.md`**: Contains document metadata (Pandoc title block) and preamble:
  ```markdown
  % Document Title
  % Author or Organization
  % Date
  ```
- **Nested `index.md`**: Sub-sections inside an `index.md` should use headings relative to their level (e.g. if the directory is `##`, internal subsections start at `###`).

### Markdown Formatting Conventions

- **Tables**: Standard Markdown tables. Must be followed immediately by a table caption line: `Table: Caption Text`.
- **Equations**: LaTeX blocks `$$ ... $$`.
- **Callouts**: Standard blockquotes `> **注意**：...`.
- **Images**: Store images in `image/` or subdirectories. Reference them via relative paths (e.g., `image/pic.png`).

---

## Workflows

### 1. Initializing in a New Project

**IMPORTANT**: Do **NOT** copy `build.py` or `reference.docx` into the user workspace. The build script is executed directly from the skill directory, and will automatically fall back to using the skill's bundled `reference.docx` when no workspace-level template is present.

When requested to setup `docxspace` or initialize document structure:
1. Create `image/` directory if needed.
2. Scaffold the target document directory structure with `index.md` files (or refer to sample in `<skill_dir>/assets/测试文档`).
3. (Only if the user explicitly requests custom Word styles) Place a custom `reference.docx` in the workspace root.

### 2. Building Documents

Execute `build.py` directly from the skill directory:

```bash
# Auto-discover and build all top-level document directories (.md and .docx) in the current workspace
python3 <skill_dir>/scripts/build.py

# Combine Markdown only (does not require Pandoc)
python3 <skill_dir>/scripts/build.py combine

# Build a specific document
python3 <skill_dir>/scripts/build.py <DocumentDirectoryName>

# Combine a specific document only
python3 <skill_dir>/scripts/build.py combine <DocumentDirectoryName>

# Convert existing combined Markdown to docx
python3 <skill_dir>/scripts/build.py convert <DocumentDirectoryName>
```

> **Note**: `<skill_dir>` refers to the docxspace skill directory. It automatically discovers documents in and outputs `.md`/`.docx` into the current working directory (workspace root).

**Requirements**:
- Merging Markdown (`combine`): Python 3 standard library only (no external dependencies).
- Converting to Word (`convert`): Requires `pandoc` installed on the system.
