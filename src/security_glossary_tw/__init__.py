"""
Security Glossary TW - 繁體中文資安術語庫

台灣第一個開源、結構化、可機器讀取的繁體中文資安專有名詞庫。

基本用法：

    from security_glossary_tw import Glossary

    glossary = Glossary()
    
    # 查詢術語
    term = glossary.get("apt")
    print(term.term_zh)  # 進階持續性威脅
    
    # 比對文本
    matches = glossary.find_terms("APT 組織發動攻擊")
    
    # 驗證用詞
    issues = glossary.validate("黑客入侵系統")

快速函式：

    from security_glossary_tw import get_term, find_terms, validate_text
    
    term = get_term("apt")
    matches = find_terms("APT 組織發動攻擊")
    issues = validate_text("黑客入侵系統")
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .glossary import (
    Glossary,
    get_glossary,
    get_term,
    find_terms,
    validate_text,
)
from .models import (
    Term,
    TermMatch,
    ValidationIssue,
    Category,
    StyleRule,
)
from .matcher import TermMatcher
from .validator import TermValidator

__all__ = [
    # 主要類別
    "Glossary",
    "TermMatcher",
    "TermValidator",
    # 資料模型
    "Term",
    "TermMatch",
    "ValidationIssue",
    "Category",
    "StyleRule",
    # 便捷函式
    "get_glossary",
    "get_term",
    "find_terms",
    "validate_text",
]
