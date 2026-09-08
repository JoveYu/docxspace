---
name: docxspace
description: Scaffold, write, organize, and build structured Markdown documentation spaces into combined Markdown and styled Word (.docx) documents. Use when creating new doc projects, organizing multi-chapter docs with numbered folders, or building Word docs with Pandoc.
---

# docxspace

Organize structured documentation spaces using directories and Markdown files, then build them into combined Markdown and professionally styled Word (`.docx`) documents via Pandoc.

## Core Capabilities

1. **Scaffold docxspace**: Initialize build scripts, templates (`reference.docx`), and directory structures in any workspace.
2. **Document Authoring & Structuring**: Organize chapters, sections, and metadata using numbered directory hierarchies.
3. **Build & Convert**: Merge multi-file documents and convert them into `.docx` with table of contents and custom reference styles.

---

## Directory & Document Architecture

Each top-level directory containing an `index.md` represents an independent document:

```text
workspace-root/
├── build.py             # Build script (copied from skill's scripts/build.py)
├── reference.docx       # Optional Pandoc Word style template
├── image/               # Shared document images
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

When requested to setup `docxspace` or initialize document building in a project:

1. Copy the build script:
   Copy `<skill_dir>/scripts/build.py` into the target workspace root as `build.py` (or execute directly from skill without copying).
2. (Optional) Copy style template:
   Copy `<skill_dir>/assets/reference.docx` to the target workspace root if customized styling is desired.
3. (Optional) Scaffold sample document:
   Copy `<skill_dir>/assets/测试文档` as a reference/starter directory structure.
4. Create `image/` directory.
5. Scaffold the target document directory structure with `index.md` files.

### 2. Building Documents

Run the build script from the workspace root:

```bash
# Auto-discover and build all top-level document directories (.md and .docx)
python3 build.py

# Combine Markdown only (does not require Pandoc)
python3 build.py combine

# Build a specific document
python3 build.py <DocumentDirectoryName>

# Combine a specific document only
python3 build.py combine <DocumentDirectoryName>

# Convert existing combined Markdown to docx
python3 build.py convert <DocumentDirectoryName>
```

**Requirements**:
- Merging Markdown (`combine`): Python 3 standard library only (no external dependencies).
- Converting to Word (`convert`): Requires `pandoc` installed on the system.
