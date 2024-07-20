"""Multi Tokenizer Module."""

import pickle

from multi_tokenizer.pretrained import LanguageSpecificTokenizer

from tokenizers import Encoding


class MultiTokenizer:
    """MultiTokenizer Class."""

    def __init__(self, tokenizers: list[LanguageSpecificTokenizer]) -> None:
        """Initialize MultiTokenizer."""
        self.tokenizers = tokenizers

    def encode(self, text: str) -> Encoding:
        """Encode Text."""
        raise NotImplementedError

    def decode(self, encoding: Encoding) -> str:
        """Decode Encoding."""
        raise NotImplementedError

    def save(self, path: str) -> None:
        """Save Tokenizer."""
        with open(path, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load(path: str) -> "MultiTokenizer":
        """Load Tokenizer."""
        with open(path, "rb") as file:
            return pickle.load(file)
