"""Formatter node - extracts metadata and formats output."""

import json
from agent import AgentState, BlogMeta
from agent.tools import get_gemini_client
from logger import setup_logger

logger = setup_logger(__name__)


def estimate_reading_time(text: str) -> int:
    """Estimate reading time in minutes.
    
    Args:
        text: Blog content
        
    Returns:
        Estimated reading time in minutes
    """
    words = len(text.strip().split())
    # Average reading speed: ~200 words per minute
    return max(1, round(words / 200))


def count_words(text: str) -> int:
    """Count words in text.
    
    Args:
        text: Text to count
        
    Returns:
        Word count
    """
    return len(text.strip().split())


async def formatter_node(state: AgentState) -> AgentState:
    """Formatter node - extracts metadata and finalizes output.
    
    Extracts metadata like title, description, tags from the blog
    and calculates reading time and word count.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with extracted metadata
    """
    logger.info("[Formatter] Extracting metadata...")

    blog = state.final_blog or state.draft
    if not blog:
        logger.warning("[Formatter] No content to format")
        return state.update(error="No content to format")

    # Calculate metrics
    word_count = count_words(blog)
    reading_time = estimate_reading_time(blog)

    # Extract metadata using LLM
    meta_prompt = f"""From this blog post, extract metadata. Respond ONLY with valid JSON, no markdown fences.

Blog post:
{blog[:2000]}

Return this exact JSON structure:
{{
  "title": "the blog post title (from H1 or infer from content)",
  "description": "a 1-2 sentence SEO meta description",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
}}"""

    try:
        client = get_gemini_client()
        meta_raw = await client.generate_text(meta_prompt)

        # Clean and parse JSON
        cleaned = meta_raw.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(cleaned)

        meta = BlogMeta(
            title=parsed.get("title", state.topic),
            description=parsed.get("description", ""),
            tags=parsed.get("tags", [])[:6],  # Limit to 6 tags
            reading_time=reading_time,
            word_count=word_count,
        )

        logger.info(f"[Formatter] Metadata extracted: '{meta.title}'")
        return state.update(meta=meta, final_blog=blog)

    except json.JSONDecodeError as e:
        logger.warning(f"[Formatter] Failed to parse JSON: {str(e)}, using fallback metadata")
        # Fallback metadata
        meta = BlogMeta(
            title=state.topic,
            description="",
            tags=[],
            reading_time=reading_time,
            word_count=word_count,
        )
        return state.update(meta=meta, final_blog=blog)
    except Exception as e:
        logger.error(f"[Formatter] Error: {str(e)}")
        # Return with basic metadata
        meta = BlogMeta(
            title=state.topic,
            description="",
            tags=[],
            reading_time=reading_time,
            word_count=word_count,
        )
        return state.update(meta=meta, final_blog=blog)
