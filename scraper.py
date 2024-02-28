from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import pandas as pd
import time
import os
import math

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
#Put your link here
mainlink = 'https://njmovers.com/search-for-a-mover/'
driver.get(mainlink)
driver.implicitly_wait(10)
country_list = []

try:
    x = driver.find_element(By.XPATH, "//select[contains(@class,'njmovers_select_county')]")
    y = x.find_elements(By.XPATH, "//option")
    for i in range(len(y)-1):
        country_list.append(y[i+1].text)
except:
    print("Somethin wrong. Code didn't work")


columns = [
    'Company Name', 'Address', 'NJIC#', 'Website', 'Email', 'Phone', 'Street Address' 'City', 'Country', 'State', 'Zip'
]
output_file = 'output.csv' #output file name and directory

# Check if the output file already exists
if not os.path.isfile(output_file):
    empty_df = pd.DataFrame(columns=columns)
    empty_df.to_csv(output_file, index=False)

columnsM = ['Country']
missing_file = 'missing_links.csv'
if not os.path.isfile(missing_file):
    _df = pd.DataFrame(columns=columnsM)
    _df.to_csv(missing_file, index=False)

print(country_list)
print(len(country_list))

for c in range(len(country_list)):
    con = country_list[c]
    # try:
    df1 = pd.read_csv(output_file) 
    if con in df1['Country'].values:
        continue
    else:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(mainlink)
        driver.implicitly_wait(10)
        # Find the dropdown element by its class name
        dropdown_element = driver.find_element(By.XPATH, "//select[contains(@class,'njmovers_select_county')]")
        # Create a Select object from the dropdown element
        dropdown = Select(dropdown_element)
        # Select 'Sussex' by its name
        dropdown.select_by_visible_text(con)
        driver.implicitly_wait(10)
        
        x = driver.find_elements(By.XPATH, "//div[@class='njmovers_dt_sec']/div[@class='njmovers_mover']")
        for i in range(len(x)):
            try:
                comName = x[i].find_element(By.XPATH, f"(//h4[@class = 'njmovers_name'])[{i+1}]").text
            except NoSuchElementException:
                comName = ""
            
            try:
                add = x[i].find_element(By.XPATH, f"(//p[@class = 'njmovers_address'])[{i+1}]").text
                if len(add.split(', ')) == 5:
                    street_address = add.split(', ')[0]
                    city = add.split(',')[1]
                    state = add.split(',')[3].replace(' ', '')
                    zip = add.split(',')[4].replace(' ', '')
                elif len(add.split(', ')) == 4:
                    street_address = add.split(', ')[0]
                    city = add.split(', ')[1]
                    state_zip = add.split(', ')[3].split(' ')
                    state = state_zip[0]
                    zip = state_zip[1]
            except NoSuchElementException:
                add = ""
                
            try:
                njic = x[i].find_element(By.XPATH, f"(//div[@class = 'njmovers_license_no']//p)[{i+1}]").text
            except NoSuchElementException:
                njic = ""
                
            try:
                web = x[i].find_element(By.XPATH, f"(//p[@class = 'njmovers_web'])[{i+1}]").text
            except NoSuchElementException:
                web = ""
                
            try:
                email = x[i].find_element(By.XPATH, f"(//p[@class = 'njmovers_mail'])[{i+1}]").text
            except NoSuchElementException:
                email = ""
                
            try:
                phone = x[i].find_element(By.XPATH, f"(//p[@class = 'njmovers_phone'])[{i+1}]").text
            except NoSuchElementException:
                phone = ""
                
            data = {
                'Company Name': comName,
                'Address': add,
                'NJIC#': njic,
                'Website': web,
                'Email': email,
                'Phone': phone,
                'Street Address': street_address,
                'City': city,
                'Country': con,
                'State': state,
                'Zip': zip
                }
            data_list = [data]
            existing_data = pd.read_csv(output_file) 
            new_data_df = pd.DataFrame(data_list, columns=columns)
            updated_data = existing_data._append(new_data_df, ignore_index=True)
            updated_data.to_csv(output_file, index=False)
            time.sleep(1)
            
        driver.quit()

    # except:
    #     data = {
    #         'Country': con,
    #     }
    #     data_list = [data]
    #     existing_data = pd.read_csv(missing_file) 
    #     new_data_df = pd.DataFrame(data_list, columns=columnsM)
    #     updated_data = existing_data._append(new_data_df, ignore_index=True)
    #     updated_data.to_csv(missing_file, index=False)
            

