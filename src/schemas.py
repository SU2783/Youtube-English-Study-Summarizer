from typing_extensions import TypedDict


class Description(TypedDict):
    timestamp: list[str]
    sentence: list[str]
    transcription: list[str]
    explanation: list[list[str]]