from openai import OpenAI
from typing import Generator
import tiktoken

from config import config


class ChatService:
    """Service for handling chat interactions with OpenAI API"""

    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.MODEL_NAME
        self.max_tokens = config.MAX_TOKENS
        self.temperature = config.TEMPERATURE

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text string"""
        try:
            encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))

    def count_messages_tokens(self, messages: list) -> int:
        """Count total tokens in a list of messages"""
        total = 0
        for message in messages:
            total += self.count_tokens(message.get("content", ""))
            total += 4  # overhead per message
        return total

    def chat(self, messages: list, system_prompt: str = None) -> str:
        """
        Send a chat request to OpenAI and get a response

        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: Optional system prompt to prepend

        Returns:
            The assistant's response text
        """
        full_messages = []

        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})

        full_messages.extend(messages)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        return response.choices[0].message.content

    def chat_stream(self, messages: list, system_prompt: str = None) -> Generator[str, None, None]:
        """
        Send a chat request and stream the response

        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: Optional system prompt to prepend

        Yields:
            Chunks of the assistant's response
        """
        full_messages = []

        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})

        full_messages.extend(messages)

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content


chat_service = ChatService()
