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
