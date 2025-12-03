#!/usr/bin/env python3
"""
Build documentation and API from YAML term definitions.

This script generates:
1. Markdown files for each term in docs/glossary/
2. JSON API files in docs/api/v1/
3. Index pages for glossary and categories
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

# Paths
ROOT_DIR = Path(__file__).parent.parent
TERMS_DIR = ROOT_DIR / "terms"
META_DIR = ROOT_DIR / "meta"
DOCS_DIR = ROOT_DIR / "docs"
GLOSSARY_DIR = DOCS_DIR / "glossary"
CATEGORIES_DIR = DOCS_DIR / "categories"
API_DIR = DOCS_DIR / "api" / "v1"
API_TERMS_DIR = API_DIR / "terms"


def load_categories() -> dict[str, dict]:
    """Load category definitions."""
    categories_file = META_DIR / "categories.yaml"
    with open(categories_file, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return {cat["id"]: cat for cat in data.get("categories", [])}


def load_all_terms() -> list[dict]:
    """Load all terms from YAML files."""
    terms = []
    for yaml_file in sorted(TERMS_DIR.glob("*.yaml")):
        with open(yaml_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data and "terms" in data:
            terms.extend(data["terms"])
    return terms


def generate_term_markdown(term: dict, categories: dict[str, dict]) -> str:
    """Generate markdown content for a single term."""
    term_id = term["id"]
    term_en = term["term_en"]
    term_zh = term["term_zh"]
    definitions = term.get("definitions", {})
    brief = definitions.get("brief", "")
    standard = definitions.get("standard", "")
    category_id = term.get("category", "")
    category = categories.get(category_id, {})
    category_name = category.get("name_zh", category_id)
    category_icon = category.get("icon", "📚")

    lines = [
        f"# {term_en}",
        "",
        f"**{term_zh}**",
        "",
        f"!!! info \"{brief}\"",
        "",
    ]

    # Category badge
    lines.extend([
        f"<span class=\"md-tag\">{category_icon} {category_name}</span>",
        "",
    ])

    # Standard definition
    if standard:
        lines.extend([
            "## 定義",
            "",
            standard.strip(),
            "",
        ])

    # Aliases
    aliases = term.get("aliases", {})
    zh_aliases = aliases.get("zh", [])
    en_aliases = aliases.get("en", [])
    if zh_aliases or en_aliases:
        lines.extend([
            "## 別名",
            "",
        ])
        if zh_aliases:
            lines.append(f"- 中文：{', '.join(zh_aliases)}")
        if en_aliases:
            lines.append(f"- 英文：{', '.join(en_aliases)}")
        lines.append("")

    # Related terms
    related = term.get("related_terms", [])
    if related:
        lines.extend([
            "## 相關術語",
            "",
        ])
        for rel_id in related:
            lines.append(f"- [{rel_id}](../{rel_id}/)")
        lines.append("")

    # Tags
    tags = term.get("tags", [])
    if tags:
        lines.extend([
            "## 標籤",
            "",
            " ".join(f"`{tag}`" for tag in tags),
            "",
        ])

    # Usage examples
    usage = term.get("usage", {})
    examples = usage.get("examples", [])
    if examples:
        lines.extend([
            "## 使用範例",
            "",
        ])
        for example in examples:
            lines.append(f"> {example}")
            lines.append("")

    # Avoid terms
    avoid = usage.get("avoid", [])
    if avoid:
        lines.extend([
            "!!! warning \"避免使用\"",
            f"    以下用語不建議使用：{', '.join(avoid)}",
            "",
        ])

    # References
    references = term.get("references", {})
    if references:
        lines.extend([
            "## 參考資料",
            "",
        ])
        for ref_name, ref_url in references.items():
            display_name = ref_name.replace("_", " ").title()
            lines.append(f"- [{display_name}]({ref_url})")
        lines.append("")

    return "\n".join(lines)


def generate_term_json(term: dict) -> dict:
    """Generate JSON representation for a single term."""
    return {
        "id": term["id"],
        "term_en": term["term_en"],
        "term_zh": term["term_zh"],
        "definitions": term.get("definitions", {}),
        "category": term.get("category", ""),
        "subcategory": term.get("subcategory", ""),
        "tags": term.get("tags", []),
        "related_terms": term.get("related_terms", []),
        "aliases": term.get("aliases", {}),
    }


def generate_glossary_index(terms: list[dict], categories: dict[str, dict]) -> str:
    """Generate glossary index page."""
    lines = [
        "# 術語庫",
        "",
        "資安術語完整列表，點擊術語查看詳細說明。",
        "",
        f"共收錄 **{len(terms)}** 個術語。",
        "",
    ]

    # Group by category
    by_category: dict[str, list[dict]] = {}
    for term in terms:
        cat_id = term.get("category", "other")
        if cat_id not in by_category:
            by_category[cat_id] = []
        by_category[cat_id].append(term)

    # Generate sections
    for cat_id, cat_terms in sorted(by_category.items()):
        cat = categories.get(cat_id, {})
        cat_name = cat.get("name_zh", cat_id)
        cat_icon = cat.get("icon", "📚")

        lines.extend([
            f"## {cat_icon} {cat_name}",
            "",
            "| 英文 | 中文 | 說明 |",
            "|------|------|------|",
        ])

        for term in sorted(cat_terms, key=lambda t: t["term_en"].lower()):
            term_id = term["id"]
            term_en = term["term_en"]
            term_zh = term["term_zh"]
            brief = term.get("definitions", {}).get("brief", "")
            lines.append(f"| [{term_en}]({term_id}/) | {term_zh} | {brief} |")

        lines.append("")

    return "\n".join(lines)


def generate_categories_index(terms: list[dict], categories: dict[str, dict]) -> str:
    """Generate categories index page."""
    lines = [
        "# 分類瀏覽",
        "",
        "依分類瀏覽資安術語。",
        "",
    ]

    # Count terms per category
    counts: dict[str, int] = {}
    for term in terms:
        cat_id = term.get("category", "other")
        counts[cat_id] = counts.get(cat_id, 0) + 1

    # Generate category cards
    for cat_id, cat in categories.items():
        cat_name = cat.get("name_zh", cat_id)
        cat_icon = cat.get("icon", "📚")
        cat_desc = cat.get("description", "")
        count = counts.get(cat_id, 0)

        lines.extend([
            f"## {cat_icon} {cat_name}",
            "",
            f"{cat_desc}",
            "",
            f"共 **{count}** 個術語 → [查看全部](../glossary/)",
            "",
        ])

    return "\n".join(lines)


def generate_api_index() -> str:
    """Generate API documentation page."""
    return """# API 文件

