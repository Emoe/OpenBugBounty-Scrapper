from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
import sys

def clean_URL(url):
    if url[0] == "*":
        return url[2:]
    else:
        return url

banner = """
  ______   .______    _______ .__   __. .______    __    __    _______ .______     ______    __    __  .__   __. .___________.____    ____ 
 /  __  \  |   _  \  |   ____||  \ |  | |   _  \  |  |  |  |  /  _____||   _  \   /  __  \  |  |  |  | |  \ |  | |           |\   \  /   / 
|  |  |  | |  |_)  | |  |__   |   \|  | |  |_)  | |  |  |  | |  |  __  |  |_)  | |  |  |  | |  |  |  | |   \|  | `---|  |----` \   \/   /  
|  |  |  | |   ___/  |   __|  |  . `  | |   _  <  |  |  |  | |  | |_ | |   _  <  |  |  |  | |  |  |  | |  . `  |     |  |       \_    _/   
|  `--'  | |  |      |  |____ |  |\   | |  |_)  | |  `--'  | |  |__| | |  |_)  | |  `--'  | |  `--'  | |  |\   |     |  |         |  |     
 \______/  | _|      |_______||__| \__| |______/   \______/   \______| |______/   \______/   \______/  |__| \__|     |__|         |__|     
                                                                                                                                           
     _______.  ______ .______          ___      .______   .______    _______ .______                                                       
    /       | /      ||   _  \        /   \     |   _  \  |   _  \  |   ____||   _  \                                                      
   |   (----`|  ,----'|  |_)  |      /  ^  \    |  |_)  | |  |_)  | |  |__   |  |_)  |                                                     
    \   \    |  |     |      /      /  /_\  \   |   ___/  |   ___/  |   __|  |      /                                                      
.----)   |   |  `----.|  |\  \----./  _____  \  |  |      |  |      |  |____ |  |\  \----.                                                 
|_______/     \______|| _| `._____/__/     \__\ | _|      | _|      |_______|| _| `._____|                                                 
                                                                                                                                           
                                                                                                                                        """
print(banner)

baseURL = "https://www.openbugbounty.org/bugbounty-list/page/{}/"
if len(sys.argv) < 2:
    print("Please provide the amount of Sites to scrape")
    print("Usage: python3 BugBountyList.py 40")
    sys.exit()
max_legth = int(sys.argv[1])

browser = webdriver.Firefox()

urls = []
domains = []
for i in range(1, max_legth+1):
    print("Dump Page - {}".format(str(i)))
    browser.get(baseURL.format(str(i)))

    table = browser.find_element(by=By.ID, value="bugbounty-list")
    elements = table.find_elements(by=By.TAG_NAME, value="a")
    for url in elements:
        urlText = url.get_attribute("href")
        if "/bugbounty/" in urlText: 
            urls.append(urlText)

for url in urls:
    browser.get(url)
    time.sleep(2)
    table = browser.find_element(by=By.CLASS_NAME, value="wishlist")
    elements = table.find_elements(by=By.TAG_NAME, value="td")
    for elem in elements:
        domains.append(clean_URL(elem.get_attribute("innerText")))
print("Scan Done")

browser.close()
output = open("OpenBugBountyURLS.txt", "w")
output2 = open("OpenBugBountyURLS.json", "w")
output2.write(json.dumps(domains))
for domain in domains:
    output.write(domain + "\r\n")
output2.close()
output.close()