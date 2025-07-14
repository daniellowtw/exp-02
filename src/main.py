import os
import tweepy
from atproto import Client
from dotenv import load_dotenv

load_dotenv()

def post_to_x(text):
    # Authenticate to X
    consumer_key = os.getenv("X_CONSUMER_KEY")
    consumer_secret = os.getenv("X_CONSUMER_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    # Post the tweet
    try:
        response = client.create_tweet(text=text)
        print(f"Successfully posted to X: {response.data['id']}")
    except Exception as e:
        print(f"Error posting to X: {e}")

def post_to_bluesky(text):
    # Authenticate to Blue Sky
    bluesky_handle = os.getenv("BLUESKY_HANDLE")
    bluesky_password = os.getenv("BLUESKY_APP_PASSWORD")

    client = Client()
    profile = client.login(bluesky_handle, bluesky_password)
    print(profile.display_name)

    # Post the skeet
    try:
        response = client.send_post(text=text)
        print(f"Successfully posted to Blue Sky: {response.uri}")
    except Exception as e:
        print(f"Error posting to Blue Sky: {e}")

def main():
    text = input("Enter the text to post: ")
    post_to_x(text)
    post_to_bluesky(text)

if __name__ == "__main__":
    main()
