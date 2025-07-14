# Microblogging CLI

A command-line tool to post to multiple microblogging platforms.

## Setup

1. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Set up environment variables:**

    Create a `.env` file in the root of the project and add the following:

    ```
    X_CONSUMER_KEY="your_consumer_key"
    X_CONSUMER_SECRET="your_consumer_secret"
    X_ACCESS_TOKEN="your_access_token"
    X_ACCESS_TOKEN_SECRET="your_access_token_secret"

    BLUESKY_HANDLE="your_bluesky_handle"
    BLUESKY_APP_PASSWORD="your_bluesky_app_password"

    THREADS_ACCESS_TOKEN="your_access_token"
    ```

## Usage

1. **Place an image file** (e.g., `.jpg`, `.png`) in the same directory as the script.
2. Run the script:

    ```bash
    python src/main.py
    ```

3. Enter the text for your post when prompted. If you leave the text empty, the image's filename will be used as the post text.
