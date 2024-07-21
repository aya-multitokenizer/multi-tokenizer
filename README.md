# Multi-Tokenizer
Tokenization of Multilingual Texts using Language-Specific Tokenizers

[![PyPI version](https://img.shields.io/pypi/v/multi-tokenizer.svg)](https://pypi.org/project/multi-tokenizer/)

## Overview

Multi-Tokenizer is a Python package that provides tokenization of multilingual texts using language-specific tokenizers. The package is designed to be used in a variety of applications, including natural language processing, machine learning, and data analysis. Behind the scenes, the package uses `lingua` library to detect the language of the text segments, the `tokenizers` library to create language-specific tokenizers, and then tokenizes the text segments using the appropriate tokenizer. Multi-tokenizer introduces additional special tokens to handle the language-specific tokenization, which can be used to reconstruct the original text segments after tokenization and allows the models to differentiate between the languages in the text segments.

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
