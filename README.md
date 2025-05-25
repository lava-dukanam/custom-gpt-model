# Project Title: Language Correction GPT

## Description
This project aims to create a custom GPT model specifically trained for language correction tasks. It can be used to identify and correct grammatical errors, spelling mistakes, and improve overall sentence structure and clarity.

## Features
- Consolidates multiple feedback texts into a single document.
- Aligns consolidated text to standard British English, including:
    - Common spelling corrections (e.g., color -> colour, analyze -> analyse, center -> centre).
    - Conversion of "-ize" verb endings to "-ise".
    - Differentiation between "licence" (noun) and "license" (verb) for British English.
- Processes feedback from an Excel file (`input_feedback.xlsx`):
    - Reads data from columns 'Reviewer', 'Standard Number', and 'Feedback'.
    - Groups feedback by 'Reviewer' and 'Standard Number'.
    - Consolidates and aligns feedback for each group.
    - Writes processed data, including aggregated values for other columns, to `processed_feedback.xlsx`.

## Getting Started

### Prerequisites
*   Python 3.7+
*   A spaCy English model: `python -m spacy download en_core_web_sm` (or a larger model like `en_core_web_md` for better accuracy).
*   Other dependencies listed in `requirements.txt`. Install them using:
    ```bash
    pip install -r requirements.txt
    ```

### Installation
1.  Clone the repository:
    ```bash
    git clone <your-repository-url>
    cd <repository-name>
    ```
2.  Install dependencies by running `pip install -r requirements.txt` (after ensuring you have Python and have downloaded the spaCy model).

## Usage

This project processes feedback from an Excel file to consolidate it and align it to British English.

1.  **Prepare your input file:**
    *   Create an Excel file named `input_feedback.xlsx` in the `language_corrector` directory (the same directory as `main.py`).
    *   Ensure your feedback data is on the **first sheet** of the Excel file.
    *   The script expects to find data in the following columns (it will try to find them by these names first, then by fixed positions B, F, I if names are not found):
        *   **Reviewer**: The name or identifier of the reviewer (tries 'Reviewer', then Column B).
        *   **Standard Number**: The standard number associated with the feedback (tries 'Standard Number', then Column F).
        *   **Feedback**: The actual feedback text (tries 'Feedback', then Column I).
    *   Other columns will be carried over and their values aggregated if multiple rows are consolidated for the same Reviewer/Standard Number.

2.  **Run the processing script:**
    Navigate to the `language_corrector` directory in your terminal and run:
    ```bash
    python main.py
    ```

3.  **Output:**
    *   A new Excel file named `processed_feedback.xlsx` will be created in the `language_corrector` directory.
    *   This file will contain the processed data, with feedback consolidated and aligned to British English in the 'Feedback' column (or original Column I). Other columns will have their data appropriately aggregated.
    *   The script will print status messages to the console, including any errors encountered (e.g., if the input file is not found or columns are not as expected).

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
