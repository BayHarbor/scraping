import os
import tweepy as tw
import pandas as pd
import config

auth = tw.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Post a tweet from Python
api.update_status("Test2")
