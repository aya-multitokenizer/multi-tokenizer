"""Multi Tokenizer Module."""

import pickle
from typing import Any

from lingua import Language

from multi_tokenizer.language_detect import LanguageDetector
from multi_tokenizer.pretrained import LanguageSpecificTokenizer, PretrainedTokenizers


class MultiTokenizer:
    """MultiTokenizer Class."""

    def __init__(
        self,
        tokenizers: list[LanguageSpecificTokenizer | PretrainedTokenizers],
        fallback_tokenizer: Any = None,
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
        self.fallback_tokenizer = (
            self.tokenizers[0] if fallback_tokenizer is None else fallback_tokenizer
        )
        self.language_prefix_token_ids = [
            tokenizer.language_prefix_token[1] for tokenizer in self.tokenizers
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
        last_end_index = 0
        for detection in language_detections:
            # If there is text between the last detected language and the current one
            if detection.start_index != last_end_index:
                pre_tokenized_text.append(
                    (
                        text[last_end_index : detection.start_index],
                        (last_end_index, detection.start_index),
                    )
                )
            detected_text = text[detection.start_index : detection.end_index]
            last_end_index = detection.end_index
            tokenizer = self.get_tokenizer_by_language(detection.language)
            output: list[tuple[str, tuple[int, int]]] = (
                tokenizer.tokenizer.pre_tokenizer.pre_tokenize_str(detected_text)
            )
            output = (
                [(tokenizer.language_prefix_token[0], (-1, 0))]
                + output
                + [
                    (
                        tokenizer.language_suffix_token[0],
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
        # If there is text after the last detected language
        if last_end_index < len(text):
            pre_tokenized_text.append(
                (text[last_end_index:], (last_end_index, len(text)))
            )
        return pre_tokenized_text

    def get_tokenizer_by_language(
        self, language: Language
    ) -> LanguageSpecificTokenizer:
        """Get Tokenizer for Language."""
        for tokenizer in self.tokenizers:
            if tokenizer.language == language:
                return tokenizer
        raise ValueError(f"Tokenizer for {language} not found.")

    def get_tokenizer_by_prefix(self, prefix: str) -> LanguageSpecificTokenizer:
        """Get Tokenizer by Prefix."""
        for tokenizer in self.tokenizers:
            if tokenizer.language_prefix_token[0] == prefix:
                return tokenizer
        raise ValueError(f"Tokenizer for prefix {prefix} not found.")

    def get_tokenizer_by_prefix_id(self, prefix_id: int) -> LanguageSpecificTokenizer:
        """Get Tokenizer by Prefix ID."""
        for tokenizer in self.tokenizers:
            if tokenizer.language_prefix_token[1] == prefix_id:
                return tokenizer
        raise ValueError(f"Tokenizer for prefix ID {prefix_id} not found.")

    def encode(self, text: str) -> tuple[list[int], list[str]]:
        """Encode Text."""
        ids = []
        tokens = []
        language_detections = (
            self.language_detector.detect(text)
            if not self.split_text
            else self.language_detector.split_n_detect(text, self.sep)
        )
        last_end_index = 0
        for detection in language_detections:
            if detection.start_index != last_end_index:
                encoding = self.fallback_tokenizer.encode(
                    text[last_end_index : detection.start_index]
                )
                ids.extend(encoding.ids)
                tokens.extend(encoding.tokens)
            detected_text = text[detection.start_index : detection.end_index]
            tokenizer = self.get_tokenizer_by_language(detection.language)
            detected_text = (
                tokenizer.language_prefix_token[0]
                + detected_text
                + tokenizer.language_suffix_token[0]
            )
            encoding = tokenizer.tokenizer.encode(detected_text)
            ids.extend(encoding.ids)
            tokens.extend(encoding.tokens)
            last_end_index = detection.end_index
        if last_end_index < len(text):
            encoding = self.fallback_tokenizer.encode(text[last_end_index:])
            ids.extend(encoding.ids)
            tokens.extend(encoding.tokens)
        return ids, tokens

    def decode(self, token_ids: list[int]) -> str:
        """Decode Encoding."""
        decoded_str = []
        cur_tokenizer = None
        i, j = 0, 0
        while i < len(token_ids):
            if token_ids[i] in self.language_prefix_token_ids:
                cur_tokenizer = self.get_tokenizer_by_prefix_id(token_ids[i])
                j = i + 1
                while token_ids[j] != cur_tokenizer.language_suffix_token[1]:
                    j += 1
                decoded_str.append(cur_tokenizer.decode(token_ids[i : j + 1]))
                i = j + 1
            else:
                while (
                    j < len(token_ids)
                    and token_ids[j] not in self.language_prefix_token_ids
                ):
                    j += 1
                decoded_str.append(self.fallback_tokenizer.decode(token_ids[i:j]))
                i = j
        return "".join(decoded_str)

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
        return max(len(vocab[language]) for language in vocab)
