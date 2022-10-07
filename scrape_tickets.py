from cgitb import text
import time
import csv
from datetime import date
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.headless = False

today = date.today()

driver = webdriver.Chrome(ChromeDriverManager().install()) #always re-install chromedriver because I couldn't make it work with a specified path
driver = driver
html_page = driver.get("https://billetterie.psg.fr/fr/second/match-foot-masculin-paris-vs-marseille/")

#Accept cookies
cookie = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable(("xpath", '//*[@id="didomi-notice-agree-button"]'))
)
cookie.click()

#Close pop-up
fast_popup = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable(("xpath", '//div[@class="stack:32px psgTicketplaceFastest wrapper:450px fs:14px ta:center"]//descendant::button'))
)
fast_popup.click()

# nl_popup = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable(("xpath", '//a[@class="wp-optin-dialog-button wp-optin-dialog-negativeButton"]'))
# )
# nl_popup.click()
# time.sleep(1)

# Object fetching 
booking_cats = driver.find_elements("xpath", '//div[@class="cardBox relative cardBoxHover bookingCategory"]')
booking_cats_buttons = driver.find_elements("xpath", '//button[@class="relative flex ai:center jc:space-between p:12px w:100% fs:14px ta:left dropdownArrows bookingCategoryToggle"]')
booking_accesses = driver.find_elements("xpath", '//button[@class="flex ai:center w:100% ta:left"]')

# Loop on categories  
Tickets = []
# the loop sometimes breaks after a few categories 
# probably a specific access or ticket badly handled in a cat after the 2nd one
for i, booking_cat in enumerate(booking_cats):

    cat_accesses = []
    print(booking_cat.text)
    booking_cats_buttons[i] = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((booking_cats_buttons[i]))
        )
    booking_cats_buttons[i].click()  # opening category 
    cat_number = i # not the real number, needs to be implemented

    # Loop to get the access buttons specific to this category
    for j, access_button in enumerate(booking_accesses):
        if access_button.aria_role != 'none':
            cat_accesses.append(access_button)

    # Loop on accesses
    for access in cat_accesses:
        access = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((access))
        )
        access.click()
        # Loop on tickets
        access_name = driver.find_element("xpath", '//span[@class="block"]')
        cat_name = driver.find_element("xpath", '//b[@class="flex flexcolumn w:fit-content tt:capitalize bookingCategoryName"]')
        rangs = driver.find_elements("xpath", '//button[@class="flex ai:center py:10px w:100% fw:700 bookingResaleToggle dropdownArrows relative cardBoxMinimalContent"]//descendant::span[3]')
        quantities = driver.find_elements("xpath", '//button[@class="flex ai:center py:10px w:100% fw:700 bookingResaleToggle dropdownArrows relative cardBoxMinimalContent"]//descendant::span[6]')
        prices = driver.find_elements("xpath", '//button[@class="flex ai:center py:10px w:100% fw:700 bookingResaleToggle dropdownArrows relative cardBoxMinimalContent"]//descendant::span[9]')
        cat_name = cat_name.text
        access_name = access_name.text

        for k in range(len(rangs)):
            try:    # the exception doesn't seem to pick up the error from selenium
                Tickets.append([today, cat_number, cat_name, access_name, rangs[k].text, quantities[k].text, prices[k].text])
            except Exception as e:
                print("invalid ticket")
        time.sleep(1)        
        return_button = driver.find_element("xpath", '//button[@title="Retour"]')
        return_button.click()

        booking_cats_buttons[i] = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((booking_cats_buttons[i]))
        )
        booking_cats_buttons[i].click()  # reopening category to get the next access

    booking_cats_buttons[i] = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((booking_cats_buttons[i]))
        )
    booking_cats_buttons[i].click()  # closing category 


# creating the csv

fields = ['Date', 'Cat_index', 'Cat_name', 'Access', 'Rank', 'Quant', 'Price'] 
rows = Tickets
    
filename = "db_psg_price_" + str(today)
    
# writing to csv file 
with open(filename, 'w', encoding="utf-8") as csvfile: 
    csvwriter = csv.writer(csvfile)  
    csvwriter.writerow(fields) 
    csvwriter.writerows(rows)

print("done")