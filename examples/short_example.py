from pydeidentify import Deidentifier, DeidentifiedText

# Deidentify using this Deidentifier class
d = Deidentifier(classifier="dbmdz/bert-large-cased-finetuned-conll03-english", tokenizer="bert-base-cased")
d_text: DeidentifiedText = d.deidentify("""My name is Joe Biden, I'm from Scranton, Pennsylvania and I like to create python packages.
I was born 12-1-1999. 
That would be the same as December 1, 1999.
That would also be the same as 12/1/1999.
There are many ways to write dates.
I could say December.
I could say December 12th ninety-nine.
I could say December twelfth nineteen ninety-nine.
This pipeline should catch all of these""")

# View output of deidentification using DeidentifiedText class
print(d_text.original())
print(d_text)
print(d_text.encode_mapping)
print(d_text.decode_mapping)
print(d_text.counts)
