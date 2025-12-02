"""術語比對引擎"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from rapidfuzz import fuzz, process

from .models import Term, TermMatch

if TYPE_CHECKING:
    from .glossary import Glossary


class TermMatcher:
    """術語比對器"""
    
    def __init__(self, glossary: Glossary):
        self.glossary = glossary
        self._build_index()
    
    def _build_index(self) -> None:
        """建立比對索引"""
        self._name_to_id: dict[str, str] = {}
        self._patterns: list[tuple[re.Pattern, str]] = []
        
        for term in self.glossary.all():
            # 建立名稱對照表
            for name in term.get_all_names():
                self._name_to_id[name.lower()] = term.id
                
                # 為較長的術語建立正則模式（避免部分匹配）
                if len(name) >= 2:
                    # 使用 word boundary 避免部分匹配
                    pattern = re.compile(
                        r"\b" + re.escape(name) + r"\b",
                        re.IGNORECASE
                    )
                    self._patterns.append((pattern, term.id))
        
        # 按長度排序，優先匹配較長的術語
        self._patterns.sort(key=lambda x: -len(x[0].pattern))
    
    def search(self, query: str, limit: int = 10) -> list[Term]:
        """
        搜尋術語（支援模糊比對）
        
        Args:
            query: 搜尋關鍵字
            limit: 最多回傳數量
            
        Returns:
            匹配的術語列表
        """
        if not query:
            return []
        
        # 精確匹配
        term = self.glossary.get_by_name(query)
        if term:
            return [term]
        
        # 模糊比對
        all_names = list(self._name_to_id.keys())
        matches = process.extract(
            query.lower(),
            all_names,
            scorer=fuzz.WRatio,
            limit=limit,
        )
        
        results = []
        seen_ids = set()
        for name, score, _ in matches:
            if score < 60:  # 閾值
                continue
            term_id = self._name_to_id.get(name)
            if term_id and term_id not in seen_ids:
                term = self.glossary.get(term_id)
                if term:
                    results.append(term)
                    seen_ids.add(term_id)
        
        return results
    
    def find_all(self, text: str) -> list[TermMatch]:
        """
        在文本中找出所有術語
        
        Args:
            text: 要分析的文本
            
        Returns:
            比對結果列表
        """
        matches: list[TermMatch] = []
        matched_spans: list[tuple[int, int]] = []
        
        for pattern, term_id in self._patterns:
            for match in pattern.finditer(text):
                start, end = match.start(), match.end()
                
                # 檢查是否與已匹配的範圍重疊
                overlaps = any(
                    not (end <= s or start >= e)
                    for s, e in matched_spans
                )
                if overlaps:
                    continue
                
                term = self.glossary.get(term_id)
                if term:
                    matches.append(TermMatch(
                        term_id=term_id,
                        term=term,
                        matched_text=match.group(),
                        start=start,
                        end=end,
                        confidence=1.0,
                    ))
                    matched_spans.append((start, end))
        
        # 按位置排序
        matches.sort(key=lambda m: m.start)
        return matches
    
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
            format: "markdown" 或 "html"
            base_url: 術語頁面基礎 URL
            
        Returns:
            加上連結的文本
        """
        matches = self.find_all(text)
        
        if not matches:
            return text
        
        # 從後往前替換，避免位置偏移
        result = text
        for match in reversed(matches):
            if format == "markdown":
                replacement = (
                    f"[{match.matched_text}]"
                    f"({base_url}/glossary/{match.term_id} "
                    f'"{match.term.definitions.brief}")'
                )
            else:  # html
                replacement = (
                    f'<a href="{base_url}/glossary/{match.term_id}" '
                    f'class="term-link" '
                    f'title="{match.term.definitions.brief}">'
                    f'{match.matched_text}</a>'
                )
            
            result = result[:match.start] + replacement + result[match.end:]
        
        return result
    
    def highlight(self, text: str, tag: str = "mark") -> str:
        """
        標記文本中的術語
        
        Args:
            text: 原始文本
            tag: HTML 標籤名稱
            
        Returns:
            標記後的 HTML
        """
        matches = self.find_all(text)
        
        if not matches:
            return text
        
        result = text
        for match in reversed(matches):
            replacement = f"<{tag}>{match.matched_text}</{tag}>"
            result = result[:match.start] + replacement + result[match.end:]
        
        return result
