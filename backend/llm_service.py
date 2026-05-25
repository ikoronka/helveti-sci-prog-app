import logging
import os

from google import genai

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self) -> None:
        self.client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    def generate_conclusion(
        self,
        city: str,
        bhk: int,
        n_samples: int,
        slope: float,
        r_squared: float,
        p_value: float,
    ) -> str:
        prompt = (
            f"You are a data analyst summarizing a regression analysis of Indian housing data.\n\n"
            f"Context:\n"
            f"- City: {city}\n"
            f"- BHK (bedrooms): {bhk}\n"
            f"- Number of listings analyzed: {n_samples}\n"
            f"- Regression of Rent (₹) on Size (sqft): slope = {slope:.2f} ₹/sqft\n"
            f"- R² = {r_squared:.3f}, p-value = {p_value:.4f}\n\n"
            f"Write a concise 2-3 sentence research conclusion. "
            f"Interpret statistical significance, effect size, and practical meaning. "
            f"Do not repeat the raw numbers verbatim — synthesize them."
        )
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite", contents=prompt
            )
            text = response.text or ""
            if not text.strip():
                return "The model returned an empty response. Please try again."
            return text
        except Exception as e:
            logger.error("LLM call failed: %s", e)
            return "AI insight is temporarily unavailable. Please try again later."
