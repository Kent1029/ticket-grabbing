import json
import os
import time
import random
import ddddocr
import logging
import base64
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ticket_booking.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def buy_ticket(driver):
    logger.info("Attempting to click 'Buy Ticket' button...")
    buy_ticket_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@class='red large light'][contains(text(),'我要購票')]"))
    )
    buy_ticket_button.click()
    logger.info("Successfully clicked 'Buy Ticket' button.")

def input_username(driver, username):
    logger.info("Entering username...")
    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='LOGIN_ID']"))
    )
    username_input.send_keys(username)
    logger.info("Username entered successfully.")

def input_password(driver, password):
    logger.info("Entering password...")
    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='LOGIN_PWD']"))
    )
    password_input.send_keys(password)
    logger.info("Password entered successfully.")

def booking_currently(driver):
    logger.info("Attempting to click 'Book Now' button...")
    booking_currently_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@class='red'][contains(text(),'立即訂購')]"))
    )
    booking_currently_button.click()
    logger.info("Successfully clicked 'Book Now' button.")

def select_ticket_type(driver):
    logger.info("Selecting ticket type...")
    ticket_type = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//tr[@class='status_tr']//*[contains(text(),'對號座位')]"))
    )
    ticket_type.click()
    logger.info("Successfully selected ticket type.")

def default_price(driver):
    logger.info("Selecting default price...")
    default_price = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'原價')]"))
    )
    default_price.click()
    logger.info("Successfully selected default price.")

def computer_selector(driver):
    logger.info("Selecting 'Computer Seat Assignment'...")
    computer_selector_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='choice']//button[contains(text(), '電腦配位')]"))
    )
    computer_selector_button.click()
    logger.info("Successfully selected 'Computer Seat Assignment'.")

def click_plus_button(driver):
    logger.info("Clicking plus button...")
    plus_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='minus plus']"))
    )
    plus_button.click()
    logger.info("Successfully clicked plus button.")

def select_empty_seats(driver):
    logger.info("Selecting empty seats...")
    empty_seats = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td.empty.up'))
    )
    if len(empty_seats) >= 2:
        empty_seats[0].click()
        empty_seats[1].click()
        logger.info("Successfully selected empty seats.")
    else:
        logger.warning("Not enough adjacent seats available.")

def process_captcha(driver, ocr):
    logger.info("Processing captcha...")

    # Execute JavaScript code to get Base64 encoded image data
    image_data = driver.execute_script("""
        function ticket_get_ocr_image() {
            let image_data = "";
            let image_id = 'chk_pic';
            let img = document.getElementById(image_id);
            if (img != null) {
                let canvas = document.createElement('canvas');
                let context = canvas.getContext('2d');
                canvas.height = img.naturalHeight;
                canvas.width = img.naturalWidth;
                context.drawImage(img, 0, 0);
                let img_data = canvas.toDataURL();
                if (img_data) {
                    image_data = img_data.split(",")[1];
                }
            }
            return image_data;
        }
        return ticket_get_ocr_image();
    """)

    if image_data:
        # Convert Base64 encoded data to binary data
        img_bytes = base64.b64decode(image_data)
        
        # Use OCR to recognize captcha
        captcha_text = ocr.classification(img_bytes)
        if captcha_text:
            logger.info(f"Captcha processed successfully, input: {captcha_text}")
            captcha_input = driver.find_element(By.XPATH, "//*[@id='CHK']")
            captcha_input.send_keys(captcha_text.upper())
        else:
            logger.error("Failed to recognize the captcha.")
    else:
        logger.error("Failed to retrieve the captcha image.")

def add_shopping_cart(driver):
    logger.info("Adding to shopping cart...")
    add_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='addcart']/button"))
    )
    add_button.click()
    logger.info("Successfully added to shopping cart.")

def filter_and_add_cookies(driver, cookies):
    logger.info("Adding cookies...")
    for cookie in cookies:
        if cookie.get('httpOnly'):
            continue
        if 'sameSite' in cookie and cookie['sameSite'] not in ["Strict", "Lax", "None"]:
            del cookie['sameSite']
        driver.add_cookie(cookie)
    logger.info("Cookies added successfully.")

def main():
    logger.info("Starting ticket booking process...")
    home_page = "https://kham.com.tw/application/UTK02/UTK0201_.aspx?PRODUCT_ID=P0KYQBSU#"
    chrome_options = Options()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-images")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.maximize_window()
    driver.get(home_page)
    
    ocr = ddddocr.DdddOcr()

    buy_ticket(driver)
    booking_currently(driver)
    computer_selector(driver)

    rows = driver.find_elements(By.CSS_SELECTOR, 'tr.status_tr')

    available_tickets = []
    for row in rows:
        seats = row.find_element(By.CSS_SELECTOR, 'td[data-title="空位："]').text.strip()
        if seats != "已售完":
            area = row.find_element(By.CSS_SELECTOR, 'td[data-title="票區："]').text.strip()
            price = row.find_element(By.CSS_SELECTOR, 'td[data-title="票價："]').text.strip()
            ticket_element = row.find_element(By.CSS_SELECTOR, 'td')
            available_tickets.append({"Area": area, "Price": price, "Seats": seats, "Element": ticket_element})

    if available_tickets:
        selected_ticket = random.choice(available_tickets)
        logger.info(f"Selected ticket: {selected_ticket}")
        selected_ticket['Element'].click()
    else:
        logger.warning("No available tickets.")

    threads = []

    for _ in range(2):
        thread = threading.Thread(target=click_plus_button, args=(driver,))
        threads.append(thread)
        thread.start()
    
    threads.append(threading.Thread(target=input_username, args=(driver, "@gmail.com")))
    threads.append(threading.Thread(target=input_password, args=(driver, "")))

    for thread in threads[-2:]:
        thread.start()

    for thread in threads:
        thread.join()

    process_captcha(driver, ocr)
    
    add_shopping_cart(driver)
    
    time.sleep(600)
    driver.quit()
    logger.info("Ticket booking process completed.")

if __name__ == "__main__":
    main()
