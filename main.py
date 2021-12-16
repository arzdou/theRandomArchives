'''
For now the main file just creates the text of the tweet
'''

import json
from random import randint, choice

DIRECTORY = './_jsons'

episode_number = randint(1, 200)
file_name = '{}.json'.format(episode_number)
file_name = (8-len(file_name))*'0' + file_name   # This ensures that the leading 0s are always correct

with open('{}/{}'.format(DIRECTORY, file_name)) as f:
    statement = json.load(f)
    
speaker = choice(list(statement.keys()))
phrase = choice(statement[speaker])
if speaker == "NOISE":
    text = phrase
else:
    text = '{}: {}'.format(speaker, phrase)

print(text)