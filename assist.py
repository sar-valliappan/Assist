from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

with open('codes.json', 'r') as file:
    data = json.load(file)

cc_codes = []
for agreement in list(data):
    if agreement['isCommunityCollege']:
        school_id = agreement['id']
        cc_codes.append(school_id)

print(cc_codes)

'''
driver = None  # Initialize driver variable outside try block
try:
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # URL of the webpage
    url = 'https://assist.org/transfer/results?year=75&institution=7&agreement=150&agreementType=from&view=agreement&viewBy=dept&viewSendingAgreements=false&viewByKey=75%2F150%2Fto%2F7%2FAllDepartments'
    driver.get(url)

    # Wait for the presence of an element specified by XPath
    search = True
    i = 1
    while (search):
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//awc-agreement-row[{i}]'))
        )
        if ("MATH 20A" in element.text) :
            print("Element found: ", element.text)
            search = False
        i += 1
    
    # If the element is found, print its text (or handle it as needed)
    print("Element found: ", element.text)


except TimeoutException:
    print("Timed out waiting for page to load or element to appear.")
except WebDriverException as e:
    print(f"WebDriver encountered an issue: {e}")
finally:
    # Ensure the driver quits no matter what
    if driver is not None:  # Only quit if driver was succjssfully created
        driver.quit()
'''