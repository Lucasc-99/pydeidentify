# pydeidentify

A simple tool for text deidentification, built on spacy's state-of-the-art named entity recognition pipeline, now supporting 22 languages.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pydeidentify.

```bash
$ pip3 install pydeidentify
```

Using poetry
```bash
$ poetry add pydeidentify
```

## Usage

DISCLAIMER: this tool is not 100% accurate, and may miss some entities
The model is also case sensitive, and will have decreased accuracy if text is all lower-case

```python

# Basic usage, see examples/long_example.py for more

from pydeidentify import Deidentifier, DeidentifiedText

# Deidentify using this Deidentifier class
d = Deidentifier()
d_text: DeidentifiedText = d.deidentify(
    """My name is Joe Biden, I'm from Scranton, Pennsylvania and I like to create python packages. I was born 12-1-1999."""
)

# View output of deidentification using DeidentifiedText class

print(d_text.original()) # My name is Joe Biden, I'm from Scranton, Pennsylvania and I like to create python packages. I was born 12-1-1999.

print(d_text) # My name is PERSON0, I'm from GPE0, GPE1 and I like to create python packages. I was born DATE0.

print(d_text.encode_mapping) # {'Joe Biden': 'PERSON0', 'Scranton': 'GPE0', 'Pennsylvania': 'GPE1', '12-1-1999': 'DATE0'}
print(d_text.decode_mapping) # {'PERSON0': 'Joe Biden', 'GPE0': 'Scranton', 'GPE1': 'Pennsylvania', 'DATE0': '12-1-1999'}
print(d_text.counts) # {'ORG': 0, 'LOC': 0, 'PERSON': 1, 'GPE': 2, 'DATE': 1, 'FAC': 0}

# Use any spacy model that supports named entity recognition by passing it's name in the spacy_model parameter
# The line below loads the chinese version of the default english model: 'en_core_web_trf'
# see https://spacy.io/models for all models
d_chinese = Deidentifier(spacy_model="zh_core_web_trf") 
```

See all available langauges and pipelines at https://spacy.io/models

## Get and Run Example Code with Poetry
install poetry at https://python-poetry.org/docs/#installation
```bash
$ git clone https://github.com/Lucasc-99/pydeidentify
$ cd pydeidentify
$ poetry install
$ poetry run python examples/long_example
$ poetry run python examples/short_example
```

## Contributing

All pull requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)