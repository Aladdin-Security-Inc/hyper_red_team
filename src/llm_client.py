# src/llm_client.py
import asyncio
from groq import AsyncGroq
import re
import os

class LLMClient:
    """
    A client for interacting with the Groq API.
    """
    def __init__(self, model_name: str, api_key: str = None):
        if api_key is None:
            api_key = os.getenv("GROQ_API_KEY")
        if api_key is None:
            raise ValueError("GROQ_API_KEY must be provided or set as an environment variable.")
        
        self.model_name = model_name
        self.async_client = AsyncGroq(api_key=api_key)

    async def generate_code(self, prompt: str) -> tuple[str, str]:
        """
        Asynchronously generates code and extracts the code block.
        """
        try:
            chat_completion = await self.async_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
                temperature=0.2, # Lower temperature for more deterministic results
                max_tokens=2048,
            )
            response_text = chat_completion.choices[0].message.content
            return response_text, response_text # Return the full response and let the harness extract
        except Exception as e:
            print(f"An error occurred while calling the Groq API: {e}")
            return f"Error: {e}", f"Error: {e}"
