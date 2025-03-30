# CittadinanzaBot

A Telegram bot that monitors the Italian Consulate of Cordoba's website for new posts and sends instant notifications.

## Description

This bot is designed to help users stay informed about updates from the Italian Consulate of Cordoba's website. It periodically checks the website for new posts and sends instant notifications via Telegram to subscribed users. This is particularly useful for individuals interested in citizenship updates or other announcements from the consulate.

## Features

- **Automatic Website Monitoring:** Periodically checks the consulate's website for new content.
- **Instant Telegram Notifications:** Sends immediate notifications to users when new posts are detected.
- **Easy Configuration:** Uses environment variables for flexible and secure configuration.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd cittadinanzabot
    ```

2.  **Install dependencies using `uv`:**

    ```bash
    # Install uv
    pip install uv

    # It's highly recommended to use a virtual environment
    uv venv
    source .venv/bin/activate # or .\.venv\Scripts\activate on Windows

    #Use uv sync to create the virtual enviroment based on the toml file
    uv sync
    ```

3.  **Configure Environment Variables:**

    - Create a `.env` file in the project directory. See `.env.example` for the required environment variables.
    - Populate the `.env` file with the following:

      ```
      WORDPRESS_API_URL=<Your Wordpress API URL> #The url for the wordpress api endpoint
      TELEGRAM_BOT_TOKEN=<Your Telegram Bot Token> # Your Telegram Bot Token
      TELEGRAM_USER_ID=<Your Telegram User ID>   # Your Telegram User ID
      CHECK_INTERVAL=600                         # Check interval in seconds (default: 600 seconds = 10 minutes)
      DATA_FILE="last_post_data.json"            # File to store last post data (default: "last_post_data.json")
      ```

    - **Important:** Replace the placeholder values with your actual values. **DO NOT commit your `.env` file to a public repository!** Add it to your `.gitignore`.

4.  **Run the bot:**

    ```bash
    python main.py
    ```

## Usage

1.  **Start the bot:** Run the main Python script. The bot will begin monitoring the consulate's website in the background.
2.  **Interact with the bot via Telegram:** Users will automatically receive notifications when new posts are detected on the consulate's website.

## Configuration

The following environment variables are used to configure the bot:

- `WORDPRESS_API_URL`: The URL of the WordPress API endpoint for the consulate's website.
- `TELEGRAM_BOT_TOKEN`: The API token for your Telegram bot. You can obtain this from BotFather on Telegram.
- `TELEGRAM_USER_ID`: The Telegram user ID of the user who will receive notifications.
- `CHECK_INTERVAL`: The interval (in seconds) at which the bot checks the consulate's website for new posts. Defaults to 600 seconds (10 minutes).
- `DATA_FILE`: The name of the file used to store the data of the last processed post. Defaults to `last_post_data.json`.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Ezequiel Cavallo (<ezecavallo@gmail.com>)
