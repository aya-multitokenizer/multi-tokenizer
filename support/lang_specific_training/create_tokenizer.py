"""Script to create a tokenizer for a specific language."""

import argparse
from typing import Generator

from datasets import load_dataset

from tokenizers import ByteLevelBPETokenizer


def main(args: argparse.Namespace) -> None:
    """Create Tokenizer for Specific Language."""
    dataset = load_dataset(args.dataset_path, args.dataset_name, split="train")
    batch_size = args.batch_size
    assert (
        args.data_key in dataset.column_names
    ), f"Key {args.data_key} not found in dataset."

    def batch_iterator() -> Generator:
        """Batch Iterator."""
        for i in range(0, len(dataset), batch_size):
            yield dataset[i : i + batch_size][args.data_key]

    tokenizer = ByteLevelBPETokenizer()
    tokenizer.train_from_iterator(
        batch_iterator(),
        vocab_size=args.vocab_size,
        min_frequency=args.min_frequency,
        special_tokens=[
            "<UNK>",
            "<CLS>",
            "<SEP>",
            "<EN>",
            "</EN>",
            "<ES>",
            "</ES>",
            "<ZH>",
            "</ZH>",
            "<HI>",
            "</HI>",
        ],
    )
    tokenizer.save(args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create Tokenizer for Specific Language."
    )
    parser.add_argument(
        "--language", type=str, required=True, help="Language to create tokenizer for."
    )
    parser.add_argument(
        "--dataset_path",
        type=str,
        required=True,
        help="Dataset Path to train tokenizer on.",
    )
    parser.add_argument(
        "--dataset_name", type=str, help="Dataset Name to train tokenizer"
    )
    parser.add_argument(
        "--data_key", type=str, default="text", help="Key for text data in dataset."
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=1000,
        help="Batch size for training tokenizer.",
    )
    parser.add_argument("--output", type=str, help="Output path for tokenizer.")
    parser.add_argument(
        "--vocab_size", type=int, default=25000, help="Vocabulary size for tokenizer."
    )
    parser.add_argument(
        "--min_frequency", type=int, default=2, help="Minimum frequency for tokens."
    )
    args = parser.parse_args()

    if not args.output:
        args.output = f"{args.language}_tokenizer.json"

    main(args)
