import spacy
from spacy.pipeline import AttributeRuler

# Load a small English spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize the AttributeRuler and add it to the pipeline
# Add it before the lemmatizer (if present) and before NER to ensure
# subsequent components see the modified token attributes.
# Based on default pipeline components, 'tagger' is a good component to add it after,
# and 'parser' or 'ner' are good components to add it before.
# If lemmatizer is not explicitly in the pipeline, spaCy might add it based on model.
# We'll add it before 'parser' to be safe.
if "lemmatizer" in nlp.pipe_names:
    ruler = nlp.add_pipe("attribute_ruler", before="lemmatizer")
else:
    # If no lemmatizer, try before parser or ner. Defaulting to before parser.
    if 'parser' in nlp.pipe_names:
        ruler = nlp.add_pipe("attribute_ruler", before="parser")
    elif 'ner' in nlp.pipe_names:
        ruler = nlp.add_pipe("attribute_ruler", before="ner")
    else:
        ruler = nlp.add_pipe("attribute_ruler")


# Define patterns for British English spelling alignment
# The attributes to set are:
# "LOWER": for the lowercase version of the token text itself (if we want to change it)
# "TEXT": for the token text itself (if we want to change its casing or form)
# "LEMMA": to set the lemma to the British form
# "NORM": to set the normalized form (often used in matching) to the British form

patterns = [
    {"patterns": [[{"LOWER": "center"}]], "attrs": {"LEMMA": "centre", "NORM": "centre", "TEXT": "centre"}},
    {"patterns": [[{"LOWER": "color"}]], "attrs": {"LEMMA": "colour", "NORM": "colour", "TEXT": "colour"}},
    {"patterns": [[{"LOWER": "analyze"}]], "attrs": {"LEMMA": "analyse", "NORM": "analyse", "TEXT": "analyse"}},
    {"patterns": [[{"LOWER": "realize"}]], "attrs": {"LEMMA": "realise", "NORM": "realise", "TEXT": "realise"}},
    # Add more common patterns here -ize to -ise, -or to -our, etc.
    # Example for -ize ending words (this is a simple approach, might need refinement for edge cases)
    # This specific pattern targets verbs ending in 'ize'
    {"patterns": [[{"LOWER": {"REGEX": ".+ize$"}}, {"TAG": {"REGEX": "VB.?"}}]] , "attrs": {"TEXT": {"REGEX_REPLACE": ["(ize)$", "ise"]}, "LEMMA": {"REGEX_REPLACE": ["(ize)$", "ise"]}, "NORM": {"REGEX_REPLACE": ["(ize)$", "ise"]}}},
    {"patterns": [[{"LOWER": "licence"}, {"TAG": "NN"}]], "attrs": {"LEMMA": "licence", "NORM": "licence", "TEXT": "licence"}}, # Noun form already BrE
    {"patterns": [[{"LOWER": "license"}, {"TAG": {"REGEX": "VB.?"}}]] , "attrs": {"LEMMA": "license", "NORM": "license", "TEXT": "license"}}, # Verb form already BrE
    {"patterns": [[{"LOWER": "licence"}, {"TAG": {"REGEX": "VB.?"}}]] , "attrs": {"LEMMA": "license", "NORM": "license", "TEXT": "license"}}, # Verb form as licence (AmE) -> license (BrE verb)
    {"patterns": [[{"LOWER": "license"}, {"TAG": "NN"}]], "attrs": {"LEMMA": "licence", "NORM": "licence", "TEXT": "licence"}}, # Noun form as license (AmE) -> licence (BrE noun)
]

# Add patterns to the ruler
ruler.add_patterns(patterns)

def align_to_british_english(text: str) -> str:
    """
    Processes a text string with spaCy and applies AttributeRuler
    rules to align spellings and forms to British English.
    Returns the modified text.
    """
    doc = nlp(text)
    # Reconstruct the text from tokens, respecting original spacing.
    # The TEXT attribute of tokens might have been changed by the AttributeRuler.
    words = []
    for token in doc:
        words.append(token.text_with_ws if token.whitespace_ else token.text)
    return "".join(words)

if __name__ == '__main__':
    # Example Usage
    american_text = "I want to analyze the color and center of the object. I realize this is a license to print money."
    british_text = align_to_british_english(american_text)
    print(f"American English: {american_text}")
    print(f"British English:  {british_text}")

    american_text_2 = "Please organize the files and catalogue them. It's a common practice."
    british_text_2 = align_to_british_english(american_text_2)
    print(f"American English: {american_text_2}")
    print(f"British English:  {british_text_2}")

    # Test for license/licence
    # In BrE: licence (noun), license (verb)
    # In AmE: license (noun/verb)
    test_licence_1 = "He has a driving license." # AmE noun
    corrected_licence_1 = align_to_british_english(test_licence_1)
    print(f"AmE: {test_licence_1} -> BrE: {corrected_licence_1}") # Expected: He has a driving licence.

    test_licence_2 = "The authority will license the premises." # AmE verb (same as BrE verb)
    corrected_licence_2 = align_to_british_english(test_licence_2)
    print(f"AmE: {test_licence_2} -> BrE: {corrected_licence_2}") # Expected: The authority will license the premises.

    test_licence_3 = "This is his licence to operate." # BrE noun (should remain)
    corrected_licence_3 = align_to_british_english(test_licence_3)
    print(f"BrE: {test_licence_3} -> BrE: {corrected_licence_3}") # Expected: This is his licence to operate.

    test_licence_4 = "They licence him to fish here." # BrE verb (should remain)
    corrected_licence_4 = align_to_british_english(test_licence_4)
    print(f"BrE: {test_licence_4} -> BrE: {corrected_licence_4}") # Expected: They licence him to fish here.
