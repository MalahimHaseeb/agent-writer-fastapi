"""Search node - performs web search."""

from agent import AgentState
from agent.tools.search import get_search_client
from logger import setup_logger

logger = setup_logger(__name__)


async def search_node(state: AgentState) -> AgentState:
    """Search node - performs web research if needed.
    
    Executes web search queries to gather current information
    about the topic for the writer to reference.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with search results or empty results if search not needed
    """
    if not state.needs_search:
        logger.info("[Search] Skipping web search")
        return state.update(search_results=[])

    try:
        search_client = get_search_client()
        logger.info(f"[Search] Searching for: '{state.topic}'")

        # Perform two searches for broader coverage
        primary_results = await search_client.search(state.topic, max_results=4)
        recent_results = await search_client.search(
            f"{state.topic} latest 2026",
            max_results=3
        )

        all_results = primary_results + recent_results

        # Format results for LLM prompt
        formatted = search_client.format_results_for_prompt(all_results)

        logger.info(f"[Search] Found {len(all_results)} total results")
        return state.update(search_results=[formatted])

    except Exception as e:
        logger.error(f"[Search] Error: {str(e)}")
        return state.update(
            search_results=[],
            error="Web search failed, proceeding without it"
        )
