import os
import tweepy

def post_tweet(message, image_path=None):
    auth = tweepy.OAuth1UserHandler(
        os.getenv('TWITTER_API_KEY'),
        os.getenv('TWITTER_API_SECRET'),
        os.getenv('TWITTER_ACCESS_TOKEN'),
        os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )
    api = tweepy.API(auth)

    if image_path:
        api.update_status_with_media(status=message, filename=image_path)
    else:
        api.update_status(status=message)
