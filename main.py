import os, zipfile, getpass
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

login_id = '<assessor-id>'
username = '<username>'
password = getpass.getpass()

series = 'June 2023'
centre_number = input('Centre number: ')

# Replace username with your username and make sure to create the OCR_JUNE_2023 directory
# Alternatively just replace the whole path with one of your preference
download_directory = f'/Users/<pc-username>/Documents/OCR_JUNE_2023/{centre_number}'
if not os.path.exists(download_directory):
   os.makedirs(download_directory)

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : download_directory}
chrome_options.add_experimental_option('prefs', prefs)

# Replace this path with a path to your chosen driver
# The path you can see here references the M1 Mac Chrome Driver within this repo
# https://chromedriver.chromium.org/downloads
chrome_driver_service = Service('chromedriver_mac_arm64/chromedriver')
driver = webdriver.Chrome(service=chrome_driver_service, options=chrome_options)

driver.get('https://repository.ocr.org.uk/CentresOverview.aspx')

driver.find_element(By.CLASS_NAME, 'LoginId').send_keys(login_id)
driver.find_element(By.CLASS_NAME, 'Username').send_keys(username)
driver.find_element(By.CLASS_NAME, 'Password').send_keys(password)

driver.find_element(By.CLASS_NAME, 'Button').click()

series_dropdown = driver.find_element(By.ID, 'seriesDropDown')
for option in series_dropdown.find_elements(By.TAG_NAME, 'option'):
    if option.text == series:
        option.click()
        break

# If you have more than one panel, this might not work
# Contact me on billy.rebecchi@googlemail.com and I will help out
panel_dropdown = driver.find_element(By.ID, 'panelDropDown')
panel_dropdown.find_element(By.TAG_NAME, 'option').click()

unit_dropdown = driver.find_element(By.ID, 'unitComponentDropDown')
unit_dropdown.find_element(By.TAG_NAME, 'option').click()

driver.find_element(By.CLASS_NAME, 'actionBtn').click()

driver.find_element(By.LINK_TEXT, centre_number).click()

candidates = []
cells = driver.find_elements(By.TAG_NAME, 'td')
for i in range(1, len(cells), 4):
    candidates.append(cells[i].text)

for candidate in candidates:
    print(f"Fetching work for Candidate: {candidate}")
    try:
        driver.find_element(By.LINK_TEXT, candidate).click()

        driver.find_element('xpath', '//input[@value="allSelectRadioButton"]').click()
        driver.find_element('xpath', '//input[@value="Download"]').click()
    except:
        print("Couldn't fetch candidate. Download manually later.")

    driver.back()

input("Press any key to continue (once downloads have all finished)...")

i = 0
for item in os.listdir(download_directory):
    if item.endswith('.zip'):
        folder_name = download_directory + f'/{item}'

        filename_components = item.replace(".zip","").split("_")
        candidate = filename_components[len(filename_components)-1]

        zip_ref = zipfile.ZipFile(folder_name)
        candidate_directory = download_directory + f'/{candidate}'

        zip_ref.extractall(candidate_directory)
        zip_ref.close()

        os.remove(folder_name)

        for item in os.listdir(candidate_directory):
            if item.endswith('.zip'):
                folder_name = candidate_directory + f'/{item}'
                zip_ref = zipfile.ZipFile(folder_name)
                zip_ref.extractall(candidate_directory)
                zip_ref.close()
                os.remove(folder_name)

        i += 1