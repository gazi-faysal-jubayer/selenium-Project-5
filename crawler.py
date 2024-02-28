from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import math
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import pandas as pd

driver = webdriver.Chrome()
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
# Close the WebDriver
driver.quit()

# Create a DataFrame from the list of links
df = pd.DataFrame(country_list, columns=['Country'])

# Save the DataFrame to a CSV file
df.to_csv('country_list.csv', index=False) #output file name and directory