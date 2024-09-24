import os
import time
import random
import ddddocr
import logging
import pytesseract
from PIL import Image
from io import BytesIO
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load environment variables from .env file
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
    """Click on the 'Buy Ticket' button."""
    logger.info("Attempting to click 'Buy Ticket' button...")
    page.click("xpath=//*[@class='buy']//div[contains(text(),'立即購票')]")
    logger.info("Successfully clicked 'Buy Ticket' button.")

def buy_now(page):
    """Click on the 'Buy Now' button for available games or events."""
    logger.info("Attempting to click 'Buy Now' button...")
    page.click("xpath=//*[@id='gameList']//tr/td[4]/button")
    logger.info("Successfully clicked 'Buy Now' button.")

def process_captcha(page):
    """Download and process captcha using OCR."""
    logger.info("Processing captcha...")
    
    captcha_image = page.locator('#TicketForm_verifyCode-image')
    captcha_image_src = captcha_image.get_attribute('src')
    
    # Download captcha image
    captcha_image_response = page.request.get(captcha_image_src)
    image_bytes = captcha_image_response.body()

    # Open image with Pillow
    image = Image.open(BytesIO(image_bytes))

    # Use Tesseract OCR to read captcha
    captcha_text = pytesseract.image_to_string(image)

    logger.info(f'Captcha text: {captcha_text}')
    return captcha_text

def select_random_ticket(page):
    """Select a random available ticket from the list."""
    logger.info("Selecting random ticket...")
    selectable_tickets = page.query_selector_all('.select_form_b a[style="opacity: 1;"]')

    if selectable_tickets:
        random_ticket = random.choice(selectable_tickets)
        random_ticket.click()
        logger.info("Random ticket selected and clicked.")
    else:
        logger.warning("No available tickets to select.")

def agree_terms(page):
    """Agree to terms and conditions and proceed."""
    logger.info("Agreeing to terms and conditions...")
    page.click('#TicketForm_agree')
    logger.info("Successfully agreed to terms and conditions.")

def select_payment_method(page):
    """Select payment method (e.g., Credit Card)."""
    logger.info("Selecting payment method (Credit Card)...")
    page.click('#CheckoutForm_paymentId_36')
    logger.info("Payment method selected (Credit Card).")

def submit_order(page):
    """Submit the order and proceed to the next step."""
    logger.info("Submitting the order...")
    page.click('#submitButton')
    logger.info("Order submitted.")

def select_ticket_quantity(page, quantity='2'):
    """Select ticket quantity by matching any possible ticketPrice select element."""
    logger.info("Selecting ticket quantity...")

    # Use a wildcard selector to match any element whose ID starts with 'TicketForm_ticketPrice_'
    select_element = page.query_selector('select[id^="TicketForm_ticketPrice_"]')

    if select_element:
        page.select_option(select_element, quantity)
        logger.info(f"Ticket quantity {quantity} selected.")
    else:
        logger.warning("No valid ticket quantity select element found.")

def main():
    """Main function to automate the ticket booking process."""
    logger.info("Starting ticket booking process...")

    # Load necessary environment variables
    url = os.getenv("URL")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to the target URL
        page.goto(url)

        # Step 1: Buy ticket
        buy_ticket(page)
        
        # Step 2: Select event/game and proceed
        buy_now(page)

        # Step 3: Select a random available ticket
        select_random_ticket(page)

        # Step 4: Select the ticket quantity (2 in this case)
        logger.info("Selecting ticket quantity...")
        select_ticket_quantity(page, '2')
        logger.info("Ticket quantity selected.")

        # Step 5: Process captcha
        process_captcha(page)

        # Step 6: Agree to terms and conditions
        agree_terms(page)

        # Step 7: Confirm the ticket count
        logger.info("Confirming ticket count...")
        page.click('button.btn.btn-primary.btn-green')
        logger.info("Ticket count confirmed.")

        # Step 8: Select payment method
        select_payment_method(page)

        # Step 9: Submit the order
        submit_order(page)

        # Sleep to keep the browser open (adjust as needed)
        time.sleep(600)

        # Close the browser after completing the process
        browser.close()
        logger.info("Ticket booking process completed.")

if __name__ == "__main__":
    main()
