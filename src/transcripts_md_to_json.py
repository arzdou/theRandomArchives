'''
This script will create all the JSON files with the possible phrases and the correspondant speaker.

Not all phrases are allowed, specificaly I have removed those that:
 - Have less than 2 words.
 - Have too many characters to be posted on twitter.
 
The data is saved in the _jsons folder.
'''

import re
import json
from os import listdir

# Function taken from https://www.py4u.net/discuss/10738 to split a paragraph into sentences

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


DIRECTORY = './_posts'
FILE_NAMES = listdir(DIRECTORY)

for episode in FILE_NAMES:
    with open('{}/{}'.format(DIRECTORY, episode)) as file_md:
        text = file_md.read()
        text = re.sub(r'\([^)]*\)', '', text) # Goodbye everything between parenthesis
        text = re.sub(r'\_', '', text) # Goodbye hyphens :)
        
        # All files begin with a table with a variety of content, we delete it because it is not interesting (god i wish i knew how to do this with regex)
        end_intro_index = text[1:].find('---') 
        statement = text[end_intro_index+6:]
        
        paragraphs = statement.split("\n")
        paragraphs_filtered = [p for p in paragraphs if p] # Goodbye empty strings
        
        # Our data structure of choice are JSONs (or dictionaries) with the keys being the speakers
        # The speakers are marked with four (4) # and the random noises with five (5) #
        speakers = [p[5:].strip() for p in paragraphs_filtered if p[:5] == "#### "] 
        dict_by_speakers = {s:[] for s in speakers} # repeating speakers are not a problem
        dict_by_speakers["NOISE"] = []
        
        speaker = "NOISE"
        for paragraph in paragraphs_filtered:
            if paragraph[:5] == "#### ":
                speaker = paragraph[5:].strip() # strip() removes trailing whitespaces
                continue
            elif paragraph[:5] == "#####":
                dict_by_speakers["NOISE"].append(paragraph[6:])
                continue
            else:
                # We split the paragraphs into sentences and append them to the latest speaker
                sentences = split_into_sentences(paragraph)
                for s in sentences:
                    if s != '' and len(s) < 250 and len(s.split(' ')) > 2:
                        dict_by_speakers[speaker].append(s.strip())
        
        dict_by_speakers = {speaker: sentences for speaker, sentences in dict_by_speakers.items() if sentences} # Eliminate empty lists
        
        with open('./_jsons/{}.json'.format(episode[-6:-3]), 'w') as json_file:
            json.dump(dict_by_speakers, json_file, indent=1)