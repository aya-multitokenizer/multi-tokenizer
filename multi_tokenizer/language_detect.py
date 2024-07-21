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

    def split_n_detect(self, text: str, sep: str = " ") -> list[DetectionResult]:
        """Split Text and Detect Language."""

        def merge_results(
            results: list[list[DetectionResult]],
        ) -> list[DetectionResult]:
            """Merge Results. If consecutive words are detected as the same language, merge them."""
            merged_results: list[DetectionResult] = []
            for result in results:
                if not merged_results:
                    merged_results.extend(result)
                else:
                    for detection in result:
                        last_result = merged_results[-1]
                        if detection.language == last_result.language:
                            merged_results[-1] = DetectionResult(
                                language=last_result.language,
                                start_index=last_result.start_index,
                                end_index=last_result.end_index
                                + detection.end_index
                                - detection.start_index
                                + len(sep),
                                word_count=last_result.word_count
                                + detection.word_count,
                            )
                        else:
                            merged_results.append(
                                DetectionResult(
                                    language=detection.language,
                                    start_index=last_result.end_index + len(sep),
                                    end_index=last_result.end_index
                                    + detection.end_index
                                    - detection.start_index
                                    + len(sep),
                                    word_count=detection.word_count,
                                )
                            )
            return merged_results

        texts = text.split(sep)
        print(texts)
        results = self.batch_detect(texts)
        merged_results = merge_results(results)
        return merged_results

    def batch_detect(self, texts: list[str]) -> list[list[DetectionResult]]:
        """Detect Language in Batch."""
        results = self.detector.detect_multiple_languages_in_parallel_of(texts)
        return results
