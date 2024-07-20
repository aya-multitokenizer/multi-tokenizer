"""Pretrained Tokenizers for Specific Languages."""

import os
from enum import Enum
from typing import Callable

from multi_tokenizer.language_detect import (
    CantoneseDetector,
    EnglishDetector,
    HindiDetector,
    LanguageDetector,
    SpanishDetector,
)

from tokenizers import Tokenizer


file_dir = os.path.dirname(__file__)


class LanguageSpecificTokenizer:
    """Language Specific Tokenizer."""

    def __init__(
        self, tokenizer_path: str, language_detector: LanguageDetector | None = None
    ) -> None:
        """Initialize Language Specific Tokenizer."""
        self.language_detector = language_detector
        self.tokenizer = Tokenizer.from_file(tokenizer_path)

    def __getattr__(self, name: str) -> Callable:
        """Get Attribute."""
        return getattr(self.tokenizer, name)


class PretrainedTokenizers(Enum):
    """Pretrained Tokenizers for Specific Languages."""

    ENGLISH = LanguageSpecificTokenizer(
        os.path.join(file_dir, "english_tokenizer.json"), EnglishDetector()
    )
    SPANISH = LanguageSpecificTokenizer(
        os.path.join(file_dir, "spanish_tokenizer.json"), SpanishDetector()
    )
    CANTONESE = LanguageSpecificTokenizer(
        os.path.join(file_dir, "cantonese_tokenizer.json"), CantoneseDetector()
    )
    HINDI = LanguageSpecificTokenizer(
        os.path.join(file_dir, "hindi_tokenizer.json"), HindiDetector()
    )


__all__ = ["PretrainedTokenizers"]
