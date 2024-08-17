from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

# 創建一個選項對象來存儲你的自定義選項
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36")

# 初始化webdriver對象
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
# 首先導航到主網頁
driver.get('https://1campus.net')

time.sleep(1)

driver.delete_all_cookies()


# 添加你的cookies
cookies = [
    {"domain": ".1campus.net", "expirationDate": 1728871669.678601, "hostOnly": False, "httpOnly": False, "name": "_ga", "path": "/", "sameSite": "None", "secure": False, "session": False, "storeId": "0", "value": "GA1.1.1763465071.1688870172", "id": 1},
    {"domain": ".1campus.net", "expirationDate": 1728871671.521719, "hostOnly": False, "httpOnly": False, "name": "_ga_0XS98J4028", "path": "/", "sameSite": "None", "secure": False, "session": False, "storeId": "0", "value": "GS1.1.1694311474.2.1.1694311671.0.0.0", "id": 2},
    {"domain": "1campus.net", "expirationDate": 1694916470.593094, "hostOnly": True, "httpOnly": True, "name": "@ecoboost-web3", "path": "/", "sameSite": "None", "secure": True, "session": False, "storeId": "0", "value": "19a43522-900d-43bf-be36-1ceee0d6a78c", "id": 3},
    {"domain": "1campus.net", "expirationDate": 1694916470.593118, "hostOnly": True, "httpOnly": True, "name": "@ecoboost-web3.sig", "path": "/", "sameSite": "None", "secure": True, "session": False, "storeId": "0", "value": "bs4mFWRL-hmbVYKXhTtHoBcRuNo", "id": 4}
]

for cookie in cookies:
    driver.add_cookie(cookie)

time.sleep(1)
# 現在導航到特定的子頁面
driver.get('https://1campus.net/s/h.hwsh.tc.edu.tw/r/student/7006/g/agent/75036378-359E-4D92-8A9B-15437CBEDB6D')



iframe = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//iframe[@name="gadget-iframe-agent"]'))
)
driver.switch_to.frame(iframe)

nested_iframe = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//iframe[@title="Web2 Gadget"]'))
)
driver.switch_to.frame(nested_iframe)

club = "吉他社"
club_selector = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, f'//td[contains(text(), "{club}")]'))
)
    
if club_selector.is_displayed():
    club_selector.click()
else:
    print(f'元素存在但不可见: {club}')
    



time.sleep(60)