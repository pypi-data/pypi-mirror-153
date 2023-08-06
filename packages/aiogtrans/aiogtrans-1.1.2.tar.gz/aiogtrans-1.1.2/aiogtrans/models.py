from httpx import Response
from aiohttp import ClientResponse
import typing


class Base:
    """
    Base class for response objects such as Translated and Detected
    """

    def __init__(self, response: typing.Union[Response, ClientResponse] = None):
        self._response = response


class TranslatedPart:
    """Translated parts"""

    def __init__(self, text: str, candidates: typing.List[str]) -> None:
        """
        Init for translated parts
        """
        self.text = text
        self.candidates = candidates

    def __str__(self) -> str:
        return self.text

    def __dict__(self) -> dict:
        return {
            "text": self.text,
            "candidates": self.candidates,
        }


class Translated(Base):
    """Translate result object

    :param src: source language (default: auto)
    :param dest: destination language (default: en)
    :param origin: original text
    :param text: translated text
    :param pronunciation: pronunciation
    """

    def __init__(
        self,
        src: str,
        dest: str,
        origin: str,
        text: str,
        pronunciation: str,
        parts: typing.List[TranslatedPart],
        extra_data=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.src = src
        self.dest = dest
        self.origin = origin
        self.text = text
        self.pronunciation = pronunciation
        self.parts = parts
        self.extra_data = extra_data

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return f"Translated(src={self.src}, dest={self.dest}, text={self.text}, pronunciation={self.pronunciation}, extra_data={repr(self.extra_data)[:10]}...)"

    def __dict__(self):
        return {
            "src": self.src,
            "dest": self.dest,
            "origin": self.origin,
            "text": self.text,
            "pronunciation": self.pronunciation,
            "extra_data": self.extra_data,
            "parts": list(map(lambda part: part.__dict__(), self.parts)),
        }


class Detected(Base):
    """Language detection result object

    :param lang: detected language
    :param confidence: the confidence of detection result (0.00 to 1.00)
    """

    def __init__(self, lang: str, confidence: float, **kwargs) -> None:
        """Initiation for detected object"""
        super().__init__(**kwargs)
        self.lang = lang
        self.confidence = confidence

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return f"Detected(lang={self.lang}, confidence={self.confidence})"
