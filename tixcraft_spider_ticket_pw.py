import os
import time
import random
import ddddocr
import logging
import base64
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()
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

def buy_ticket(page):
    logger.info("Attempting to click 'Buy Ticket' button...")
    page.click("xpath=//*[@class='red large light'][contains(text(),'我要購票')]")
    logger.info("Successfully clicked 'Buy Ticket' button.")

def input_username(page, username):
    logger.info("Entering username...")
    page.fill("xpath=//*[@id='LOGIN_ID']", username)
    logger.info("Username entered successfully.")

def input_password(page, password):
    logger.info("Entering password...")
    page.fill("xpath=//*[@id='LOGIN_PWD']", password)
    logger.info("Password entered successfully.")

def booking_currently(page):
    logger.info("Attempting to click 'Book Now' button...")
    page.click("xpath=//*[@class='red'][contains(text(),'立即訂購')]")
    logger.info("Successfully clicked 'Book Now' button.")

def select_ticket_type(page):
    logger.info("Selecting ticket type...")
    page.click("xpath=//tr[@class='status_tr']//*[contains(text(),'對號座位')]")
    logger.info("Successfully selected ticket type.")

def default_price(page):
    logger.info("Selecting default price...")
    page.click("xpath=//button[contains(text(),'原價')]")
    logger.info("Successfully selected default price.")

def computer_selector(page):
    logger.info("Selecting 'Computer Seat Assignment'...")
    page.click("xpath=//div[@id='choice']//button[contains(text(), '電腦配位')]")
    logger.info("Successfully selected 'Computer Seat Assignment'.")

def click_plus_button(page):
    logger.info("Clicking plus button...")
    page.click("xpath=//button[@class='minus plus']")
    logger.info("Successfully clicked plus button.")

def select_get_ticket_method(page):
    logger.info("Select get ticket from 7-11")
    page.click("xpath=//*[@id='GET_METOD_ROOT']/label[2]")
    logger.info("Successfully clicked get ticket")
    
def click_agree(page):
    logger.info("Click agree")
    page.click("xpath=//*[@id='agreen']")
    logger.info("Successfully clicked agree")

def click_popup_alert(page):
    page.click("xpath=/html/body/div[1]/div[3]/div/button")

def select_empty_seats(page):
    logger.info("Selecting empty seats...")
    empty_seats = page.query_selector_all('css=td.empty.up')
    if len(empty_seats) >= 2:
        empty_seats[0].click()
        empty_seats[1].click()
        logger.info("Successfully selected empty seats.")
    else:
        logger.warning("Not enough adjacent seats available.")

def click_next_step(page):
    logger.info("Click next step")
    page.click("xpath=//*[@id='NEXT_BTN_SHOW']")
    logger.info("Successfully clicked next step")
    
def click_checkout(page):
    logger.info("Click checkout")
    page.click("xpath=//button[contains(text(), '結帳')]")
    logger.info("Successfully clicked checkout")
    
def process_captcha(page, ocr):
    logger.info("Processing captcha...")

    # Execute JavaScript code to get Base64 encoded image data
    image_data = page.evaluate("""
        (function() {
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
        })();
    """)

    if image_data:
        # Convert Base64 encoded data to binary data
        img_bytes = base64.b64decode(image_data)
        
        # Use OCR to recognize captcha
        captcha_text = ocr.classification(img_bytes)
        if captcha_text:
            logger.info(f"Captcha processed successfully, input: {captcha_text}")
            captcha_input = page.locator("xpath=//*[@id='CHK']")
            captcha_input.fill(captcha_text.upper())
        else:
            logger.error("Failed to recognize the captcha.")
    else:
        logger.error("Failed to retrieve the captcha image.")


def add_shopping_cart(page):
    logger.info("Adding to shopping cart...")
    page.click("xpath=//*[@id='addcart']/button")
    logger.info("Successfully added to shopping cart.")

def main():
    logger.info("Starting ticket booking process...")
    
    url = os.getenv("URL")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(url)
        
        ocr = ddddocr.DdddOcr()

        buy_ticket(page)
        booking_currently(page)
        computer_selector(page)

        rows = page.query_selector_all('tr.status_tr')

        available_tickets = []
        for row in rows:
            seats = row.query_selector('td[data-title="空位："]').inner_text().strip()
            if seats != "已售完":
                area = row.query_selector('td[data-title="票區："]').inner_text().strip()
                price = row.query_selector('td[data-title="票價："]').inner_text().strip()
                available_tickets.append({"Area": area, "Price": price, "Seats": seats, "Element": row})

        if available_tickets:
            selected_ticket = random.choice(available_tickets)
            logger.info(f"Selected ticket: {selected_ticket}")
            selected_ticket['Element'].click()
        else:
            logger.warning("No available tickets.")
        
        for _ in range(2):
            click_plus_button(page)
        
        input_username(page, username)
        input_password(page, password)

        process_captcha(page, ocr)
        
        add_shopping_cart(page)
        
        click_popup_alert(page)

        select_get_ticket_method(page)
        
        click_agree(page)
        
        click_next_step(page)
        
        time.sleep(600)
        browser.close()
        logger.info("Ticket booking process completed.")

if __name__ == "__main__":
    main()
