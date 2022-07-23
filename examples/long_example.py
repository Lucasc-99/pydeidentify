from pydeidentify import (
    Deidentifier,
    DeidentifiedText,
    replace_words_with_map,
    SUPPORTED_ENTITIES,
)

text = """
This text was copied from a public domain website by Lucasc-99, the author of this code. We will exclude Lucasc-99 from the deidentification process. Thus the term Lucasc-99 will not be replaced.
Nineteen Eighty-Four (also stylised as 1984) is a dystopian social science fiction novel and cautionary tale written by the English writer George Orwell.
It was published on 8 June 1949 by Secker & Warburg as Orwell's ninth and final book completed in his lifetime.
Thematically, it centres on the consequences of totalitarianism, mass surveillance and repressive regimentation of people and behaviours within society.
Orwell, a democratic socialist, modelled the totalitarian government in the novel after Stalinist Russia and Nazi Germany. 
More broadly, the novel examines the role of truth and facts within politics and the ways in which they are manipulated.
The story takes place in an imagined future, the year 1984, when much of the world has fallen victim to perpetual war, omnipresent government surveillance, historical negationism, and propaganda.
Great Britain, known as Airstrip One, has become a province of the totalitarian superstate Oceania, ruled by the Party, who employ the Thought Police to persecute individuality and independent thinking.
Big Brother, the dictatorial leader of Oceania, enjoys an intense cult of personality, manufactured by the party's excessive brainwashing techniques.
The color of animals is by no means a matter of chance; it depends on many considerations, but in the majority of cases tends to protect the animal from danger by rendering it less conspicuous.
Perhaps it may be said that if coloring is mainly protective, there ought to be but few brightly colored animals. There are, however, not a few cases in which vivid colors are themselves protective.
The kingfisher itself, though so brightly colored, is by no means easy to see.
The blue harmonizes with the water, and the bird as it darts along the stream looks almost like a flash of sunlight.
Desert animals are generally the color of the desert. 
Thus, for instance, the lion, the antelope, and the wild donkey are all sand-colored. “Indeed,” says Canon Tristram, “in the desert, where neither trees, brushwood, nor even undulation of the surface afford the slightest protection to its foes, a modification of color assimilated to that of the surrounding country is absolutely necessary. Hence, without exception, the upper plumage of every bird, and also the fur of all the smaller mammals and the skin of all the snakes and lizards, is of one uniform sand color.”
The next point is the color of the mature caterpillars, some of which are brown. This probably makes the caterpillar even more conspicuous among the green leaves than would otherwise be the case. Let us see, then, whether the habits of the insect will throw any light upon the riddle. What would you do if you were a big caterpillar? Why, like most other defenseless creatures, you would feed by night, and lie concealed by day. So do these caterpillars. When the morning light comes, they creep down the stem of the food plant, and lie concealed among the thick herbage and dry sticks and leaves, near the ground, and it is obvious that under such circumstances the brown color really becomes a protection. It might indeed be argued that the caterpillars, having become brown, concealed themselves on the ground, and that we were reversing the state of things. But this is not so, because, while we may say as a general rule that large caterpillars feed by night and lie concealed by day, it is by no means always the case that they are brown; some of them still retaining the green color. We may then conclude that the habit of concealing themselves by day came first, and that the brown color is a later adaptation.
"""

# Deidentify the above text using the Deidentifier class
d = Deidentifier(
    included_entity_types={"PERSON", "ORG", "FAC", "LOC", "GPE", "DATE"},
    exceptions={"Lucasc-99"},
)

# To see the full list of entities and what they mean, use the SUPPORTED_ENTITIES constant
print(f"Supported Entities and Meanings:\n{SUPPORTED_ENTITIES}")


# Run the pipeline
deidentified_text: DeidentifiedText = d.deidentify(text)

# View output, original, counts and mappings with the DeidentifiedText class
print("Deidentified Text:\n", deidentified_text)
print("Original:\n", deidentified_text.original())
print(f"Encode mapping: {deidentified_text.encode_mapping}\n")
print(f"Decode mapping: {deidentified_text.decode_mapping}\n")
print(f"Entity Counts: {deidentified_text.counts}\n")

# You can use the replace_words_with_map() function to do as you will with the entity mappings
assert deidentified_text.original() == replace_words_with_map(
    deidentified_text.text, deidentified_text.decode_mapping
)  # True
