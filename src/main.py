import os
import tweepy
from atproto import Client, models
from dotenv import load_dotenv

load_dotenv()

def find_image_path():
    supported_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    for file in os.listdir('.'):
        if os.path.isfile(file):
            ext = os.path.splitext(file)[1].lower()
            if ext in supported_extensions:
                return file
    return None

def post_to_x(text, image_path=None):
    # Authenticate to X
    consumer_key = os.getenv("X_CONSUMER_KEY")
    consumer_secret = os.getenv("X_CONSUMER_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    # v2 client for creating the tweet
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    media_id = None
    if image_path:
        # v1.1 API for media uploads
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        api_v1 = tweepy.API(auth)
        try:
            media = api_v1.media_upload(filename=image_path)
            media_id = media.media_id_string
            print(f"Successfully uploaded media to X.")
        except Exception as e:
            print(f"Error uploading media to X: {e}")
            return

    # Post the tweet
    try:
        media_ids = [media_id] if media_id else None
        response = client.create_tweet(text=text, media_ids=media_ids)
        print(f"Successfully posted to X: {response.data['id']}")
    except Exception as e:
        print(f"Error posting to X: {e}")

def post_to_bluesky(text, image_path=None):
    # Authenticate to Blue Sky
    bluesky_handle = os.getenv("BLUESKY_HANDLE")
    bluesky_password = os.getenv("BLUESKY_APP_PASSWORD")

    client = Client()
    client.login(bluesky_handle, bluesky_password)

    # Post the skeet
    try:
        if image_path:
            with open(image_path, 'rb') as f:
                img_data = f.read()
            
            upload = client.upload_blob(img_data)
            embed = models.AppBskyEmbedImages.Main(
                images=[models.AppBskyEmbedImages.Image(alt=text, image=upload.blob)]
            )
            response = client.send_post(text=text, embed=embed)
            print(f"Successfully posted to Blue Sky with image: {response.uri}")
        else:
            response = client.send_post(text=text)
            print(f"Successfully posted to Blue Sky: {response.uri}")
    except Exception as e:
        print(f"Error posting to Blue Sky: {e}")

def main():
    image_path = find_image_path()
    prompt_text = "Enter the text to post: "
    if image_path:
        print(f"Found image: {image_path}. Attaching to posts.")
        prompt_text = "Enter the text to post (leave empty to use filename as text): "

    text = input(prompt_text)
    if image_path and not text:
        text = os.path.splitext(os.path.basename(image_path))[0]

    post_to_x(text, image_path)
    post_to_bluesky(text, image_path)

if __name__ == "__main__":
    main()
