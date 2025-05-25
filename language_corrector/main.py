import sys
import os

# Add src directory to Python path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from feedback_processor import consolidate_feedback
from alignment import align_to_british_english

def main():
    """
    Main function to demonstrate feedback consolidation and alignment.
    """
    sample_feedback_list = [
        "The user interface is intuitive and the color scheme is pleasant. I did realize some minor bugs though.",
        "I want to analyze the performance. The application center needs more work.",
        "Overall, a good effort. We should organize a meeting to finalize the details and get the license for the new font."
    ]

    print("----- Original Feedback -----")
    for i, feedback in enumerate(sample_feedback_list):
        print(f"Reviewer {i+1}: {feedback}")
    print("\n---------------------------\n")

    consolidated_text = consolidate_feedback(sample_feedback_list)
    print("----- Consolidated Feedback (American English) -----")
    print(consolidated_text)
    print("\n--------------------------------------------------\n")

    final_british_text = align_to_british_english(consolidated_text)
    print("----- Final Aligned Feedback (British English) -----")
    print(final_british_text)
    print("\n--------------------------------------------------\n")

if __name__ == '__main__':
    main()
