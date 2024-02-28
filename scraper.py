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

# driver = webdriver.Chrome()
#Put your link here
mainlink = 'https://njmovers.com/search-for-a-mover/'
# driver.get(mainlink)
# driver.implicitly_wait(10)

columns = [
    'Company Name', 'Address', 'NJIC#', 'Website', 'Email', 'Phone', 'City', 'Country', 'State', 'Zip'
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

file_path = 'country_list.csv' #input file name and directory #The list of links of the pages which you get from first script
df = pd.read_csv(file_path)

for c in range(len(df)):
    con = df.iloc[c, 0]
    try:
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
            
            x = driver.find_elements(By.XPATH, "(//div[contains(@class,'njmovers_mover')])")
            for i in range(len(x)-1):
                try:
                    comName = x[i+1].find_element(By.XPATH, f"(//h4[@class = 'njmovers_name'])[{i+1}]").text
                except NoSuchElementException:
                    comName = ""
                
                try:
                    add = x[i+1].find_element(By.XPATH, f"(//p[@class = 'njmovers_address'])[{i+1}]").text
                    if len(add.split(', ')) == 5:
                        city = add.split(',')[1]
                        state = add.split(',')[3].replace(' ', '')
                        zip = add.split(',')[4].replace(' ', '')
                    elif len(add.split(', ')) == 4:
                        city = add.split(', ')[1]
                        state_zip = add.split(', ')[3].split(' ')
                        state = state_zip[0]
                        zip = state_zip[1]
                except NoSuchElementException:
                    add = ""
                    
                try:
                    njic = x[i+1].find_element(By.XPATH, f"(//div[@class = 'njmovers_license_no']//p)[{i+1}]").text
                except NoSuchElementException:
                    njic = ""
                    
                try:
                    web = x[i+1].find_element(By.XPATH, f"(//p[@class = 'njmovers_web'])[{i+1}]").text
                except NoSuchElementException:
                    web = ""
                    
                try:
                    email = x[i+1].find_element(By.XPATH, f"(//p[@class = 'njmovers_mail'])[{i+1}]").text
                except NoSuchElementException:
                    email = ""
                    
                try:
                    phone = x[i+1].find_element(By.XPATH, f"(//p[@class = 'njmovers_phone'])[{i+1}]").text
                except NoSuchElementException:
                    phone = ""
                    
                data = {
                    'Company Name': comName,
                    'Address': add,
                    'NJIC#': njic,
                    'Website': web,
                    'Email': email,
                    'Phone': phone,
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

    except:
        data = {
            'Country': con,
        }
        data_list = [data]
        existing_data = pd.read_csv(missing_file) 
        new_data_df = pd.DataFrame(data_list, columns=columnsM)
        updated_data = existing_data._append(new_data_df, ignore_index=True)
        updated_data.to_csv(missing_file, index=False)
            

