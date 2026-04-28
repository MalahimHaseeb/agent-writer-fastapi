"""Agent state definition."""

from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BlogMeta:
    """Blog post metadata."""

    title: str
    description: str
    tags: List[str]
    reading_time: int
    word_count: int


@dataclass
class AgentState:
    """Blog writing agent state.
    
    This represents the mutable state passed through the agent workflow.
    """

    topic: str
    session_id: str
    search_results: List[str] = field(default_factory=list)
    needs_search: bool = True
    draft: str = ""
    final_blog: str = ""
    meta: Optional[BlogMeta] = None
    error: Optional[str] = None

    def update(self, **kwargs) -> "AgentState":
        """Create a new state with updated values."""
        return AgentState(
            topic=kwargs.get("topic", self.topic),
            session_id=kwargs.get("session_id", self.session_id),
            search_results=kwargs.get("search_results", self.search_results),
            needs_search=kwargs.get("needs_search", self.needs_search),
            draft=kwargs.get("draft", self.draft),
            final_blog=kwargs.get("final_blog", self.final_blog),
            meta=kwargs.get("meta", self.meta),
            error=kwargs.get("error", self.error),
        )


@dataclass
class GraphOutput:
    """Output from running the agent graph."""

    final_blog: str
    meta: Optional[BlogMeta]
    error: Optional[str]