資安術語庫提供靜態 JSON API，可供其他應用程式使用。

## 端點

### 取得所有術語

```
GET /api/v1/terms.json
```

回傳所有術語的列表。

### 取得單一術語

```
GET /api/v1/terms/{term_id}.json
```

回傳指定術語的詳細資訊。

**範例：**

```
GET /api/v1/terms/apt.json
```

### 取得所有分類

```
GET /api/v1/categories.json
```

回傳所有分類的列表。

## 回應格式

### 術語物件

```json
{
  "id": "apt",
  "term_en": "APT",
  "term_zh": "進階持續性威脅",
  "definitions": {
    "brief": "國家級駭客組織發動的長期網路攻擊",
    "standard": "進階持續性威脅是一種..."
  },
  "category": "threat_actors",
  "tags": ["國家級", "長期攻擊"],
  "related_terms": ["apt_group", "nation_state"]
}
```

## 使用範例

### JavaScript

```javascript
fetch('https://astroicers.github.io/security-glossary-tw/api/v1/terms/apt.json')
  .then(response => response.json())
  .then(term => {
    console.log(term.term_zh); // 進階持續性威脅
  });
```

### Python

```python
import requests

resp = requests.get(
    'https://astroicers.github.io/security-glossary-tw/api/v1/terms/apt.json'
)
term = resp.json()
print(term['term_zh'])  # 進階持續性威脅
```

