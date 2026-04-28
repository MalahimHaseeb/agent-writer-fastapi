import google.generativeai as genai
from config import get_settings
from logger import setup_logger

logger = setup_logger(__name__)


class GeminiClient:

    def __init__(self):
        settings = get_settings()
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.LLM_MODEL
        self.timeout = settings.LLM_TIMEOUT

    async def generate_text(self, prompt: str) -> str:
        try:
            logger.info(f"[Gemini] Generating text with model: {self.model_name}")
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(
                prompt,
                generation_config={"temperature": 0.7}
            )
            text = response.text
            logger.debug(f"[Gemini] Generated {len(text)} characters")
            return text
        except Exception as e:
            logger.error(f"[Gemini] Error: {str(e)}")
            raise Exception(f"Failed to generate text: {str(e)}")


_gemini_client: GeminiClient = None


def get_gemini_client() -> GeminiClient:
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client
