# Tokenization of Multilingual Texts using Language-Specific Tokenizers

## Approaches

1. [Approach 1: Individual tokenizers for each language](support/proposal_1.md)
2. [Approach 2: Unified tokenization approach across languages using utf-8 encondings](support/proposal_2.md)

## Evaluation

- [Evaluation Methodologies](support/evaluation.md#evaluation-metodologies)
- [Data Collection and Analysis](support/evaluation.md#7-data-collection-and-analysis)
- [Comparative Analysis](support/evaluation.md#8-comparative-analysis)
- [Implementation Plan](support/evaluation.md#9-implementation-plan)
- [Future Expansion](support/evaluation.md#10-future-expansion)

## Development Setup

### Prerequisites
- Use the Dev Container for easy setup
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
