from typing import TypedDict, Literal, List

ModelName = Literal["gemini/gemini-1.5-flash", "gemini/gemini-1.5-pro", "gemini/gemini-2.0-flash"]
TestFramework = Literal["unittest", "pytest"]  
DocstringStyle = Literal["google", "numpy"]

class ChatMessage(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str

Messages = List[ChatMessage]
