import re  # Import the regular expression module for pattern matching
from playwright.sync_api import Playwright, sync_playwright, expect  # Import Playwright modules for browser automation
import time  # Import the time module for adding delays
import pandas as pd  # Import the pandas library for data manipulation

def run(playwright: Playwright) -> None:
    """
    This function automates the process of scraping Google Maps reviews for specified locations.
    It navigates to each location's page, extracts review information, and saves the data to a CSV file.
    """
    browser = playwright.chromium.launch(headless=False, slow_mo=100)  # Launch a Chromium browser instance. headless=False makes the browser visible, slow_mo adds a delay.
    context = browser.new_context()  # Create a new browser context.  A context provides an isolated environment for each scraping task.

    list_df_all_reviews = []  # Initialize an empty list to store DataFrames of reviews from all locations.
    pages = []  # Initialize an empty list to store page objects, location names, and location URLs.
    input_data = [
        {
            'location_name': 'マティーニバーガー',
            'share_url': 'https://maps.app.goo.gl/3L9NpDhg1y7VPEBw8'
        },
        {
            'location_name': 'ランタンバｰガｰ＆ステーキ Lantern burger＆steak',
            'share_url': 'https://maps.app.goo.gl/VLPT47gZSaVbcrN69'
        }
    ]  # Define a list of dictionaries containing location names and share URLs.
    df_locations = pd.DataFrame(input_data)  # Create a pandas DataFrame from the input data.

    for _, location in df_locations.iterrows():  # Iterate over each location in the DataFrame.
        location_name = location['location_name']  # Extract the location name from the DataFrame.
        location_url = location['share_url']  # Extract the share URL from the DataFrame.

        new_page = context.new_page()  # Create a new page within the browser context.
        new_page.goto(location_url)  # Navigate the page to the location URL.
        pages.append((new_page, location_name, location_url))  # Append the page object, location name, and URL to the pages list.

    for new_page, location_name, location_url in pages:  # Iterate over each page object, location name, and location URL in the pages list.
        new_page.wait_for_load_state('domcontentloaded') # Wait until the page's DOM content is fully loaded.
        
        # Wait for the "クチコミ" button to be visible and click it
        review_button = new_page.locator('button[role="tab"]:has-text("クチコミ")') # Locate the review button using its role and text.
        expect(review_button).to_be_enabled() # Assert that the review button is enabled.
        review_button.click() # Click the review button to navigate to the reviews section.

        # Wait for the specific element to appear and get total number of reviews
        review_count_element = new_page.wait_for_selector('div.jANrlb div.fontBodySmall') # Wait for the review count element to appear.
        review_count_text = review_count_element.inner_text() # Extract the inner text of the review count element.
        review_count = int(re.search(r'(\d+) 件のクチコミ', review_count_text).group(1)) # Extract the number of reviews from the text using a regular expression.
        
        # Print the number of reviews to the console
        print(f"Number of reviews: {review_count}") # Print the number of reviews to the console.
        
        # Wait for the reviews section to be fully loaded
        new_page.wait_for_selector('div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde div.jftiEf.fontBodyMedium') # Wait for the reviews section to be fully loaded.

        expect(new_page.get_by_role("button", name="クチコミの並べ替え")).to_be_enabled() # Assert that the sort button is enabled.
        new_page.get_by_role("button", name="クチコミの並べ替え").click() # Click the sort button to open the sort menu.
        expect(new_page.get_by_role("menu")).to_be_visible() # Assert that the sort menu is visible.
        new_page.get_by_role("menuitemradio", name="新しい順").click() # Click the "新しい順" (newest) menu item to sort reviews by newest.
        new_page.wait_for_load_state('domcontentloaded') # Wait until the page's DOM content is fully loaded.
        time.sleep(2) # Wait for 2 seconds to allow the reviews to reload.
        
        # Wait for the reviews to be reloaded in the newest order
        new_page.wait_for_selector('div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde div.jftiEf.fontBodyMedium') # Wait for the reviews to be reloaded in the newest order.

        # Scroll and collect all reviews
        loaded_reviews = 0 # Initialize a counter for the number of loaded reviews.
        while loaded_reviews < review_count: # Continue scrolling until all reviews are loaded.
            # Scroll down the review section
            review_section = new_page.locator('div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde') # Locate the review section.
            review_section.evaluate('element => element.scrollBy(0, element.scrollHeight)') # Scroll the review section to the bottom.
            new_page.wait_for_load_state('domcontentloaded') # Wait until the page's DOM content is fully loaded.
            print("Scrolling...") # Print "Scrolling..." to the console.

            # Get the number of loaded reviews
            loaded_reviews = new_page.locator('div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde div.jftiEf.fontBodyMedium').count() # Count the number of loaded reviews.
            print(f"Loaded reviews: {loaded_reviews}") # Print the number of loaded reviews to the console.

        # Collect all reviews text
        reviews = [] # Initialize an empty list to store review data.
        review_elements = new_page.locator('div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde div.jftiEf.fontBodyMedium') # Locate all review elements.
        for element in review_elements.element_handles(): # Iterate over each review element.
            reviewer_name = element.query_selector('div.WNxzHc.qLhwHc button.al6Kxe div.d4r55').inner_text() # Extract the reviewer name.
            
            # Extract the number of comments the user has made
            user_comments_element = element.query_selector('div.WNxzHc.qLhwHc button.al6Kxe div.RfnDt') # Locate the element containing the number of user comments.
            user_comments = user_comments_element.inner_text() if user_comments_element else "N/A" # Extract the number of user comments, or "N/A" if not found.
            
            stars = element.query_selector('div.DU9Pgb span.kvMYJc').get_attribute('aria-label') # Extract the star rating.
            time_of_review = element.query_selector('div.DU9Pgb span.rsqaWe').inner_text() # Extract the time of review.
            
            # Check for "もっと見る" button and click it if present
            more_button = element.query_selector('button.w8nwRe.kyuRq') # Locate the "もっと見る" (more) button.
            if more_button: # If the "もっと見る" button is present:
                more_button.click() # Click the "もっと見る" button to expand the review text.
                new_page.wait_for_selector('div.MyEned span.wiI7pd')  # Wait for the full text to load
            
            review_text_element = element.query_selector('div.MyEned span.wiI7pd') # Locate the review text element.
            review_text = review_text_element.inner_text().replace('\n', ' ') if review_text_element else "" # Extract the review text, replacing newlines with spaces.

            # Check for the share button and click it if present
            share_button = element.query_selector('button.GBkF3d[aria-label*="クチコミを共有"]') # Locate the share button.
            review_url = "" # Initialize an empty string for the review URL.
            if share_button: # If the share button is present:
                max_retries = 3 # Set the maximum number of retries.
                for attempt in range(max_retries): # Retry the following block up to max_retries times.
                    try:
                        share_button.click() # Click the share button.
                        
                        # Wait for the share dialog to open
                        new_page.wait_for_selector('div.yFnP6d div.kARmKf') # Wait for the share dialog to open.
                        
                        # Wait for the review URL input field to be visible and extract the URL
                        review_url_element = new_page.wait_for_selector('div.WVlZT input.vrsrZe') # Wait for the review URL input field to be visible.
                        review_url = review_url_element.get_attribute('value') # Extract the review URL from the input field.
                        
                        # Close the share dialog
                        new_page.query_selector('button[aria-label="閉じる"]').click() # Close the share dialog.
                    except Exception as e: # If an exception occurs:
                        print(f"Attempt {attempt + 1} failed: {e}") # Print the error message.
                        time.sleep(1) # Wait for 1 second before retrying.
            
            reviews.append({ # Append the review data to the reviews list.
                '場所名': location_name,  # Location Name
                '場所URL': location_url,  # Location URL
                'レビュアー名': reviewer_name,  # Reviewer Name
                'コメント数': user_comments,  # Number of Comments
                '評価': stars,  # Star Rating
                'レビュー日時': time_of_review,  # Time of Review
                'レビュー内容': review_text,  # Review Text
                'レビューURL': review_url  # Review URL
            })

        df_one_location_reviews = pd.DataFrame(reviews) # Create a pandas DataFrame from the reviews list.
        list_df_all_reviews.append(df_one_location_reviews) # Append the DataFrame to the list of all reviews.

    df_all_location_reviews = pd.concat(list_df_all_reviews, ignore_index=True) # Concatenate all DataFrames in the list into a single DataFrame.
    df_all_location_reviews.to_csv('google_maps_reviews.csv', index=False, encoding='utf-8-sig') # Save the DataFrame to a CSV file.

    # ---------------------
    context.close() # Close the browser context.
    browser.close() # Close the browser.


with sync_playwright() as playwright: # Launch Playwright and run the scraping function.
    run(playwright) # Call the run function with the Playwright instance.
