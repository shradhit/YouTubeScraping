import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chrome_path = "/Users/shradhitsubudhi/.wdm/drivers/chromedriver/80.0.3987.106/mac64/chromedriver"
page_url = "https://www.youtube.com/watch?v=ioxWuCd-mn0" 


driver = webdriver.Chrome(executable_path=chrome_path)
driver.get(page_url)
time.sleep(2)  


title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
print(title)


SCROLL_PAUSE_TIME = 2
CYCLES = 100

html = driver.find_element_by_tag_name('html')
html.send_keys(Keys.PAGE_DOWN)  
html.send_keys(Keys.PAGE_DOWN)  
time.sleep(SCROLL_PAUSE_TIME * 3)

for i in range(CYCLES):
    html.send_keys(Keys.END)
    time.sleep(SCROLL_PAUSE_TIME)


comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
all_comments = [elem.text for elem in comment_elems]
print(all_comments)

replies_elems =driver.find_elements_by_xpath('//*[@id="replies"]')
all_replies = [elem.text for elem in replies_elems]
print(all_replies)

write_file = "output_replies.csv"
with open(write_file, "w") as output:
    for line in all_replies:
        output.write(line + '\n')
