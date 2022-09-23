from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import date
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

x = 1
y = 1
expert = 2
summary = 2
TOPICXPATH = "/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div/div/div[2]/ul[2]/li[" +str(x) +"]/ul/li[" + str(y) + "]/a"
TOPICTITLE = "/html/body/div[1]/div/div[2]/div/div[2]/h1"
# EXPERTNAME = "/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div/div[" + expert + "]/div/div/div[2]/h3/a"
# EMAIL = "/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div/div[" + expert + "]/div/div/div[3]/div[1]/a"
# PHONE = "/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div/div[" + expert + "]/div/div/div[3]/div[2]"
# ASSOCIATIONS = "/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div/div[" + expert + "]/div/div/div[2]/h5"
SUMMARYSENTENCE = "/html/body/div[1]/div/div[2]/div/div[4]/div[1]/div[1]/div/div[2]/div/article/div/div[1]/div/div/p[1]"
# SUMMARY = "/html/body/div[1]/div/div[2]/div/div[4]/div[1]/div[1]/div/div[2]/div/article/div/div[1]/div/div/p[" + summary +"]"
SUMMARYDIV = "/html/body/div[1]/div/div[2]/div/div[4]/div[1]/div[1]/div/div[2]/div/article/div/div[1]/div/div"

df = pd.DataFrame(columns=['name', 'topic_category', 'email', 'phone', 'association1', 'association2', 'association3', 'association4', 'association5', 'association6',\
  'association7', 'summary_sentence', 'summary'])

today = date.today()
os.makedirs("C:/ExpertsData/{}_SEARCH".format(today.strftime("%Y%b%d")), exist_ok=True) 

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://newsroom.asu.edu/experts")
driver.maximize_window()
time.sleep(2)


def checkExistsByXpath(xpath):
  time.sleep(1)
  try:
    driver.find_element(By.XPATH, xpath)
  except NoSuchElementException:
    return False
  return True
  
def getTextFromElement(xpath):
  text = None
  try:
    text = driver.find_element(By.XPATH, xpath).text
  except Exception as e:
    print(e)
  return text

def processExperts():
  flag = 1
  tflag = 1
  i = 1
  j = 1
  parentCategory = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div/div/div[2]/ul[2]")
  categoryCount = len(parentCategory.find_elements_by_xpath("./li"))
  print("++++++")
  print(categoryCount)
  print("++++++")
  for i in range(1, categoryCount+1):
      flag = flag + 1
      if flag == 3:
        break     
      TOPICXPATH = "/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div/div/div[2]/ul[2]/li[" +str(i) +"]/ul"
      parentTopic = driver.find_element(By.XPATH, TOPICXPATH)
      topicCount = len(parentTopic.find_elements_by_xpath("./li"))
      print("++++++")
      print(topicCount)
      print("++++++")
      for j in range(1 , topicCount+1):
        TOPICXPATH = "/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div/div/div[2]/ul[2]/li[" +str(i) +"]/ul/li[" + str(j) + "]/a"   
        topic = ""
        if checkExistsByXpath("/html/body/div[3]/div/div/section[3]/button[2]"):
            driver.find_element(By.XPATH, "/html/body/div[3]/div/div/section[3]/button[2]").click()
        if not checkExistsByXpath(TOPICXPATH):
            if tflag == 1:
              tflag = 0
            else:
              break
        else: 
            driver.find_element(By.XPATH, TOPICXPATH).click()
            topic = getTextFromElement(TOPICTITLE)
            parentDIVExpertNames = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div")
            countOfDivs = len(parentDIVExpertNames.find_elements_by_xpath("./div"))
            print("++++++")
            print(countOfDivs)
            print("++++++")
            for k in range(2, countOfDivs+1):
                name = ""
                email = ""
                phone = ""
                associations = ""
                summarySentence = ""
                summary = ""
                time.sleep(1)
                if checkExistsByXpath("/html/body/div[3]/div/div/section[3]/button[2]"):
                    driver.find_element(By.XPATH, "/html/body/div[3]/div/div/section[3]/button[2]").click()   
                EXPERTNAME = "/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div/div[" + str(k) + "]/div/div/div[2]/h3/a"
                EMAIL = "/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div/div[" + str(k) + "]/div/div/div[3]/div[1]/a"
                PHONE = "/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div/div[" + str(k) + "]/div/div/div[3]/div[2]"
                ASSOCIATIONS = "/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div/div[" + str(k) + "]/div/div/div[2]/h5"
                if checkExistsByXpath(EXPERTNAME):
                    name = getTextFromElement(EXPERTNAME)
                if checkExistsByXpath(EMAIL):
                    email = getTextFromElement(EMAIL)
                if checkExistsByXpath(PHONE):
                    phone = getTextFromElement(PHONE)
                if checkExistsByXpath(ASSOCIATIONS):
                    associations = getTextFromElement(ASSOCIATIONS)
                if checkExistsByXpath(EXPERTNAME):
                    driver.find_element(By.XPATH, EXPERTNAME).click()
                    if checkExistsByXpath(SUMMARYDIV):
                        summary = getTextFromElement(SUMMARYDIV)
                        if checkExistsByXpath("//p[contains(@class, 'lead')]"):
                            summarySentence =  driver.find_element(By.XPATH, "//p[contains(@class, 'lead')]").text
                        elif checkExistsByXpath("//span[contains(@class, 'lead')]"):
                            summarySentence =  driver.find_element(By.XPATH, "//span[contains(@class, 'lead')]").text
                associations = associations.split(",")
                for x in range(7 - len(associations)):
                    associations.append(" ")
                l = [name, topic, email, phone] + associations + [summarySentence, summary]
                print(l)
                df.loc[len(df.index)] = l
                driver.back()
            driver.back()
              


processExperts()
df.to_csv("C:/ExpertsData/{}_SEARCH/{}.csv".format(today.strftime("%Y%b%d"), today.strftime("%Y%b%d")))                  
              
          
          
      
  