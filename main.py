import os, zipfile, configparser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

config = configparser.ConfigParser()
config.read('env.ini')

assessor_id = config.get('credentials', 'assessor_id')
username = config.get('credentials', 'username')
password = config.get('credentials', 'password')

series = config.get('repository', 'series')
centre_number = config.get('repository', 'centre')

download_directory = config.get('local', 'download_directory') + centre_number
if not os.path.exists(download_directory):
   os.makedirs(download_directory)

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : download_directory}
chrome_options.add_experimental_option('prefs', prefs)

driver_path = config.get('local', 'driver')
chrome_driver_service = Service(driver_path)
driver = webdriver.Chrome(service=chrome_driver_service, options=chrome_options)
driver.set_page_load_timeout(1800)

driver.get('https://repository.ocr.org.uk/CentresOverview.aspx')

driver.find_element(By.CLASS_NAME, 'LoginId').send_keys(assessor_id)
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
    if cells[i].text == "": continue
    candidates.append(cells[i].text)

for i, candidate in enumerate(candidates):
    print(f"Fetching work for Candidate: {candidate} ({i+1}/{len(candidates)})")
    
    driver.find_element(By.LINK_TEXT, candidate).click()

    driver.find_element('xpath', '//input[@value="allSelectRadioButton"]').click()
    driver.find_element('xpath', '//input[@value="Download"]').click()

    driver.back()

input("Press any key to continue (once downloads have all finished)...")

for i, item in enumerate(os.listdir(download_directory)):
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