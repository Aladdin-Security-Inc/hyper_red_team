# src/llm_client.py
import asyncio
from groq import AsyncGroq
import re

class LLMClient:
    """
    A client for interacting with the Groq API to generate code.
    """
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = AsyncGroq(api_key=api_key)

    async def generate_code(self, prompt: str) -> tuple[str, str]:
        """
        Generates code using the specified model and prompt.

        Args:
            prompt: The prompt to send to the LLM.

        Returns:
            A tuple containing the extracted code block and the full response text.
        """
        try:
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_name,
                temperature=0.5, # Encourage some creativity but not too much
                max_tokens=2048,
                top_p=1,
                stop=None,
            )
            response_text = chat_completion.choices[0].message.content
            code_block = self._extract_code_block(response_text)
            return code_block, response_text
        except Exception as e:
            print(f"An error occurred while calling the Groq API: {e}")
            return "", f"Error: {e}"

    def _extract_code_block(self, text: str) -> str:
        """
        Extracts the first Python code block from a markdown-formatted string.
        """
        match = re.search(r"```python\n(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        # Fallback for cases where the block is not perfectly formatted
        if "```" in text:
            return text.split("```")[1].strip()
        return text # Return the whole text if no block is found

