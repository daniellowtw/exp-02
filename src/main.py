import os
import tweepy
import requests
from atproto import Client, models
from dotenv import load_dotenv

load_dotenv()

THREADS_GRAPH_API_BASE_URL = "https://graph.threads.net/v1.0/"

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
            print("Successfully uploaded media to X.")
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

def post_to_threads(text, image_path=None):
    # Authenticate to Threads
    access_token = os.getenv("THREADS_ACCESS_TOKEN") # Threads uses the same token

    try:
        if image_path: 
            # NOTE: UNTESTED!
            # 1. Create a media container for the image.
            data = {
                'media_type': 'IMAGE',
                'image_url': 'YOUR_PUBLIC_IMAGE_URL_HERE', # This needs to be a publicly accessible URL
                'caption': text,
                'access_token': access_token
            }
            # For local files, you'd need to upload them to a public server first.
            # For now, we'll use a placeholder for image_url.
            # The Threads API requires a public URL for images/videos.
            # This example assumes you have a public URL for the image.
            # In a real application, you'd upload the image to a service like AWS S3, Cloudinary, etc.
            # and then use the URL provided by that service.
            # For demonstration purposes, I'm using a placeholder.
            # If you want to test with a local image, you'll need to host it publicly first.
            print("Note: For image posts to Threads, the image must be hosted on a public server.")
            print("Please replace 'YOUR_PUBLIC_IMAGE_URL_HERE' with the actual public URL of your image.")
            
            # For now, let's assume a placeholder URL for testing purposes.
            # In a real scenario, you'd have a mechanism to get this URL.
            # For this example, I'll use a dummy URL.
            data['image_url'] = "https://example.com/your_image.jpg" # Placeholder

            response = requests.post(f"{THREADS_GRAPH_API_BASE_URL}me/threads", json=data)
            response.raise_for_status()
            container_id = response.json()['id']
            print(f"Created media container with ID: {container_id}")

            # 2. Publish the media container.
            publish_data = {
                'creation_id': container_id,
                'access_token': access_token
            }
            response = requests.post(f"{THREADS_GRAPH_API_BASE_URL}me/threads_publish", json=publish_data)
            response.raise_for_status()
            print(f"Successfully posted to Threads with image: {response.json()['id']}")
        else:
            # 1. Create a media container for text only.
            data = {
                'text': text,
                'access_token': access_token,
                'media_type': 'TEXT'  # Assuming Threads API supports text-only posts
            }
            response = requests.post(f"{THREADS_GRAPH_API_BASE_URL}me/threads", params=data)
            response.raise_for_status()
            container_id = response.json()['id']
            print(f"Created media container with ID: {container_id}")

            # 2. Publish the text container.
            publish_data = {
                'creation_id': container_id,
                'access_token': access_token
            }
            response = requests.post(f"{THREADS_GRAPH_API_BASE_URL}me/threads_publish", json=publish_data)
            response.raise_for_status()
            print(f"Successfully posted to Threads: {response.json()['id']}")
    except requests.exceptions.RequestException as e:
        print(f"Error posting to Threads: {e}")

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
    post_to_threads(text, image_path)

if __name__ == "__main__":
    main()