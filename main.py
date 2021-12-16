import json
from typing import Text
import tweepy

from time import sleep
from random import randint
from src.get_phrase import get_phrase

MIN_WAIT = 5  # min
MAX_WAIT = 60 # min

with open('keys.json', 'r') as f:
    consumer_key, consumer_secret, access_token, access_token_secret, bearer_token = json.load(f).values()
    
client = tweepy.Client( bearer_token=bearer_token, 
                        consumer_key=consumer_key, 
                        consumer_secret=consumer_secret, 
                        access_token=access_token, 
                        access_token_secret=access_token_secret,
                        wait_on_rate_limit=True)

while True:
    sleep(randint(MIN_WAIT, MAX_WAIT) * 60)
    client.create_tweet(text=get_phrase())