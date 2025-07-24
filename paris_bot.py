import random
import time
import logging
from playwright.sync_api import sync_playwright

def run_bot():
    """
    Launches a headless browser, navigates to the specified URL,
    scrolls randomly, clicks a random button, waits, and closes.
    """
    logging.info("Bot starting...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            logging.info("Navigating to https://neousaxis.github.io/Paris-Vibes/")
            page.goto("https://neousaxis.github.io/Paris-Vibes/")

            # Simulate a random scroll
            scroll_height = page.evaluate("document.body.scrollHeight")
            random_scroll_position = random.randint(0, scroll_height)
            page.evaluate(f"window.scrollTo(0, {random_scroll_position})")
            logging.info(f"Scrolled to position: {random_scroll_position}")
            time.sleep(2) # Wait a bit after scrolling

            # Find all buttons and click one randomly
            buttons = page.query_selector_all("a.button")
            if buttons:
                random_button = random.choice(buttons)
                logging.info("Found buttons, clicking a random one...")
                random_button.click()
                
                logging.info("Waiting for 10 seconds...")
                page.wait_for_timeout(10000)
            else:
                logging.info("No buttons with class 'button' found.")

            browser.close()
            logging.info("Browser closed. Bot finished.")

    except Exception as e:
        logging.error(f"An error occurred during bot execution: {e}", exc_info=True)

if __name__ == "__main__":
    run_bot()
