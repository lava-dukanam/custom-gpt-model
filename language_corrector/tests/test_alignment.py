import unittest
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from alignment import align_to_british_english

class TestAlignment(unittest.TestCase):

    def test_empty_string(self):
        self.assertEqual(align_to_british_english(""), "")

    def test_no_americanisms(self):
        text = "This text is already in proper British English, favouring colour and honour."
        self.assertEqual(align_to_british_english(text), text)

    def test_simple_spelling_conversion(self):
        self.assertEqual(align_to_british_english("The color is red."), "The colour is red.")
        self.assertEqual(align_to_british_english("Please analyze the data."), "Please analyse the data.")
        self.assertEqual(align_to_british_english("The center of the circle."), "The centre of the circle.")

    def test_ize_to_ise_conversion(self):
        self.assertEqual(align_to_british_english("Let's organize the event."), "Let's organise the event.")
        # Test a word that should not change
        self.assertEqual(align_to_british_english("The size of the prize is amazing."), "The size of the prize is amazing.")


    def test_licence_license_conversion(self):
        # Noun: AmE license -> BrE licence
        self.assertEqual(align_to_british_english("He has a driving license."), "He has a driving licence.")
        # Noun: BrE licence -> BrE licence (no change)
        self.assertEqual(align_to_british_english("It is his driving licence."), "It is his driving licence.")
        
        # Verb: AmE license -> BrE license (no change, as 'license' is verb in BrE too)
        self.assertEqual(align_to_british_english("The council will license the shop."), "The council will license the shop.")
        # Verb: BrE license -> BrE license (no change)
        self.assertEqual(align_to_british_english("They license performers."), "They license performers.")
        
        # AmE verb 'licence' (if someone misuses it) should become BrE verb 'license'
        # This depends on if the spaCy model correctly tags 'licence' as a verb if used that way.
        # The current rules assume 'licence' if tagged as verb is AmE usage.
        self.assertEqual(align_to_british_english("They will licence him."), "They will license him.")


    def test_mixed_sentence(self):
        american = "I need to analyze the color of the program and organize the files. He has a license."
        british = "I need to analyse the colour of the program and organise the files. He has a licence."
        self.assertEqual(align_to_british_english(american), british)

    def test_realize_conversion(self):
        self.assertEqual(align_to_british_english("I realize the truth."), "I realise the truth.")

if __name__ == '__main__':
    unittest.main()
