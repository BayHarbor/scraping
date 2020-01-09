import tweepy as tw
import config # File with the creds

def sendTweet(content):
    # Authenticate
    auth = tw.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    # Post the tweet
    api.update_status(content)
