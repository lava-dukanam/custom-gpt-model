# Project Title: Language Correction GPT

## Description
This project aims to create a custom GPT model specifically trained for language correction tasks. It can be used to identify and correct grammatical errors, spelling mistakes, and improve overall sentence structure and clarity.

## Features
- Consolidates multiple feedback texts into a single document.
- Aligns consolidated text to standard British English, including:
    - Common spelling corrections (e.g., color -> colour, analyze -> analyse, center -> centre).
    - Conversion of "-ize" verb endings to "-ise".
    - Differentiation between "licence" (noun) and "license" (verb) for British English.

## Getting Started

### Prerequisites
*   Python 3.7+
*   spaCy library: `pip install spacy`
*   A spaCy English model: `python -m spacy download en_core_web_sm` (or a larger model like `en_core_web_md` for better accuracy).

### Installation
1.  Clone the repository:
    ```bash
    git clone <your-repository-url>
    cd <repository-name>
    ```
2.  Install dependencies (primarily spaCy as listed above).

## Usage
The primary entry point for demonstration is `language_corrector/main.py`.

To run the demonstration:
```bash
python language_corrector/main.py
```
This script will:
1.  Take a sample list of American English feedback strings.
2.  Consolidate them into a single text.
3.  Apply British English alignment rules.
4.  Print the original, consolidated (American), and final (British) versions of the text.

This serves as a basic example of how to use the `consolidate_feedback` and `align_to_british_english` functions from the `src` directory.

## Running Tests

The project includes unit tests for the core functionalities. To run the tests, navigate to the project's root directory and use Python's `unittest` module:

```bash
python -m unittest discover -s language_corrector/tests -p "test_*.py"
```
Alternatively, you can run individual test files:
```bash
python -m unittest language_corrector/tests/test_feedback_processor.py
python -m unittest language_corrector/tests/test_alignment.py
```

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a Pull Request.

Please ensure your code adheres to the project's coding standards and includes tests where applicable.

## License
This project is licensed under the MIT License. See the LICENSE file for more details. (Note: You'll need to create a LICENSE file separately if you choose this license).
