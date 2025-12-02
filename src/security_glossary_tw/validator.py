"""用詞驗證器"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .models import ValidationIssue

if TYPE_CHECKING:
    from .glossary import Glossary


class TermValidator:
    """用詞驗證器 - 檢查文本是否使用標準術語"""
    
    def __init__(self, glossary: Glossary):
        self.glossary = glossary
        self._build_rules()
    
    def _build_rules(self) -> None:
        """建立驗證規則"""
        self._forbidden_patterns: list[tuple[re.Pattern, str, str]] = []
        
        # 從風格指南載入禁止用詞
        for rule in self.glossary.get_style_rules():
            if rule.avoid:
                pattern = re.compile(re.escape(rule.avoid), re.IGNORECASE)
                self._forbidden_patterns.append((
                    pattern,
                    rule.avoid,
                    rule.preferred,
                ))
        
        # 從術語的 usage.avoid 載入
        for term in self.glossary.all():
            for avoid in term.usage.avoid:
                pattern = re.compile(re.escape(avoid), re.IGNORECASE)
                self._forbidden_patterns.append((
                    pattern,
                    avoid,
                    f"{term.term_zh} ({term.term_en})",
                ))
    
    def validate(self, text: str) -> list[ValidationIssue]:
        """
        驗證文本用詞
        
        Args:
            text: 要驗證的文本
            
        Returns:
            驗證問題列表
        """
        issues: list[ValidationIssue] = []
        lines = text.split("\n")
        
        for line_num, line in enumerate(lines, start=1):
            # 檢查禁止用詞
            for pattern, avoid, preferred in self._forbidden_patterns:
                for match in pattern.finditer(line):
                    issues.append(ValidationIssue(
                        line=line_num,
                        column=match.start() + 1,
                        text=match.group(),
                        issue_type="forbidden_term",
                        suggestion=f"建議改為「{preferred}」",
                        severity="warning",
                    ))
        
        return issues
    
    def validate_with_context(
        self,
        text: str,
        context_lines: int = 1,
    ) -> list[dict]:
        """
        驗證並回傳上下文
        
        Args:
            text: 要驗證的文本
            context_lines: 上下文行數
            
        Returns:
            包含上下文的驗證結果
        """
        issues = self.validate(text)
        lines = text.split("\n")
        
        results = []
        for issue in issues:
            start = max(0, issue.line - context_lines - 1)
            end = min(len(lines), issue.line + context_lines)
            
            context = []
            for i in range(start, end):
                prefix = ">>> " if i == issue.line - 1 else "    "
                context.append(f"{prefix}{i + 1}: {lines[i]}")
            
            results.append({
                "issue": issue.model_dump(),
                "context": "\n".join(context),
            })
        
        return results
    
    def fix(self, text: str) -> tuple[str, list[ValidationIssue]]:
        """
        自動修正用詞問題
        
        Args:
            text: 要修正的文本
            
        Returns:
            (修正後的文本, 已修正的問題列表)
        """
        issues = self.validate(text)
        
        if not issues:
            return text, []
        
        # 從後往前替換
        result = text
        fixed = []
        
        # 將問題按位置排序（從後往前）
        sorted_issues = sorted(
            issues,
            key=lambda i: (i.line, i.column or 0),
            reverse=True,
        )
        
        lines = result.split("\n")
        
        for issue in sorted_issues:
            if issue.issue_type == "forbidden_term":
                line_idx = issue.line - 1
                if 0 <= line_idx < len(lines):
                    line = lines[line_idx]
                    # 從 suggestion 中提取建議用詞
                    suggested = issue.suggestion.replace("建議改為「", "").replace("」", "")
                    # 如果建議包含多個選項，取第一個
                    if "(" in suggested:
                        suggested = suggested.split("(")[0].strip()
                    
                    # 替換
                    start = (issue.column or 1) - 1
                    end = start + len(issue.text)
                    lines[line_idx] = line[:start] + suggested + line[end:]
                    fixed.append(issue)
        
        return "\n".join(lines), fixed
    
    def get_report(self, text: str) -> str:
        """
        產生驗證報告
        
        Args:
            text: 要驗證的文本
            
        Returns:
            Markdown 格式的報告
        """
        issues = self.validate(text)
        
        if not issues:
            return "✅ 未發現用詞問題"
        
        lines = [
            f"## 用詞驗證報告",
            f"",
            f"發現 {len(issues)} 個問題：",
            f"",
        ]
        
        for i, issue in enumerate(issues, start=1):
            lines.append(
                f"{i}. 第 {issue.line} 行：「{issue.text}」{issue.suggestion}"
            )
        
        return "\n".join(lines)
