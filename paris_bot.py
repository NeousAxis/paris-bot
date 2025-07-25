import random
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_bot():
    logging.info("Bot starting...")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize the WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30) # Set a timeout for page loads

        logging.info("Navigating to https://neousaxis.github.io/Paris-Vibes/")
        driver.get("https://neousaxis.github.io/Paris-Vibes/")
        time.sleep(3) # Initial wait as requested

        # Simulate a random scroll
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        random_scroll_position = random.randint(0, scroll_height)
        driver.execute_script(f"window.scrollTo(0, {random_scroll_position})")
        logging.info(f"Scrolled to position: {random_scroll_position}")
        time.sleep(2) # Pause after scrolling

        # Iterate over all a.shortlink, click + close tab
        shortlinks = driver.find_elements(By.CSS_SELECTOR, "a.shortlink")
        if shortlinks:
            logging.info(f"Found {len(shortlinks)} shortlinks. Clicking them one by one...")
            main_window = driver.current_window_handle
            for link in shortlinks:
                try:
                    link.click()
                    # Wait for new tab to open and switch to it
                    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
                    new_window = [window for window in driver.window_handles if window != main_window][0]
                    driver.switch_to.window(new_window)
                    logging.info(f"Clicked shortlink: {link.get_attribute('href')}. Switched to new tab.")
                    time.sleep(5) # Wait for content to load in new tab
                    driver.close() # Close the new tab
                    driver.switch_to.window(main_window) # Switch back to main tab
                    logging.info("Closed new tab and switched back to main window.")
                except Exception as click_e:
                    logging.warning(f"Could not click or process shortlink {link.get_attribute('href')}: {click_e}")
        else:
            logging.info("No shortlinks found.")

        # Switch iframe #faucetFrame + click bouton claim
        try:
            logging.info("Attempting to switch to iframe #faucetFrame...")
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "faucetFrame")))
            logging.info("Switched to iframe. Looking for claim button...")
            # Assuming the claim button has a specific ID or class within the iframe
            # You might need to inspect the iframe content to find the correct selector
            claim_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Claim')] | //input[@value='Claim']")))
            claim_button.click()
            logging.info("Claim button clicked in iframe.")
            time.sleep(5) # Wait after clicking claim
            driver.switch_to.default_content() # Switch back to main content
            logging.info("Switched back to default content.")
        except Exception as iframe_e:
            logging.warning(f"Could not interact with iframe or claim button: {iframe_e}")

    except Exception as e:
        logging.error(f"An error occurred during bot execution: {e}", exc_info=True)
    finally:
        if 'driver' in locals() and driver:
            driver.quit()
            logging.info("Browser quit. Bot finished.")

if __name__ == "__main__":
    run_bot()
