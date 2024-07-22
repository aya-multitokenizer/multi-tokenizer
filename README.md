# Multi-Tokenizer
Tokenization of Multilingual Texts using Language-Specific Tokenizers

[![PyPI version](https://img.shields.io/pypi/v/multi-tokenizer.svg)](https://pypi.org/project/multi-tokenizer/)

## Overview

Multi-Tokenizer is a Python package that provides tokenization of multilingual texts using language-specific tokenizers. The package is designed to be used in a variety of applications, including natural language processing, machine learning, and data analysis. Behind the scenes, the package uses `lingua` library to detect the language of the text segments, the `tokenizers` library to create language-specific tokenizers, and then tokenizes the text segments using the appropriate tokenizer. Multi-tokenizer introduces additional special tokens to handle the language-specific tokenization, which can be used to reconstruct the original text segments after tokenization and allows the models to differentiate between the languages in the text segments.

## Installation

### Using pip
```bash
pip install multi-tokenizer
```

### from Source
```bash
git clone https://github.com/chandralegend/multi-tokenizer.git
cd multi-tokenizer
pip install .
```

## Usage

```python
from multi_tokenizer import MultiTokenizer, PretrainedTokenizers

# specify the language tokenizers to be used
lang_tokenizers = [
    PretrainedTokenizers.ENGLISH,
    PretrainedTokenizers.CHINESE,
    PretrainedTokenizers.HINDI,
]

# create a multi-tokenizer object (split_text=True to split the text into segments, for better language detection)
tokenizer = MultiTokenizer(lang_tokenizers, split_text=True)

sentence = "Translate this hindi sentence to english - बिल्ली बहुत प्यारी है."

# Pretokenize the text
pretokenized_text = tokenizer.pretokenize(sentence) # [('<EN>', (0, 1)), ('Translate', (1, 10)), ('Ġthis', (10, 15)), ('Ġhindi', (15, 21)), ...]

# Tokenize the text
ids, tokens = tokenizer.encode(pretokenized_text) # [3, 7235, 6614, 86, 755, 775, 10763, 83, 19412, 276, ...], ['<EN>', 'Tr', 'ans', 'l', 'ate', 'Ġthis', 'Ġhind', ...]

# Decode the tokens
decoded_text = tokenizer.decode(ids) # Translate this hindi sentence to english - बिल्ली बहुत प्यारी है.
```


## Development Setup

### Prerequisites
- Use the VSCode Dev Containers for easy setup (Recommended)
- Install dev dependencies
    ```bash
    pip install poetry
    poetry install
    ```

### Linting, Formatting and Type Checking
- Add the directory to safe.directory
    ```bash
    git config --global --add safe.directory /workspaces/multi-tokenizer
    ```
- Run the following command to lint and format the code
    ```bash
    pre-commit run --all-files
    ```
- To install pre-commit hooks, run the following command (Recommended)
    ```bash
    pre-commit install
    ```

### Running the tests
Run the tests using the following command
```bash
pytest -n "auto"
```

## Approaches

1. [Approach 1: Individual tokenizers for each language](support/proposal_1.md)
2. [Approach 2: Unified tokenization approach across languages using utf-8 encondings](support/proposal_2.md)

## Evaluation

- [Evaluation Methodologies](support/evaluation.md#evaluation-metodologies)
- [Data Collection and Analysis](support/evaluation.md#7-data-collection-and-analysis)
- [Comparative Analysis](support/evaluation.md#8-comparative-analysis)
- [Implementation Plan](support/evaluation.md#9-implementation-plan)
- [Future Expansion](support/evaluation.md#10-future-expansion)

## Contributors

- [Rob Neuhaus](https://github.com/rrenaud) - ⛴👨🏻‍✈️
- [Chandra Irugalbandara](https://github.com/chandralegend)
- [Alvanli](https://github.com/alvanli)
- [Vishnu Vardhan](https://github.com/VishnuVardhanSaiLanka)
- [Anthony Susevski](https://github.com/asusevski)
