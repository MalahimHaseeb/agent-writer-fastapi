"""Writer node - generates blog draft."""

from agent import AgentState
from agent.tools import get_gemini_client
from logger import setup_logger

logger = setup_logger(__name__)


async def writer_node(state: AgentState) -> AgentState:
    """Writer node - generates the blog post draft.
    
    Creates an initial blog post draft based on the topic and
    any available search results.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with generated draft
    """
    logger.info("[Writer] Drafting blog post...")

    # Prepare research context for the writer
    research_section = ""
    if state.search_results and len(state.search_results[0]) > 10:
        research_section = f"Use this web research to inform the post:\n\n{state.search_results[0]}"
    else:
        research_section = "Write from your general knowledge."

    prompt = f"""You are an expert blog writer. Write a comprehensive, engaging blog post.

Topic: "{state.topic}"

{research_section}

Requirements:
- Write in Markdown format
- Include a compelling H1 title
- Add a short introduction that hooks the reader
- Use H2 and H3 headings to organize content
- Include practical examples or code snippets where relevant
- Write at least 600 words
- End with a clear conclusion and key takeaways
- Use a conversational but authoritative tone
- Do NOT include "Introduction" or "Conclusion" as headings — use creative headings
- If you use facts from the research, reference sources naturally in the text

Write the full blog post now:"""

    try:
        client = get_gemini_client()
        draft = await client.generate_text(prompt)
        logger.info(f"[Writer] Draft written ({len(draft)} characters)")
        return state.update(draft=draft)
    except Exception as e:
        logger.error(f"[Writer] Error: {str(e)}")
        return state.update(error="Failed to generate draft")
