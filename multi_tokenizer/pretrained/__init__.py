"""Pretrained Tokenizers for Specific Languages."""

import os
from enum import Enum
from typing import Any

from lingua import Language

from tokenizers import Tokenizer


file_dir = os.path.dirname(__file__)


class LanguageSpecificTokenizer:
    """Language Specific Tokenizer."""

    def __init__(
        self,
        tokenizer_path: str,
        language: Language,
        language_prefix: tuple[str, int],
        language_suffix: tuple[str, int],
    ) -> None:
        """Initialize Language Specific Tokenizer."""
        self.language = language
        self.language_prefix_token = language_prefix
        self.language_suffix_token = language_suffix
        self.tokenizer = Tokenizer.from_file(tokenizer_path)

    @property
    def pre_tokenizer(self) -> Any:
        """Get Pre Tokenizer."""
        return self.tokenizer.pre_tokenizer

    def encode(self, text: str) -> list[int]:
        """Get Encoder."""
        return self.tokenizer.encode(text).ids

    def tokenize(self, text: str) -> list[str]:
        """Tokenize Text."""
        return self.tokenizer.encode(text).tokens

    def decode(self, ids: list[int]) -> str:
        """Decode Text."""
        return self.tokenizer.decode(ids)

    def get_vocab(self) -> dict[str, int]:
        """Get Vocab."""
        return self.tokenizer.get_vocab()


class PretrainedTokenizers(Enum):
    """Pretrained Tokenizers for Specific Languages."""

    ENGLISH = LanguageSpecificTokenizer(
        os.path.join(file_dir, "english_tokenizer.json"),
        Language.ENGLISH,
        ("<EN>", 3),
        ("</EN>", 4),
    )
    SPANISH = LanguageSpecificTokenizer(
        os.path.join(file_dir, "spanish_tokenizer.json"),
        Language.SPANISH,
        ("<ES>", 5),
        ("</ES>", 6),
    )
    CHINESE = LanguageSpecificTokenizer(
        os.path.join(file_dir, "chinese_tokenizer.json"),
        Language.CHINESE,
        ("<ZH>", 7),
        ("</ZH>", 8),
    )
    HINDI = LanguageSpecificTokenizer(
        os.path.join(file_dir, "hindi_tokenizer.json"),
        Language.HINDI,
        ("<HI>", 9),
        ("</HI>", 10),
    )


def get_tokenizer_by_language(language: Language) -> LanguageSpecificTokenizer:
    """Get Tokenizer for Language."""
    for tokenizer in PretrainedTokenizers:
        if tokenizer.value.language == language:
            return tokenizer.value
    raise ValueError(f"Tokenizer for language {language} not found.")


__all__ = ["PretrainedTokenizers"]
