import unittest
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from feedback_processor import consolidate_feedback

class TestFeedbackProcessor(unittest.TestCase):

    def test_consolidate_empty_list(self):
        self.assertEqual(consolidate_feedback([]), "")

    def test_consolidate_single_item(self):
        self.assertEqual(consolidate_feedback(["Hello world"]), "Hello world")

    def test_consolidate_multiple_items(self):
        feedback = ["First sentence.", "Second sentence.", "Third sentence."]
        expected = "First sentence.\nSecond sentence.\nThird sentence."
        self.assertEqual(consolidate_feedback(feedback), expected)

    def test_consolidate_with_empty_strings(self):
        feedback = ["Test.", "", "Another test."]
        expected = "Test.\n\nAnother test."
        self.assertEqual(consolidate_feedback(feedback), expected)

if __name__ == '__main__':
    unittest.main()
