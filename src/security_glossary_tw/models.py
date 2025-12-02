"""資安術語資料模型"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TermStatus(str, Enum):
    """術語狀態"""
    APPROVED = "approved"
    PENDING = "pending"
    DEPRECATED = "deprecated"


class Definitions(BaseModel):
    """術語定義（三層次）"""
    brief: str = Field(..., description="簡短定義，≤30字，用於 Tooltip")
    standard: Optional[str] = Field(None, description="標準定義，≤100字，用於側邊欄")
    detailed: Optional[str] = Field(None, description="完整定義，用於術語頁面")


class Aliases(BaseModel):
    """別名"""
    en: list[str] = Field(default_factory=list, description="英文別名")
    zh: list[str] = Field(default_factory=list, description="中文別名")


class Usage(BaseModel):
    """使用指南"""
    preferred: bool = Field(True, description="是否為優先用詞")
    context: Optional[str] = Field(None, description="使用情境說明")
    examples: list[str] = Field(default_factory=list, description="例句")
    avoid: list[str] = Field(default_factory=list, description="應避免的說法")


class References(BaseModel):
    """外部參考連結"""
    mitre_attack: Optional[str] = None
    nist: Optional[str] = None
    cwe: Optional[str] = None
    owasp: Optional[str] = None
    wikipedia: Optional[str] = None
    other: dict[str, str] = Field(default_factory=dict)


class Metadata(BaseModel):
    """元資料"""
    status: TermStatus = Field(TermStatus.APPROVED, description="術語狀態")
    created: Optional[date] = Field(None, description="建立日期")
    updated: Optional[date] = Field(None, description="更新日期")
    source: Optional[str] = Field(None, description="來源")
    contributors: list[str] = Field(default_factory=list, description="貢獻者")


class Term(BaseModel):
    """資安術語"""
    
    # === 基本資訊 ===
    id: str = Field(..., description="唯一識別碼，小寫底線分隔")
    term_en: str = Field(..., description="英文術語")
    term_zh: str = Field(..., description="中文術語")
    full_name_en: Optional[str] = Field(None, description="英文全稱")
    full_name_zh: Optional[str] = Field(None, description="中文全稱")
    
    # === 定義 ===
    definitions: Definitions
    
    # === 分類 ===
    category: str = Field(..., description="主分類")
    subcategory: Optional[str] = Field(None, description="子分類")
    tags: list[str] = Field(default_factory=list, description="標籤")
    
    # === 關聯 ===
    related_terms: list[str] = Field(default_factory=list, description="相關術語 ID")
    see_also: list[str] = Field(default_factory=list, description="延伸閱讀術語 ID")
    
    # === 別名 ===
    aliases: Aliases = Field(default_factory=Aliases)
    
    # === 使用指南 ===
    usage: Usage = Field(default_factory=Usage)
    
    # === 參考 ===
    references: References = Field(default_factory=References)
    
    # === 元資料 ===
    metadata: Metadata = Field(default_factory=Metadata)
    
    def get_all_names(self) -> list[str]:
        """取得所有名稱（含別名），用於比對"""
        names = [self.term_en, self.term_zh]
        if self.full_name_en:
            names.append(self.full_name_en)
        if self.full_name_zh:
            names.append(self.full_name_zh)
        names.extend(self.aliases.en)
        names.extend(self.aliases.zh)
        return list(set(names))
    
    def to_markdown_link(self, base_url: str = "") -> str:
        """產生 Markdown 連結"""
        return f"[{self.term_zh}]({base_url}/glossary/{self.id} \"{self.definitions.brief}\")"
    
    def to_html_span(self) -> str:
        """產生 HTML span（含 tooltip）"""
        return (
            f'<span class="term" data-term-id="{self.id}" '
            f'title="{self.definitions.brief}">{self.term_zh}</span>'
        )


class Category(BaseModel):
    """術語分類"""
    id: str
    name_en: str
    name_zh: str
    description: Optional[str] = None
    subcategories: list[str] = Field(default_factory=list)
    icon: Optional[str] = None


class StyleRule(BaseModel):
    """用詞風格規則"""
    avoid: str = Field(..., description="應避免的用詞")
    preferred: str = Field(..., description="建議用詞")
    reason: Optional[str] = Field(None, description="原因說明")


class ValidationIssue(BaseModel):
    """驗證問題"""
    line: int = Field(..., description="行號")
    column: Optional[int] = Field(None, description="欄號")
    text: str = Field(..., description="問題文字")
    issue_type: str = Field(..., description="問題類型")
    suggestion: str = Field(..., description="建議修正")
    severity: str = Field("warning", description="嚴重程度: error, warning, info")


class TermMatch(BaseModel):
    """術語比對結果"""
    term_id: str
    term: Term
    matched_text: str
    start: int
    end: int
    confidence: float = Field(1.0, ge=0, le=1)
