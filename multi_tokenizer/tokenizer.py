"""Multi Tokenizer Module."""

import pickle

from multi_tokenizer.language_detect import LanguageDetector
from multi_tokenizer.pretrained import (
    LanguageSpecificTokenizer,
    PretrainedTokenizers,
    get_tokenizer_by_language,
)

from tokenizers import Encoding


class MultiTokenizer:
    """MultiTokenizer Class."""

    def __init__(
        self,
        tokenizers: list[LanguageSpecificTokenizer | PretrainedTokenizers],
        split_text: bool = False,
        sep: str = " ",
    ) -> None:
        """Initialize MultiTokenizer."""
        self.tokenizers = [
            (
                tokenizer
                if isinstance(tokenizer, LanguageSpecificTokenizer)
                else tokenizer.value
            )
            for tokenizer in tokenizers
        ]
        self.language_detector = LanguageDetector(
            [tokenizer.language for tokenizer in self.tokenizers]
        )
        self.split_text = split_text
        self.sep = sep

    def pre_tokenize(self, text: str) -> list[tuple[str, tuple[int, int]]]:
        """Pre Tokenize Text."""
        pre_tokenized_text = []
        language_detections = (
            self.language_detector.detect(text)
            if not self.split_text
            else self.language_detector.split_n_detect(text, self.sep)
        )
        for detection in language_detections:
            detected_text = text[detection.start_index : detection.end_index]
            tokenizer = get_tokenizer_by_language(detection.language)
            output: list[tuple[str, tuple[int, int]]] = (
                tokenizer.tokenizer.pre_tokenizer.pre_tokenize_str(detected_text)
            )
            output = (
                [(tokenizer.language_prefix_token, (-1, 0))]
                + output
                + [
                    (
                        tokenizer.language_suffix_token,
                        (len(detected_text) - 2, len(detected_text) - 1),
                    )
                ]
            )
            # Offsetting the start and end indices of the tokens to match the original text
            output = [
                (
                    token,
                    (
                        start + detection.start_index + 1,
                        end + detection.start_index + 1,
                    ),
                )
                for token, (start, end) in output
            ]
            pre_tokenized_text.extend(output)
        return pre_tokenized_text

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

    def get_vocab(self) -> dict[str, dict[str, int]]:
        """Get Vocabulary."""
        vocab = {}
        for tokenizer in self.tokenizers:
            vocab[tokenizer.language.name] = tokenizer.get_vocab()
        return vocab

    def get_vocab_size(self) -> int:
        """Get Vocabulary Size."""
        vocab = self.get_vocab()
        return sum(
            len(vocab[language]) for language in vocab
        )  # TODO: This is probably wrong
