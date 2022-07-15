from typing import Tuple, Dict, Union, List
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline


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
    :param tokenizer: tokenizer to use for the named entity recognition pipeline
    :param classifier: classifier to use for the named entity recognition pipeline
    :param aggregation_strategy: aggregation strategy to use for the named entity recognition pipeline
    :param include_misc: whether to include the "MISC" class when deidentifying, note that this class often contains non-entities
    """

    def __init__(
        self,
        tokenizer: str = "dslim/bert-base-NER",
        classifier: str = "dslim/bert-base-NER",
        aggregation_strategy: str = "max",
        include_misc: bool = False,
    ):
        self.include_misc = include_misc

        tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        classifier = AutoModelForTokenClassification.from_pretrained(classifier)

        self.named_entity_pipe = pipeline(
            "ner",
            model=classifier,
            tokenizer=tokenizer,
            aggregation_strategy=aggregation_strategy,
        )

    def deidentify(
        self, text: Union[str, List[str]]
    ) -> Tuple[str, Dict[str, str], Dict[str, str]]:
        """
        Deidentify the input text, returns an instance of DeidentifiedText

        :param text: text to deidentify, can be a string or a list of strings
        :returns: a DeidentifiedText object
        """
        if isinstance(text, str):
            text = [text]

        ents = [ent for ent_list in self.named_entity_pipe(text) for ent in ent_list]
        text = "\n".join(text)

        d_encode = {}
        d_decode = {}

        counts = {"PER": 0, "ORG": 0, "LOC": 0, "MISC": 0}
        for ent in ents:
            cls = ent["entity_group"]
            name = ent["word"]
            if cls != "MISC" or self.include_misc:
                if name not in d_encode:
                    d_decode[cls + str(counts[cls])] = name
                    d_encode[name] = cls + str(counts[cls])
                    text = text.replace(name, cls + str(counts[cls]))
                    counts[cls] += 1
                else:
                    text = text.replace(name, cls + str(counts[cls]))

        return DeidentifiedText(text, d_encode, d_decode, counts)

    def __call__(self, text: str) -> Tuple[str, Dict[str, str], Dict[str, str]]:
        return self.deidentify(text)
