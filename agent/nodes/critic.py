"""Critic node - reviews and improves blog draft."""

from agent import AgentState
from agent.tools import get_gemini_client
from logger import setup_logger

logger = setup_logger(__name__)


async def critic_node(state: AgentState) -> AgentState:
    """Critic node - reviews and polishes the blog draft.
    
    Performs editorial review and improvement on the generated draft,
    enhancing quality, flow, and overall impact.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with finalized blog post
    """
    logger.info("[Critic] Reviewing draft...")

    if not state.draft:
        logger.warning("[Critic] No draft to review")
        return state.update(final_blog="", error="No draft to review")

    prompt = f"""You are a senior editor reviewing a blog post draft. Your job is to improve it and return the final polished version.

Original draft:
{state.draft}

Review and improve the draft by:
1. Strengthening the opening hook
2. Improving flow and transitions between sections
3. Making sure every section adds clear value
4. Sharpening the conclusion
5. Fixing any grammar or clarity issues
6. Ensuring the tone is consistent throughout
7. Adding any missing important points about the topic

IMPORTANT: Return ONLY the improved blog post in Markdown. Do not add commentary, ratings, or notes — just the final post."""

    try:
        client = get_gemini_client()
        final_blog = await client.generate_text(prompt)
        logger.info(f"[Critic] Final blog ready ({len(final_blog)} characters)")
        return state.update(final_blog=final_blog)
    except Exception as e:
        logger.error(f"[Critic] Error, using draft as final: {str(e)}")
        # Fall back to draft if critic fails
        return state.update(final_blog=state.draft)
