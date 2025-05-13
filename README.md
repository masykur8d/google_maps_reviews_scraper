# Google Maps Reviews Scraper
[日本語版](README_ja.md)

## Overview

This Python script automates the process of scraping Google Maps reviews for specified locations using the Playwright library. It navigates to each location's page, extracts review information such as reviewer name, number of comments, star rating, review date/time, review text, and review URL, and saves the data to a CSV file.

## Features

-   **Automated Scraping:** Uses Playwright to automate browser interactions, including navigating to Google Maps locations, clicking buttons, and scrolling to load reviews.
-   **Data Extraction:** Extracts key review information such as reviewer name, number of comments, star rating, review date/time, review text, and review URL.
-   **CSV Export:** Saves the extracted data to a CSV file (`google_maps_reviews.csv`) for easy analysis and storage.
-   **Error Handling:** Implements retry logic for extracting review URLs to handle potential issues with the Google Maps interface.

## Requirements

-   Python 3.6+
-   Playwright library
-   Pandas library
-   Other dependencies specified in `requirements.txt`

## Installation

1.  Clone this repository:

    ```bash
    git clone https://github.com/masykur8d/google_maps_reviews_scraper.git
    cd google_maps_reviews_scraper
    ```

2.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Modify Input Data:**
    -   Edit the `main.py` file to update the `input_data` list with the desired Google Maps locations and share URLs.

    ```python
    input_data = [
        {
            'location_name': 'マティーニバーガー',
            'share_url': 'https://maps.app.goo.gl/3L9NpDhg1y7VPEBw8'
        },
        {
            'location_name': 'ランタンバｰガｰ＆ステーキ Lantern burger＆steak',
            'share_url': 'https://maps.app.goo.gl/VLPT47gZSaVbcrN69'
        }
    ]
    ```

2.  **Run the Script:**

    ```bash
    python main.py
    ```

3.  **View Results:**
    -   The scraped data will be saved in a CSV file named `google_maps_reviews.csv` in the same directory as the script.

## Docker

To run this application using Docker, follow these steps:

1.  **Build the Docker Image:**

    ```bash
    docker build -t google-maps-reviews .
    ```

2.  **Run the Docker Container:**

    ```bash
    docker run google-maps-reviews
    ```

    This command will execute the script inside a Docker container, using the specified Dockerfile. The resulting `google_maps_reviews.csv` file will be created within the container's file system. To access this file, you may need to copy it from the container to your host machine.

## Code Explanation

-   **Import Libraries:** Imports necessary libraries such as `re`, `playwright`, `time`, and `pandas`.
-   **`run` Function:**
    -   Launches a Chromium browser instance using Playwright.
    -   Creates a new browser context for each scraping task.
    -   Iterates over the list of locations, navigates to each location's page, and extracts review information.
    -   Saves the extracted data to a CSV file.
-   **Main Execution Block:**
    -   Uses `sync_playwright` to launch Playwright and run the `run` function.

## Best Practices

-   **Respect `robots.txt`:** Check the `robots.txt` file of the Google Maps website to ensure that scraping is allowed.
-   **Add Delays:** Use `time.sleep()` to add delays between requests to avoid overloading the server and getting IP banned.
-   **Error Handling:** Implement robust error handling to catch exceptions and prevent the script from crashing.
-   **User Agent:** Set a custom user agent to identify your script and avoid being blocked.
-   **Rate Limiting:** Implement rate limiting to control the number of requests per unit of time.
-   **Headless Mode:** Run the browser in headless mode to reduce resource consumption.
-   **Data Validation:** Validate the extracted data to ensure its accuracy and completeness.

## Disclaimer

This script is intended for educational and research purposes only. Scraping Google Maps reviews may violate the terms of service of the Google Maps website. Use this script at your own risk.
