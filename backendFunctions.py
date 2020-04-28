from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from pynput.keyboard import Key,Controller
from time import sleep

CHROME_DRIVER_PATH = "C:\\Users\\fabri\\miniconda3\\Lib\\site-packages\\selenium\\webdriver\\chrome\\chromedriver.exe"

WAIT_TIME = 3 #default wait time for pages to load in seconds
driver = webdriver.Chrome(CHROME_DRIVER_PATH) #main driver
totalInvested = "Data not collected."

def user_signed_in(websiteUrl,USERNAME,PASSWORD):
    '''
    Signs in the user based on the username and password given
    '''
    driver.get(websiteUrl) #load site
    keyboard = Controller() #make keyboard

    if websiteUrl == "https://finance.yahoo.com/":
        try:
            signInButton = driver.find_element_by_id("header-signin-link")
            signInButton.click()

            textArea = WebDriverWait(driver, 10*WAIT_TIME).until(lambda x: x.find_element_by_class_name("phone-no"))
            textArea.send_keys(USERNAME) #types in username as soon as element is found within 30 seconds
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            print("username entered.")

            textArea = WebDriverWait(driver, 10*WAIT_TIME).until(lambda x: x.find_element_by_id("login-passwd"))
            textArea.send_keys(PASSWORD) #types in username as soon as element is found within 30 seconds
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            print("password entered.")
        except:
            driver.close()
            return False
    #testing functionality with other websites
    elif(websiteUrl == "https://www.tradingview.com/"):
        signInButton = driver.find_element_by_class_name("tv-header__link.tv-header__link--signin.js-header__signin")
        signInButton.click() #click sign in button
        
        sleep(WAIT_TIME)
        keyboard.type(USERNAME)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        keyboard.type(PASSWORD) 
        keyboard.press(Key.enter)
        keyboard.release(Key.enter) #wait for sign in screen to load and type in username and password and hit enter
    else:
        return False #if website is not listed 
    return True

def readDataToDictionary():
    '''
    Holds the implementation for reading in the data from the website and creating a dictionary out of it
    '''
    ##Implemenation only for YAHOO FINANCE. To add other website, web url as input for checking
    ##Furthermore, this version only supports a single portfolio named "Primary" - simply add 
    # neccesary parameter and if statements for addtional portfolio watchlists
    d = {}
    try:
        watchListButton = WebDriverWait(driver,10*WAIT_TIME).until(lambda x: x.find_element_by_xpath("""//*[@id="data-util-col"]/section[1]/header/a"""))
        watchListButton.click()
        print("\nWatch List Button Clicked.")

        primaryButton = WebDriverWait(driver,10*WAIT_TIME).until(lambda x: x.find_element_by_xpath('//*[@id="Lead-3-Portfolios-Proxy"]/main/div[2]/section/ul/li[7]'))
        primaryButton.click()
        print("\nPrimary List Selected.")

        sleep(WAIT_TIME)
        settingsButton = WebDriverWait(driver,10*WAIT_TIME).until(lambda x: x.find_element_by_xpath('//*[@id="Lead-3-Portfolios-Proxy"]/main/header/div[2]/div/div[2]/div/span'))
        settingsButton.click()
        print("\nsettings Button found.")
        streamingButton = WebDriverWait(driver,10*WAIT_TIME).until(lambda x: x.find_element_by_xpath('//*[@id="dropdown-menu"]/ul/li[3]/button'))
        streamingButton.click()
        print("\nstreaming button found.")
    except:
        print("\nButtons were not found. Empty Dictionary Returned.")
        driver.close()
        return d

    global totalInvested
    totalInvested = WebDriverWait(driver,10*WAIT_TIME).until(lambda x: x.find_element_by_xpath("""//*[@id="Lead-3-Portfolios-Proxy"]/main/div[1]/div[1]/div/div[1]/span""")).text
    print("\n",totalInvested)
    
    attributeNames = ["Ticker","Company Name","Last Price","Change","%Change","Shares","Cost/Share","Total Equity","Total Change","Total %Change","1yr Est","Volume [M]"]
    attributeLists = []
    for att in attributeNames:
        attributeLists.append([]) #appends and empty list for every attribute 

    idx = 1
    while True:
        try:
            sleep(WAIT_TIME*0.001)
            attributeLists[0].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[1]/a').text) #ticker
            sleep(WAIT_TIME*0.001)
            attributeLists[1].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[2]').text) #name
            sleep(WAIT_TIME*0.001)
            attributeLists[2].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[3]/span').text) #lastprice
            sleep(WAIT_TIME*0.001)
            attributeLists[3].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[4]/span').text) #change
            sleep(WAIT_TIME*0.001)
            attributeLists[4].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[5]/span').text) #%change
            sleep(WAIT_TIME*0.001)
            attributeLists[5].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[7]').text) #shares
            sleep(WAIT_TIME*0.001)
            attributeLists[6].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[8]').text) #cost/share
            sleep(WAIT_TIME*0.001)
            attributeLists[7].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[9]/span').text) #total equity
            sleep(WAIT_TIME*0.001)
            attributeLists[8].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[10]/span').text) #total change
            sleep(WAIT_TIME*0.001)
            attributeLists[9].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[11]/span').text) #total %change
            sleep(WAIT_TIME*0.001)                 
            attributeLists[10].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[12]').text) #1 yr est
            sleep(WAIT_TIME*0.001)            
            attributeLists[11].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[13]/span').text) #volume
        except:
            print("loop broken at index =",idx)
            driver.close()
            break
        idx+=1
    for i in range(len(attributeNames)):
        d[attributeNames[i]] = attributeLists[i]
        print("\n",attributeNames[i],"\n",attributeLists[i]) #prints out list of every attribute

    return d

def getTotalInvested():
    return totalInvested