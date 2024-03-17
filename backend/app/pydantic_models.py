from pydantic import BaseModel
from typing import Optional


class PromptTemplate(BaseModel):
    question: Optional[str] = None
    chat_history: list
