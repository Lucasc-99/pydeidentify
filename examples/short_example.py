from pydeidentify import Deidentifier, DeidentifiedText

# Deidentify using this Deidentifier class
d = Deidentifier()
d_text: DeidentifiedText = d.deidentify("My name is Joe Biden, I'm from Scranton, Pennsylvania and I like to create python packages")

# View output of deidentification using DeidentifiedText class
print(d_text.original())
print(d_text)
print(d_text.encode_mapping)
print(d_text.decode_mapping)
print(d_text.counts)
