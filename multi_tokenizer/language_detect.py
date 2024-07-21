"""Language Detection Module."""

from lingua import DetectionResult, Language, LanguageDetectorBuilder


class LanguageDetector:
    """Language Detector."""

    def __init__(self, languages: list[Language]) -> None:
        """Initialize Language Detector."""
        self.languages = languages
        self.detector = LanguageDetectorBuilder.from_languages(*languages).build()

    def detect(self, text: str) -> list[DetectionResult]:
        """Detect Language."""
        results = self.detector.detect_multiple_languages_of(text)
        return results

    def batch_detect(self, texts: list[str]) -> list[list[DetectionResult]]:
        """Detect Language in Batch."""
        results = self.detector.detect_multiple_languages_in_parallel_of(texts)
        return results
