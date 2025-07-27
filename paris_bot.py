from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration 2Captcha\API
API_KEY = os.getenv("TWOCAPTCHA_API_KEY")

# Initialisation du navigateur
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

# Résolution de reCAPTCHA via 2Captcha
def solve_recaptcha(site_key, page_url):
    resp = requests.get(
        "http://2captcha.com/in.php", params={
            'key': API_KEY,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': page_url,
            'json': 1
        }
    ).json()
    captcha_id = resp.get('request')

    for _ in range(30):
        time.sleep(5)
        result = requests.get(
            "http://2captcha.com/res.php", params={
                'key': API_KEY,
                'action': 'get',
                'id': captcha_id,
                'json': 1
            }
        ).json()
        if result.get('status') == 1:
            return result.get('request')
    raise Exception("Timeout solving reCAPTCHA")

# Résolution de Turnstile Cloudflare via 2Captcha
def solve_turnstile(site_key, page_url):
    resp = requests.get(
        "http://2captcha.com/in.php", params={
            'key': API_KEY,
            'method': 'turnstile',
            'sitekey': site_key,
            'pageurl': page_url,
            'json': 1
        }
    ).json()
    captcha_id = resp.get('request')

    for _ in range(30):
        time.sleep(5)
        result = requests.get(
            "http://2captcha.com/res.php", params={
                'key': API_KEY,
                'action': 'get',
                'id': captcha_id,
                'json': 1
            }
        ).json()
        if result.get('status') == 1:
            return result.get('request')
    raise Exception("Timeout solving Turnstile")

# Handler ShrinkEarn
def handle_shrinkearn():
    url = "https://tpi.li/Balade_Monmartre"
    driver.get(url)
    try:
        sitekey = driver.find_element(By.CSS_SELECTOR, 'div.g-recaptcha').get_attribute('data-sitekey')
        token = solve_recaptcha(sitekey, url)
        driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = arguments[0];", token)
        driver.execute_script("___grecaptcha_cfg.clients[0].Z.Z.callback(arguments[0]);", token)
        skip_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Skip Ad")))
        skip_btn.click()
        wait.until(EC.url_changes(url))
        print("✅ ShrinkEarn redirigé vers :", driver.current_url)
    except Exception as e:
        print("❌ ShrinkEarn erreur :", e)

# Handler OUO
def handle_ouo():
    url = "https://ouo.io/rZMB9W"
    driver.get(url)
    try:
        time.sleep(3)
        sitekey = driver.find_element(By.CSS_SELECTOR, 'div.cf-turnstile').get_attribute('data-sitekey')
        token = solve_turnstile(sitekey, url)
        driver.execute_script("document.querySelector('textarea[name=\"cf-turnstile-response\"]').innerHTML = arguments[0];", token)
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            try:
                driver.switch_to.frame(iframe)
                btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#btn-main")))
                btn.click()
                driver.switch_to.default_content()
                wait.until(EC.url_changes(url))
                print("✅ OUO redirigé vers :", driver.current_url)
                return
            except:
                driver.switch_to.default_content()
                continue
        print("❌ OUO: bouton introuvable après injection Turnstile.")
    except Exception as e:
        print("❌ OUO erreur :", e)

# Handler AdFoc
def handle_adfoc():
    url = "http://adfoc.us/8733161"
    driver.get(url)
    try:
        time.sleep(15)
        print("✅ AdFoc.us visité :", driver.current_url)
    except Exception as e:
        print("❌ AdFoc erreur :", e)

# Exécution
def main():
    handle_shrinkearn()
    handle_ouo()
    handle_adfoc()
    driver.quit()

if __name__ == '__main__':
    main()