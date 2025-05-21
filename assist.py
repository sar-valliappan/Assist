from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import urllib
import ssl
import certifi

context = ssl.create_default_context(cafile=certifi.where())
with urllib.request.urlopen(
    f'https://assist.org/api/institutions/7/agreements', 
    context=context
    ) as url:
    data = json.loads(url.read().decode())
cc_codes = []
for college in list(data):
    if college['isCommunityCollege']:
        school_id = college['institutionParentId']
        school_name = college['institutionName']
        curr = {'name': school_name, 'id': school_id}
        cc_codes.append(curr)

prefix = input("Prefix: ")
number = input("Number: ")

def getPrefixCode(code):
    time.sleep(0.1)
    with urllib.request.urlopen(
        f'https://assist.org/api/agreements?receivingInstitutionId=7&sendingInstitutionId={code}&academicYearId=75&categoryCode=prefix',
        context=context
    ) as url:
        data = json.loads(url.read().decode())
    data = data['reports']
    for report in list(data):
        if prefix in report['label'] and report['ownerInstitutionId'] == 7:
            prefixCode = report['key']
            prefixList = prefixCode.split("/")
            prefixCode = prefixList[-1]
    return prefixCode


driver = None
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

for code in cc_codes:
    name = code["name"]
    id = code["id"]
    print(name)

    #Compton Community College doesn't exist anymore
    if (id == 34):
        continue

    prefixCode = getPrefixCode(id)
    print(prefixCode)
    print(id)

    try:
        url = f'https://assist.org/transfer/results?year=75&institution=7&agreement={id}&agreementType=from&view=agreement&viewBy=prefix&viewByKey=75%2F{id}%2Fto%2F7%2FPrefix%2F{prefixCode}'
        driver.get(url)
        
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

    except TimeoutException:
        print("Timed out waiting for page to load or element to appear.")
    except WebDriverException as e:
        print(f"WebDriver encountered an issue: {e}")

if driver is not None:
    driver.quit()