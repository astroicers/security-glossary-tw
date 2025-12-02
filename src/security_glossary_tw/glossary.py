"""Security Glossary TW - 繁體中文資安術語庫"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator, Optional

import yaml

from .models import (
    Category,
    StyleRule,
    Term,
    TermMatch,
    ValidationIssue,
)
from .matcher import TermMatcher
from .validator import TermValidator


# 預設術語目錄位置
DEFAULT_TERMS_DIR = Path(__file__).parent.parent.parent / "terms"
DEFAULT_META_DIR = Path(__file__).parent.parent.parent / "meta"


class Glossary:
    """資安術語庫主要介面"""
    
    def __init__(
        self,
        terms_dir: Optional[Path | str] = None,
        meta_dir: Optional[Path | str] = None,
    ):
        """
        初始化術語庫
        
        Args:
            terms_dir: 術語 YAML 檔案目錄，預設使用套件內建
            meta_dir: 元資料目錄，預設使用套件內建
        """
        self.terms_dir = Path(terms_dir) if terms_dir else DEFAULT_TERMS_DIR
        self.meta_dir = Path(meta_dir) if meta_dir else DEFAULT_META_DIR
        
        # 載入術語
        self._terms: dict[str, Term] = {}
        self._terms_by_name: dict[str, str] = {}  # name -> term_id
        self._categories: dict[str, Category] = {}
        self._style_rules: list[StyleRule] = []
        
        self._load_terms()
        self._load_meta()
        
        # 初始化比對器和驗證器
        self._matcher = TermMatcher(self)
        self._validator = TermValidator(self)
    
    def _load_terms(self) -> None:
        """載入所有術語"""
        if not self.terms_dir.exists():
            return
        
        for yaml_file in self.terms_dir.glob("*.yaml"):
            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            
            if not data:
                continue
            
            # 支援 terms: [...] 或直接 [...]
            terms_list = data.get("terms", data) if isinstance(data, dict) else data
            
            for term_data in terms_list:
                try:
                    term = Term(**term_data)
                    self._terms[term.id] = term
                    
                    # 建立名稱索引
                    for name in term.get_all_names():
                        self._terms_by_name[name.lower()] = term.id
                except Exception as e:
                    print(f"Warning: Failed to load term from {yaml_file}: {e}")
    
    def _load_meta(self) -> None:
        """載入元資料（分類、風格指南）"""
        # 載入分類
        categories_file = self.meta_dir / "categories.yaml"
        if categories_file.exists():
            with open(categories_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            for cat_data in data.get("categories", []):
                cat = Category(**cat_data)
                self._categories[cat.id] = cat
        
        # 載入風格指南
        style_file = self.meta_dir / "style_guide.yaml"
        if style_file.exists():
            with open(style_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            for rule_data in data.get("forbidden_terms", []):
                self._style_rules.append(StyleRule(
                    avoid=rule_data.get("term", ""),
                    preferred=rule_data.get("preferred", ""),
                    reason=rule_data.get("reason", ""),
                ))
    
    # === 基本查詢 ===
    
    def get(self, term_id: str) -> Optional[Term]:
        """根據 ID 取得術語"""
        return self._terms.get(term_id)
    
    def get_by_name(self, name: str) -> Optional[Term]:
        """根據名稱（英文或中文）取得術語"""
        term_id = self._terms_by_name.get(name.lower())
        if term_id:
            return self._terms.get(term_id)
        return None
    
    def search(self, query: str) -> list[Term]:
        """搜尋術語（模糊比對）"""
        return self._matcher.search(query)
    
    def all(self) -> Iterator[Term]:
        """取得所有術語"""
        yield from self._terms.values()
    
    def count(self) -> int:
        """術語總數"""
        return len(self._terms)
    
    # === 分類查詢 ===
    
    def get_category(self, category_id: str) -> Optional[Category]:
        """取得分類資訊"""
        return self._categories.get(category_id)
    
    def get_terms_by_category(self, category: str) -> list[Term]:
        """取得特定分類的所有術語"""
        return [t for t in self._terms.values() if t.category == category]
    
    def get_categories(self) -> list[Category]:
        """取得所有分類"""
        return list(self._categories.values())
    
    # === 術語比對 ===
    
    def find_terms(self, text: str) -> list[TermMatch]:
        """
        在文本中找出所有術語
        
        Args:
            text: 要分析的文本
            
        Returns:
            比對到的術語列表
        """
        return self._matcher.find_all(text)
    
    def add_links(
        self,
        text: str,
        format: str = "markdown",
        base_url: str = "",
    ) -> str:
        """
        為文本中的術語加上連結
        
        Args:
            text: 原始文本
            format: 輸出格式，"markdown" 或 "html"
            base_url: 術語頁面的基礎 URL
            
        Returns:
            加上連結後的文本
        """
        return self._matcher.add_links(text, format=format, base_url=base_url)
    
    # === 用詞驗證 ===
    
    def validate(self, text: str) -> list[ValidationIssue]:
        """
        驗證文本用詞
        
        Args:
            text: 要驗證的文本
            
        Returns:
            驗證問題列表
        """
        return self._validator.validate(text)
    
    def get_style_rules(self) -> list[StyleRule]:
        """取得所有用詞規則"""
        return self._style_rules
    
    # === 匯出 ===
    
    def to_dict(self) -> dict:
        """匯出為字典（用於 JSON API）"""
        return {
            "terms": [t.model_dump() for t in self._terms.values()],
            "categories": [c.model_dump() for c in self._categories.values()],
            "count": len(self._terms),
        }
    
    def to_json(self) -> str:
        """匯出為 JSON 字串"""
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    # === 術語標記處理 ===
    
    def process_term_markers(self, text: str) -> str:
        """
        處理 [[term_id]] 標記，轉換為連結
        
        用於 AI 產生的文本，將 [[apt]] 轉換為 [APT](/glossary/apt)
        
        Args:
            text: 包含 [[term_id]] 標記的文本
            
        Returns:
            轉換後的 Markdown 文本
        """
        import re
        
        def replace_marker(match):
            term_id = match.group(1)
            term = self.get(term_id)
            if term:
                return f"[{term.term_en}](/glossary/{term_id} \"{term.definitions.brief}\")"
            return match.group(0)  # 找不到術語，保留原樣
        
        return re.sub(r"\[\[([a-z_]+)\]\]", replace_marker, text)
    
    def get_terms_summary(self, max_terms: int = 50) -> str:
        """
        產生術語摘要（用於 AI System Prompt）
        
        Args:
            max_terms: 最多包含的術語數量
            
        Returns:
            術語摘要文字
        """
        lines = ["# 資安術語庫\n"]
        
        # 按分類整理
        by_category: dict[str, list[Term]] = {}
        for term in self._terms.values():
            cat = term.category
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(term)
        
        count = 0
        for cat_id, terms in by_category.items():
            cat = self._categories.get(cat_id)
            cat_name = cat.name_zh if cat else cat_id
            lines.append(f"\n## {cat_name}\n")
            
            for term in sorted(terms, key=lambda t: t.term_en)[:10]:
                lines.append(f"- **{term.term_en}** ({term.term_zh}): {term.definitions.brief}")
                count += 1
                if count >= max_terms:
                    break
            
            if count >= max_terms:
                break
        
        lines.append("\n\n使用術語時請以 [[術語ID]] 標記，例如 [[apt]]")
        
        return "\n".join(lines)


# 便捷函式
_default_glossary: Optional[Glossary] = None


def get_glossary() -> Glossary:
    """取得預設術語庫實例"""
    global _default_glossary
    if _default_glossary is None:
        _default_glossary = Glossary()
    return _default_glossary


def get_term(term_id: str) -> Optional[Term]:
    """快速查詢術語"""
    return get_glossary().get(term_id)


def find_terms(text: str) -> list[TermMatch]:
    """快速比對文本中的術語"""
    return get_glossary().find_terms(text)


def validate_text(text: str) -> list[ValidationIssue]:
    """快速驗證文本用詞"""
    return get_glossary().validate(text)
