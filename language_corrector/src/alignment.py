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

    # -or to -our
    {"patterns": [[{"LOWER": "behavior"}]], "attrs": {"LEMMA": "behaviour", "NORM": "behaviour", "TEXT": "behaviour"}},
    {"patterns": [[{"LOWER": "flavor"}]], "attrs": {"LEMMA": "flavour", "NORM": "flavour", "TEXT": "flavour"}},
    {"patterns": [[{"LOWER": "humor"}]], "attrs": {"LEMMA": "humour", "NORM": "humour", "TEXT": "humour"}},
    {"patterns": [[{"LOWER": "labor"}]], "attrs": {"LEMMA": "labour", "NORM": "labour", "TEXT": "labour"}},
    {"patterns": [[{"LOWER": "neighbor"}]], "attrs": {"LEMMA": "neighbour", "NORM": "neighbour", "TEXT": "neighbour"}},
    {"patterns": [[{"LOWER": "rumor"}]], "attrs": {"LEMMA": "rumour", "NORM": "rumour", "TEXT": "rumour"}},

    # -er to -re (center already done)
    {"patterns": [[{"LOWER": "theater"}]], "attrs": {"LEMMA": "theatre", "NORM": "theatre", "TEXT": "theatre"}},
    {"patterns": [[{"LOWER": "meter"}]], "attrs": {"LEMMA": "metre", "NORM": "metre", "TEXT": "metre"}}, # e.g., parking meter -> parking metre
    {"patterns": [[{"LOWER": "liter"}]], "attrs": {"LEMMA": "litre", "NORM": "litre", "TEXT": "litre"}},

    # -lling vs -ling (and similar)
    {"patterns": [[{"LOWER": "traveling"}]], "attrs": {"LEMMA": "travelling", "NORM": "travelling", "TEXT": "travelling"}},
    {"patterns": [[{"LOWER": "traveler"}]], "attrs": {"LEMMA": "traveller", "NORM": "traveller", "TEXT": "traveller"}},
    {"patterns": [[{"LOWER": "counseling"}]], "attrs": {"LEMMA": "counselling", "NORM": "counselling", "TEXT": "counselling"}},
    {"patterns": [[{"LOWER": "counselor"}]], "attrs": {"LEMMA": "counsellor", "NORM": "counsellor", "TEXT": "counsellor"}},
    {"patterns": [[{"LOWER": "modeling"}]], "attrs": {"LEMMA": "modelling", "NORM": "modelling", "TEXT": "modelling"}},
    {"patterns": [[{"LOWER": "modeler"}]], "attrs": {"LEMMA": "modeller", "NORM": "modeller", "TEXT": "modeller"}},

    # other common individual words
    # {"patterns": [[{"LOWER": "program"}], [{"LOWER": {"IN": ["computer", "software", "radio", "tv"]}}]], "attrs": {"LEMMA": "programme", "NORM": "programme", "TEXT": "programme"}}, # program (general) -> programme (BrE for broadcast/events)
    # Note: "program" in computing usually stays "program" in BrE. This rule is a simple attempt to differentiate.
    # A more robust way would require more context or a simpler rule to always change it if that's preferred.
    # For now, this rule attempts to change "computer program", "software program" etc. to "programme"
    # This might be too aggressive or not what's intended.
    # A simpler, more common one:
    {"patterns": [[{"LOWER": "program"}]], "attrs": {"LEMMA": "programme", "NORM": "programme", "TEXT": "programme"}}, # General change, user can refine if "computer program" should stay.

    {"patterns": [[{"LOWER": "dialog"}]], "attrs": {"LEMMA": "dialogue", "NORM": "dialogue", "TEXT": "dialogue"}},
    {"patterns": [[{"LOWER": "catalog"}]], "attrs": {"LEMMA": "catalogue", "NORM": "catalogue", "TEXT": "catalogue"}},
    # 'catalogue' verb -ize rule handles this if it was 'catalogize'
    {"patterns": [[{"LOWER": "analog"}]], "attrs": {"LEMMA": "analogue", "NORM": "analogue", "TEXT": "analogue"}},

    # defense/offense -> defence/offence (nouns)
    {"patterns": [[{"LOWER": "defense"}, {"TAG": {"IN": ["NN", "NNS"]}}]], "attrs": {"LEMMA": "defence", "NORM": "defence", "TEXT": "defence"}},
    {"patterns": [[{"LOWER": "offense"}, {"TAG": {"IN": ["NN", "NNS"]}}]], "attrs": {"LEMMA": "offence", "NORM": "offence", "TEXT": "offence"}},

    # grey vs gray
    {"patterns": [[{"LOWER": "gray"}]], "attrs": {"LEMMA": "grey", "NORM": "grey", "TEXT": "grey"}},

    # judgment -> judgement
    {"patterns": [[{"LOWER": "judgment"}]], "attrs": {"LEMMA": "judgement", "NORM": "judgement", "TEXT": "judgement"}},

    # check -> cheque (for bank check) - This is context dependent and hard.
    # A simple rule (might be too broad):
    {"patterns": [[{"LOWER": "check"}, {"LEMMA": "check"}, {"TAG":"NN"}, {"TEXT": {"REGEX": "^[Cc]heck$"}}]], "attrs": {"LEMMA": "cheque", "NORM": "cheque", "TEXT": "cheque"}},
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

    print("\n--- Additional Tests for Refined Patterns ---")
    test_cases = {
        "behavior": "The behavior of the animals was strange.",
        "flavor": "What is your favorite flavor of ice cream?",
        "humor": "He has a great sense of humor.",
        "labor": "The labor involved was intensive.",
        "neighbor": "My neighbor is very friendly.",
        "rumor": "There's a rumor going around.",
        "theater": "Let's go to the theater tonight.",
        "meter": "The parking meter expired.",
        "liter": "Buy a liter of milk.",
        "traveling": "He is traveling to France.",
        "traveler": "She is an experienced traveler.",
        "counseling": "She is seeking counseling.",
        "counselor": "He works as a school counselor.",
        "modeling": "He enjoys modeling clay figures.", # Note: 'modelling' also for fashion
        "program": "What's the television program tonight?", # -> programme
        "dialog": "The dialog in the movie was witty.",         # -> dialogue
        "catalog": "I browsed the store catalog.",        # -> catalogue
        "analog": "This is an analog recording.",          # -> analogue
        "defense": "The team's defense was strong.",      # -> defence
        "offense": "No offense was intended.",            # -> offence
        "gray": "The sky was gray.",                      # -> grey
        "judgment": "His judgment was sound.",              # -> judgement
        "check": "I need to write a check for the rent.", # -> cheque (context dependent)
        "check a box": "Please check this box.", # -> check (should remain)
        "organize program": "We need to organize the computer program installation.", # -> organise programme (testing interaction)
        "realize theater program": "I realize the theater program is new." # -> realise theatre programme
    }

    for key, american_text in test_cases.items():
        british_text = align_to_british_english(american_text)
        print(f"Test '{key}':")
        print(f"  AmE: {american_text}")
        print(f"  BrE: {british_text}\n")

    # Test for program (computing context, should ideally remain 'program')
    # The current general rule will change it to 'programme'.
    # This highlights the need for more sophisticated context handling for some words.
    computing_program_test = "The computer program is efficient."
    print(f"Test 'computing program':")
    print(f"  AmE: {computing_program_test}")
    print(f"  BrE (current general rule): {align_to_british_english(computing_program_test)}\n")
