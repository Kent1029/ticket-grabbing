from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import ddddocr
import os
import xml.etree.ElementTree as ET
import cairosvg

def convert_svg_to_png(svg_content, output_file='code.png'):
    cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to=output_file)


# 創建一個選項對象來存儲你的自定義選項
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36")

# 初始化webdriver對象
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
# 首先導航到主網頁
driver.get('https://ticketplus.com.tw/activity/4c035106b9449d8213a6021f56fe1cd7')
wait = WebDriverWait(driver, 10)

buy_ticket_button = driver.find_element(By.XPATH, "//*[@id='buyTicket']//*[contains(text(),'立即購票')]")
buy_ticket_button.click()

phone_number_input = driver.find_element(By.XPATH, "//*[contains(@id,'_phone_number')]")
password_input = driver.find_element(By.XPATH, "//form//*[contains(@id,'input-')]")

phone_number_input.send_keys("900248311")
password_input.send_keys("Haru0900248311")
login = driver.find_element(By.XPATH, "//form//button//*[contains(text(), '登入')]")
login.click()


plus_button = wait.until(
    EC.presence_of_element_located((By.XPATH, '//div[@class="col-sm-3 col-3 align-self-center px-4 text-center"]//button[2]//span[@class="v-btn__content"]'))
)

plus_button.click()
plus_button.click()

img_code = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.captcha-img svg'))
)
svg_content = img_code.get_attribute('outerHTML')
# 使用ElementTree解析SVG內容
root = ET.fromstring(svg_content)
for child in root:
    print(child.tag, child.attrib)
convert_svg_to_png(svg_content)


ocr = ddddocr.DdddOcr()
with open("code.png", "rb") as fp:
    image = fp.read()

catch = ocr.classification(image)
if not catch:
    print("Failed to recognize the captcha.")
code = driver.find_element(By.XPATH, '//div[contains(@class, "recaptcha-area")]//*[contains(@id,"input-")]')

print(catch)
code.send_keys(catch)
os.remove("code.png")
checked = wait.until(
    EC.presence_of_element_located((By.XPATH, '//div[@class="d-flex justify-end align-center px-4 col-sm-6 col-4"]//input[contains(@id,"input-")]'))
)
checked.click()

selected_payway = driver.find_element(By.XPATH, '//div[@id="selectedPayWay"]//div[@role="radiogroup"]/div[2]//label')
selected_payway.click()

pay_button = driver.find_element(By.XPATH, '//span[contains(text(), "前往付款")]')
pay_button.click()

time.sleep(60)

driver.quit()