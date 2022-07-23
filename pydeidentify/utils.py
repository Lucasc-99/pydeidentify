from spacy.cli.download import download as spacy_download
from spacy.util import is_package as spacy_is_package
from typing import Dict


def cached_model_download(model_name: str)-> None:
    """
    Download spacy model if it is not already downloaded.
    """
    if not spacy_is_package(model_name):
        spacy_download(model_name)
        
        

SUPPORTED_ENTITIES: Dict[str, str] = {
    "PERSON": "People, including fictional.",
    "NORP": "Nationalities or religious or political groups.",
    "FAC": "Buildings, airports, highways, bridges, etc.",
    "ORG": "Companies, agencies, institutions, etc.",
    "GPE": "Countries, cities, states.",
    "LOC": "Non-GPE locations, mountain ranges, bodies of water.",
    "PRODUCT": "Objects, vehicles, foods, etc. (Not services.)",
    "EVENT": "Named hurricanes, battles, wars, sports events, etc.",
    "WORK_OF_ART": "Titles of books, songs, etc.",
    "LAW": "Named documents made into laws.",
    "LANGUAGE": "Any named language.",
    "DATE": "Absolute or relative dates or periods.",
    "TIME": "Times smaller than a day.",
    "PERCENT": "Percentage, including ”%“.",
    "MONEY": "Monetary values, including unit.",
    "QUANTITY": "Measurements, as of weight or distance.",
    "ORDINAL": "“first”, “second”, etc.",
    "CARDINAL": "Numerals that do not fall under another type.",
}


def replace_words_with_map(text: str, mapping: Dict[str, str]) -> str:
    """
    A basic utility function to replace text with lookup table,
    use this with either of the dictionaries/maps that are created by Deidentifier (decode/encode).

    :param text: text that will be replaced
    :param mapping: dictionary that maps from original text to replacement text
    :returns: a string with the text replaced
    """
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text