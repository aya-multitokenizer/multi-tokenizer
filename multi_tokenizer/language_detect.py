"""Language Detection Module."""


class LanguageDetector:
    """Language Detector."""

    def __init__(self, language: str) -> None:
        """Initialize Language Detector."""
        self.language = language

    def detect(self, text: str) -> list[tuple[int, int]]:
        """Detect Language."""
        raise NotImplementedError


class EnglishDetector(LanguageDetector):
    """English Language Detector."""

    def __init__(self) -> None:
        """Initialize English Detector."""
        super().__init__("en")

    def detect(self, text: str) -> list[tuple[int, int]]:
        """Detect English."""
        return [(0, int(len(text) / 2) - 1), (int(len(text) / 2), len(text) - 1)]


class SpanishDetector(LanguageDetector):
    """Spanish Language Detector."""

    def __init__(self) -> None:
        """Initialize Spanish Detector."""
        super().__init__("es")

    def detect(self, text: str) -> list[tuple[int, int]]:
        """Detect Spanish."""
        return [(0, int(len(text) / 2) - 1), (int(len(text) / 2), len(text) - 1)]


class CantoneseDetector(LanguageDetector):
    """Cantonese Language Detector."""

    def __init__(self) -> None:
        """Initialize Cantonese Detector."""
        super().__init__("zh")

    def detect(self, text: str) -> list[tuple[int, int]]:
        """Detect Cantonese."""
        return [(0, int(len(text) / 2) - 1), (int(len(text) / 2), len(text) - 1)]


class HindiDetector(LanguageDetector):
    """Hindi Language Detector."""

    def __init__(self) -> None:
        """Initialize Hindi Detector."""
        super().__init__("hi")

    def detect(self, text: str) -> list[tuple[int, int]]:
        """Detect Hindi."""
        return [(0, int(len(text) / 2) - 1), (int(len(text) / 2), len(text) - 1)]
