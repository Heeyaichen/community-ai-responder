from typing import Optional
from openai import OpenAI

from app.config import get_settings


class LLMService:
    def __init__(self):
        self.settings = get_settings()
        self.client: Optional[OpenAI] = None
        self._init_client()

    def _init_client(self):
        if self.settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=self.settings.OPENAI_API_KEY)

    def generate(self, prompt: str) -> str:
        if not self.client:
            raise ValueError("OpenAI API key not configured")

        response = self.client.chat.completions.create(
            model=self.settings.OPENAI_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,
        )

        return response.choices[0].message.content

    def generate_with_context(
        self,
        post_content: str,
        category: Optional[str] = None,
        author: Optional[str] = None,
    ) -> str:
        context_parts = [f"Post by: {author}" if author else "", f"Category: {category}" if category else "", f"\nContent:\n{post_content}"]

        full_prompt = "\n".join(context_parts)

        return self.generate(full_prompt)
