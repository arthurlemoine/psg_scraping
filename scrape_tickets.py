##### TO DO #####
# Implement selenium explicit wait
# Extract category number
# Add date for the data




from cgitb import text
import time
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import csv 

t = 3

driver = webdriver.Chrome(ChromeDriverManager().install()) #always re-install chromedriver because I couldn't make it work with a specified path
html_page = driver.get("https://billetterie.psg.fr/fr/second/match-foot-masculin-paris-vs-nice/")

#Accept cookies
cookie = driver.find_element("xpath", '//*[@id="didomi-notice-agree-button"]')
cookie.click()
time.sleep(t)

#Close pop-up
fast_popup = driver.find_element("xpath", '//div[@class="stack:32px psgTicketplaceFastest wrapper:450px fs:14px ta:center"]//descendant::button')
fast_popup.click()
time.sleep(t)

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
    booking_cats_buttons[i].click()  # opening category 
    time.sleep(t)
    cat_number = i # not the real number, needs to be implemented

    # Loop to get the access buttons specific to this category
    for j, access_button in enumerate(booking_accesses):
        if access_button.aria_role != 'none':
            cat_accesses.append(access_button)

    # Loop on accesses
    for access in cat_accesses:
        access.click()
        time.sleep(t)
        # Loop on tickets
        rangs = driver.find_elements("xpath", '//button[@class="flex ai:center py:10px w:100% fw:700 bookingResaleToggle dropdownArrows relative cardBoxMinimalContent"]//descendant::span[3]')
        quantities = driver.find_elements("xpath", '//button[@class="flex ai:center py:10px w:100% fw:700 bookingResaleToggle dropdownArrows relative cardBoxMinimalContent"]//descendant::span[6]')
        prices = driver.find_elements("xpath", '//button[@class="flex ai:center py:10px w:100% fw:700 bookingResaleToggle dropdownArrows relative cardBoxMinimalContent"]//descendant::span[9]')

        for k in range(len(rangs)):
            try:    # the exception doesn't seem to pick up the error from selenium
                Tickets.append([cat_number, rangs[k].text, quantities[k].text, prices[k].text])
            except :
                print("invalid ticket")

        return_button = driver.find_element("xpath", '//div[@class="flex bookingToolbar"]//descendant::button')
        return_button.click()
        time.sleep(t)
        booking_cats_buttons[i].click()  # reopening category to get the next access
        time.sleep(t)

    booking_cats_buttons[i].click()  # closing category 
    time.sleep(t)

# creating the csv

fields = ['Cat', 'Rank', 'Quant', 'Price'] 
rows = Tickets
    
filename = "tickets_20_09.csv"
    
# writing to csv file 
with open(filename, 'w', encoding="utf-8") as csvfile: 
    csvwriter = csv.writer(csvfile)  
    csvwriter.writerow(fields) 
    csvwriter.writerows(rows)

print("done")