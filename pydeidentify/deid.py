from functools import lru_cache
from typing import Dict
import spacy


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


@lru_cache(maxsize=2)
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


class DeidentifiedText:
    """
    A class that wraps a deidentified piece of text created by Deidentifier
    and provides methods to reidentify the text

    :param text: deidentified text
    :param encode_mapping: dictionary that maps from original text to replacement text
    :param decode_mapping: dictionary that maps from replacement text to original text
    :param counts: a dictionary with the counts of each entity code in the text

    """

    def __init__(
        self,
        text: str,
        encode_mapping: Dict[str, str],
        decode_mapping: Dict[str, str],
        counts: Dict[str, int],
    ):
        self.text = text
        self.encode_mapping = encode_mapping
        self.decode_mapping = decode_mapping
        self.counts = counts

    def original(self) -> str:
        return replace_words_with_map(self.text, self.decode_mapping)

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return self.text


class Deidentifier:
    """
    A class that deidentifies a piece of text, using a pre-trained named entity recognition pipeline from transformers

    :param text: text to deidentify
    :param included_entity_types: entities that will be deidentified, see SUPPORTED_ENTITIES for all supported entities
    :param exceptions: snippets that will not be deidentified
    """

    def __init__(
        self,
        included_entity_types: set = {
            "PERSON",
            "ORG",
            "FAC",
            "LOC",
            "DATE"
        },
        exceptions: set = {},
    ):
        self.named_entity_pipe = spacy.load("en_core_web_trf")
        self.included_entity_types = included_entity_types
        self.exceptions = exceptions

    def deidentify(self, text: str) -> DeidentifiedText:
        """
        Deidentify the input text, returns an instance of DeidentifiedText

        :param text: text to deidentify, can be a string or a list of strings
        :returns: a DeidentifiedText object
        """

        d_encode = {}
        d_decode = {}

        counts = {k: 0 for k in self.included_entity_types}
        for ent in self.named_entity_pipe(text).ents:
            cls = ent.label_
            name = ent.text
            if cls in self.included_entity_types:
                if name not in d_encode and name not in self.exceptions:
                    d_decode[cls + str(counts[cls])] = name
                    d_encode[name] = cls + str(counts[cls])
                    text = text.replace(name, cls + str(counts[cls]))
                    counts[cls] += 1
                else:
                    text = text.replace(name, cls + str(counts[cls]))

        return DeidentifiedText(text, d_encode, d_decode, counts)

    def __call__(self, text: str) -> DeidentifiedText:
        return self.deidentify(text)
