import sys
import os
import pandas as pd

# Add src directory to Python path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from feedback_processor import consolidate_feedback
from alignment import align_to_british_english

def aggregate_other_columns(series):
    """
    Aggregates values in a series by joining unique stringified values with a comma.
    If all values are the same, returns that single value.
    Handles NaN by ignoring them in the aggregation unless it's the only value.
    """
    # Drop NaN values for aggregation, unless all are NaN
    # Convert to string to ensure joinability and handle mixed types
    valid_strings = [str(item) for item in series.dropna().unique()]

    if not valid_strings: # All were NaN or series was empty
        return None # Or an empty string: ""
    if len(valid_strings) == 1:
        return valid_strings[0]
    return ", ".join(valid_strings)

def process_excel_feedback(input_excel_path: str, output_excel_path: str):
    """
    Reads feedback from an input Excel file, processes it, and writes
    the result to a new output Excel file.
    """
    try:
        print(f"Reading Excel file: {input_excel_path}")
        # Assume data is on the first sheet
        df = pd.read_excel(input_excel_path, sheet_name=0)
        print("Input DataFrame columns:", df.columns.tolist())
        print(f"Input DataFrame shape: {df.shape}")

        # Define expected columns - adjust if column names in Excel are different
        # For this task, we're using column *positions* as per user (B, F, I)
        # B is 1, F is 5, I is 8 (0-indexed)
        # It's better to use names if possible, but let's map them based on the problem description
        # Assuming the user means the columns *named* "Reviewer", "Standard Number", "Feedback"
        # If not, we'll need to use iloc or get actual names.
        # For robustness, let's try to find columns by common names first, then fall back to positions if they are not found.

        col_map = {}

        # Try to identify columns by likely names
        # Column B: Reviewer
        if 'Reviewer' in df.columns:
            col_map['reviewer'] = 'Reviewer'
        elif df.shape[1] > 1: # Column B
            col_map['reviewer'] = df.columns[1]
        else:
            raise ValueError("Reviewer column (expected 'Reviewer' or Column B) not found.")

        # Column F: Standard Number
        if 'Standard Number' in df.columns:
            col_map['standard_number'] = 'Standard Number'
        elif df.shape[1] > 5: # Column F
            col_map['standard_number'] = df.columns[5]
        else:
            raise ValueError("Standard Number column (expected 'Standard Number' or Column F) not found.")

        # Column I: Feedback
        if 'Feedback' in df.columns:
            col_map['feedback'] = 'Feedback'
        elif df.shape[1] > 8: # Column I
            col_map['feedback'] = df.columns[8]
        else:
            raise ValueError("Feedback column (expected 'Feedback' or Column I) not found.")
        
        print(f"Using column mapping: {{'Reviewer': '{col_map['reviewer']}', 'Standard Number': '{col_map['standard_number']}', 'Feedback': '{col_map['feedback']}'}}")

        # Ensure feedback column is treated as string
        df[col_map['feedback']] = df[col_map['feedback']].astype(str)

        print(f"Grouping by: ['{col_map['reviewer']}', '{col_map['standard_number']}']")
        
        # Define aggregation functions
        agg_funcs = {}
        # For the feedback column, consolidate and then align
        agg_funcs[col_map['feedback']] = lambda x: align_to_british_english(consolidate_feedback(list(x)))
        
        # For all other columns, apply the custom aggregator
        for col in df.columns:
            if col not in [col_map['reviewer'], col_map['standard_number'], col_map['feedback']]:
                agg_funcs[col] = aggregate_other_columns
        
        # Perform the grouping and aggregation
        # The columns we group by will become the index, so we reset_index()
        processed_df = df.groupby([col_map['reviewer'], col_map['standard_number']], as_index=False).agg(agg_funcs)
        
        # Reorder columns to match original if necessary, or a preferred order
        # For now, pandas will put grouped columns first, then aggregated ones in order.
        # If original order is crucial:
        # processed_df = processed_df[df.columns] # This might fail if column names changed or new ones added.

        print(f"Writing processed data to: {output_excel_path}")
        processed_df.to_excel(output_excel_path, index=False)
        print("Processing complete.")

    except FileNotFoundError:
        print(f"Error: Input Excel file not found at {input_excel_path}")
        print("Please ensure the file 'input_feedback.xlsx' exists in the same directory as the script, or provide the correct path.")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    """
    Main function to trigger Excel feedback processing.
    """
    # Define input and output file paths
    # For now, these are hardcoded. Consider using command-line arguments for more flexibility.
    # Assumes the script is run from the 'language_corrector' directory,
    # and Excel files are in the same directory.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, "input_feedback.xlsx") 
    output_file = os.path.join(current_dir, "processed_feedback.xlsx")

    print(f"Looking for input file at: {input_file}")
    process_excel_feedback(input_file, output_file)

if __name__ == '__main__':
    main()
