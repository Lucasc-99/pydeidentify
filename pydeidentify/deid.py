from pydeidentify.utils import replace_words_with_map, cached_model_download
from typing import Dict
import spacy
import warnings


# Catch benign warnings from spacy about CUDA
warnings.filterwarnings("ignore", category=UserWarning)


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
    :param spacy_model: en_core_web_trf comes installed with pydeidentify by default, see https://spacy.io/models/ for more models and langauges
    """

    def __init__(
        self,
        included_entity_types: set = {"PERSON", "ORG", "FAC", "LOC", "GPE", "DATE"},
        exceptions: set = {},
        spacy_model: str = "en_core_web_trf",
    ):
        cached_model_download(spacy_model)
        self.named_entity_pipe = spacy.load(spacy_model)
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
