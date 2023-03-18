from time import time
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

# URl
start_url = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
browser = webdriver.Chrome("C://Users//vrite//Downloads//edgedriver_win64//msedgedriver.exe")
browser.get(start_url)
time.sleep(10)

headers = ["starName", "mass", "distance", "radius"]
planetsData = []
newPlanetData = []

# Creating a scrap function
def scrap() :
    for i in range (0, 201) :
        soup = BeautifulSoup(browser.page_source,"html.parser")
        for ul_tag in soup.find_all("tr", attrs = {"class" : "new"}):
            li_tags = ul_tag.find_all("tr")
            temp_list = []
            for index, li_tag in enumerate(li_tags) :
                if index == 0 :
                    temp_list.append(li_tag.find_all("td")[0].contents[0])
                else :
                    try :
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_liTag = li_tag[0]
            temp_list.append("https://en.wikipedia.org/wiki/Pegasus_(constellation)" + hyperlink_liTag.find_all("a", href = True)[0]["href"])
            planetsData.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    
def scrapMoreData(Hyperlink) :
    try :
        page = requests.get(Hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        for tr_tag in soup.find_all("tr", attrs = {"class" : "fact_row"}) :
            td_tags = tr_tag.find_all("td")
            temp_list = []
            for td_tag in td_tags :
                try :
                    temp_list.append(td_tag.find_all("div", attrs = {"class" : "new"})[0].contents[0])
                except :
                    temp_list.append("")
        newPlanetData.append(temp_list)
        
    except :
        time.sleep(1)
        scrapMoreData(Hyperlink)
    
scrap()

for index, data in enumerate (planetsData) :
    scrapMoreData(data[5])

finalPlanetData = []

for index, data in enumerate (planetsData) :
    newPlanetDataElement = newPlanetData[index]
    newPlanetDataElement = [elem.replace("\n", "") for elem in newPlanetDataElement]
    newPlanetDataElement = newPlanetDataElement[0:5]
    finalPlanetData.append(newPlanetDataElement)

# Storing in csv file
with open("Planets.csv", "W")as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(finalPlanetData)