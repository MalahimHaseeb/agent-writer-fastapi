"""Agent graph nodes."""

from agent import AgentState
from agent.tools import get_gemini_client
from logger import setup_logger

logger = setup_logger(__name__)


async def router_node(state: AgentState) -> AgentState:
    """Router node - decides if web search is needed.
    
    Analyzes the topic to determine if current web research is required
    or if the blog can be written from general knowledge.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with needs_search decision
    """
    prompt = f"""You are a routing agent. Decide if writing a blog post about this topic requires current web research or if it can be written from general knowledge.

Topic: "{state.topic}"

Rules:
- Answer SEARCH if the topic involves recent events, statistics, news, specific tools/products, or anything time-sensitive
- Answer SKIP if it's a timeless concept, tutorial, or something that doesn't need current data

Respond with ONLY one word: SEARCH or SKIP"""

    try:
        client = get_gemini_client()
        decision = await client.generate_text(prompt)
        needs_search = "SEARCH" in decision.upper()
        logger.info(f"[Router] Topic: '{state.topic}' → {'SEARCH' if needs_search else 'SKIP'}")
        return state.update(needs_search=needs_search)
    except Exception as e:
        logger.error(f"[Router] Error: {str(e)}, defaulting to search")
        return state.update(needs_search=True)
