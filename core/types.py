from typing import TypedDict, Literal, List

ModelName = Literal["gpt-3.5-turbo", "o3-mini", "gpt-4o-mini", "gpt-4o"]
TestFramework = Literal["unittest", "pytest"]  
DocstringStyle = Literal["google", "numpy"]

class ChatMessage(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str

Messages = List[ChatMessage]
