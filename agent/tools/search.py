"""Web search integration using Tavily."""

from typing import List
from dataclasses import dataclass
from tavily import TavilyClient
from config import get_settings
from logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class SearchResult:
    """Search result from web search."""

    title: str
    url: str
    content: str


class SearchClient:
    """Tavily web search client."""

    def __init__(self):
        """Initialize search client."""
        settings = get_settings()
        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)
        self.max_results = settings.SEARCH_MAX_RESULTS
        self.search_depth = settings.SEARCH_DEPTH

    async def search(self, query: str, max_results: int = None) -> List[SearchResult]:
        """Search the web using Tavily.
        
        Args:
            query: Search query
            max_results: Maximum number of results (uses config default if not specified)
            
        Returns:
            List of search results
        """
        try:
            max_results = max_results or self.max_results
            logger.info(f"[Search] Searching for: {query}")

            response = self.client.search(
                query,
                search_depth=self.search_depth,
                max_results=max_results,
                include_answer=True
            )

            results = [
                SearchResult(
                    title=r.get("title", ""),
                    url=r.get("url", ""),
                    content=r.get("content", "")
                )
                for r in response.get("results", [])
            ]

            logger.info(f"[Search] Found {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"[Search] Error: {str(e)}")
            return []

    @staticmethod
    def format_results_for_prompt(results: List[SearchResult]) -> str:
        """Format search results for use in LLM prompts.
        
        Args:
            results: Search results to format
            
        Returns:
            Formatted string for prompts
        """
        if not results:
            return ""

        formatted = "## Web Search Results\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"### {i}. {result.title}\n"
            formatted += f"**URL:** {result.url}\n"
            formatted += f"**Content:** {result.content}\n\n"

        return formatted


# Singleton instance
_search_client: SearchClient = None


def get_search_client() -> SearchClient:
    """Get search client singleton."""
    global _search_client
    if _search_client is None:
        _search_client = SearchClient()
    return _search_client