## CORS

靜態檔案透過 GitHub Pages 提供，支援跨域請求。
"""


def generate_home_page(terms: list[dict], categories: dict[str, dict]) -> str:
    """Generate home page."""
    return f"""# 資安術語庫

歡迎使用 **Security Glossary TW** - 繁體中文資安術語標準化詞彙庫。

## 📊 統計

- 術語總數：**{len(terms)}**
- 分類數量：**{len(categories)}**

## 🔍 快速開始

- [瀏覽術語庫](glossary/) - 查看所有術語
- [分類瀏覽](categories/) - 依分類查找
- [API 文件](api.md) - 程式化存取

## 💡 用途

此術語庫可用於：

1. **統一翻譯** - 確保團隊使用一致的資安術語翻譯
2. **報告撰寫** - 在資安報告中使用標準化用語
3. **教育訓練** - 學習資安專業詞彙
4. **自動化工具** - 透過 API 整合到其他系統

## 🔗 連結

- [GitHub 專案](https://github.com/astroicers/security-glossary-tw)
- [PyPI 套件](https://pypi.org/project/security-glossary-tw/)

## 📝 貢獻

歡迎提交 Pull Request 新增或修正術語！
"""


def main():
    """Main function to build docs."""
    print("Loading categories...")
    categories = load_categories()
    print(f"  Loaded {len(categories)} categories")

    print("Loading terms...")
    terms = load_all_terms()
    print(f"  Loaded {len(terms)} terms")

    # Ensure directories exist
    GLOSSARY_DIR.mkdir(parents=True, exist_ok=True)
    CATEGORIES_DIR.mkdir(parents=True, exist_ok=True)
    API_DIR.mkdir(parents=True, exist_ok=True)
    API_TERMS_DIR.mkdir(parents=True, exist_ok=True)

    # Generate term pages
    print("Generating term pages...")
    for term in terms:
        term_id = term["id"]
        term_dir = GLOSSARY_DIR / term_id
        term_dir.mkdir(exist_ok=True)

        # Markdown
        md_content = generate_term_markdown(term, categories)
        (term_dir / "index.md").write_text(md_content, encoding="utf-8")

        # JSON API
        json_content = generate_term_json(term)
        (API_TERMS_DIR / f"{term_id}.json").write_text(
            json.dumps(json_content, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    print(f"  Generated {len(terms)} term pages")

    # Generate glossary index
    print("Generating glossary index...")
    glossary_index = generate_glossary_index(terms, categories)
    (GLOSSARY_DIR / "index.md").write_text(glossary_index, encoding="utf-8")

    # Generate categories index
    print("Generating categories index...")
    categories_index = generate_categories_index(terms, categories)
    (CATEGORIES_DIR / "index.md").write_text(categories_index, encoding="utf-8")

    # Generate API files
    print("Generating API files...")

    # All terms
    all_terms_json = [generate_term_json(t) for t in terms]
    (API_DIR / "terms.json").write_text(
        json.dumps({"terms": all_terms_json, "count": len(all_terms_json)},
                   ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    # Categories
    categories_json = list(categories.values())
    (API_DIR / "categories.json").write_text(
        json.dumps({"categories": categories_json, "count": len(categories_json)},
                   ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    # Generate API documentation
    print("Generating API documentation...")
    api_doc = generate_api_index()
    (DOCS_DIR / "api.md").write_text(api_doc, encoding="utf-8")

    # Generate home page
    print("Generating home page...")
    home_page = generate_home_page(terms, categories)
    (DOCS_DIR / "index.md").write_text(home_page, encoding="utf-8")

    print("Done!")
    print(f"  - {len(terms)} term pages in docs/glossary/")
    print(f"  - {len(terms)} JSON files in docs/api/v1/terms/")
    print(f"  - API index at docs/api/v1/terms.json")
    print(f"  - Categories at docs/api/v1/categories.json")


if __name__ == "__main__":
    main()
