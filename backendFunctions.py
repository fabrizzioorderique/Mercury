from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from pynput.keyboard import Key,Controller
from time import sleep

WAIT_TIME = 3 #default wait time for pages to load in seconds

def user_signed_in(driver,websiteUrl,USERNAME,PASSWORD):
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

def readDataToDictionary(driver):
    '''
    Holds the implementation for reading in the data from the website and creating a dictionary out of it
    that contains a list of the attributes passed on to it.

    INPUTS:
    *driver - the driver that is being used
    *websiteUrl - yahoo finance website
    *attributeList - For the attribute/column list, the name of the attribute can be changed on the list, 
    but the order in which each attribute is in MUST BE KEPT THE SAME

    OUTPUTS:
    *d - a dictionary containing the information for each attribute in attributeList
    '''
    ##Implemenation only for YAHOO FINANCE. To add other website, web url as input for checking
    ##Furthermore, this version only supports a single portfolio named "Primary" - simply add 
    # neccesary parameter and if statements for addtional portfolio watchlists
    d = {}

    watchListButton = WebDriverWait(driver,10*WAIT_TIME).until(lambda x: x.find_element_by_xpath("""//*[@id="data-util-col"]/section[1]/header/a"""))
    watchListButton.click()
    print("Watch List Button Clicked.")

    primaryButton = WebDriverWait(driver,10*WAIT_TIME).until(lambda x: x.find_element_by_xpath('//*[@id="Lead-3-Portfolios-Proxy"]/main/div[2]/section/ul/li[7]'))
    primaryButton.click()

    #potential problem: Prices are changing as we collect data. perhaps lets try freezing the panel first?
    settingsButton = WebDriverWait(driver,10*WAIT_TIME).until(lambda x: x.find_element_by_xpath('//*[@id="Lead-3-Portfolios-Proxy"]/main/header/div[2]/div[2]/div[2]/div'))
    settingsButton.click()
    streamingButton = WebDriverWait(driver,10*WAIT_TIME).until(lambda x: x.find_element_by_xpath('//*[@id="dropdown-menu"]/ul/li[3]/button'))
    streamingButton.click()

    totalInvested = WebDriverWait(driver,10*WAIT_TIME).until(lambda x: x.find_element_by_xpath("""//*[@id="Lead-3-Portfolios-Proxy"]/main/div[1]/div[1]/div/div[1]/span""")).text
    print("\n",totalInvested)
    
    attributeNames = ["Ticker","Company Name","Last Price","Change","%Change","Shares","Cost/Share","Total Equity","Total Change","Total %Change","Div/Share","1yr Est","Volume"]
    attributeLists = []
    for att in attributeNames:
        attributeLists.append([]) #appends and empty list for every attribute 

    idx = 1
    while True:
        try:
            attributeLists[0].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[1]/a').text) #ticker
            sleep(WAIT_TIME*0.001)
            attributeLists[1].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[2]').text) #name
            # sleep(WAIT_TIME*0.001)
            # attributeLists[2].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[3]/span').text) #lastprice
            # sleep(WAIT_TIME*0.001)
            # attributeLists[3].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[4]/span').text) #change
            # sleep(WAIT_TIME*0.001)
            # attributeLists[4].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[5]/span').text) #%change
            # #attributeLists[5].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[6]/span').text) #trade date
            # attributeLists[5].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[7]').text) #shares
            # attributeLists[6].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[8]').text) #cost/share
            # attributeLists[7].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[9]/span').text) #total equity
            # attributeLists[8].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[10]/span').text) #total change
            # attributeLists[10].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[11]/span').text) #total %change
            # attributeLists[11].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[12]').text) #Div/Share
            # #divPayDates.append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[13]').text) #div pay data
            # attributeLists[12].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[14]').text) #1 yr est
            # attributeLists[13].append(driver.find_element_by_xpath('//*[@id="pf-detail-table"]/div[1]/table/tbody/tr['+str(idx)+']/td[15]/span').text) #volume
        except:
            print("loop broken at index =",idx)
            break
        idx+=1
    for i in range(len(attributeNames)):
        print("\n",attributeNames[i],"\n",attributeLists[i]) #prints out list of every attribute

    return d
    # names = driver.find_elements_by_class_name("tv-screener__description") 
    # tickers = driver.find_elements_by_class_name("tv-screener__symbol.apply-common-tooltip") 
    # prices = []
    # for index, ticker in enumerate(tickers):
    #     xpathName = '//*[@id="js-screener-container"]/div[4]/table/tbody/tr['+str(index+1)+']/td[2]/span'
    #     prices.append(driver.find_element_by_xpath(xpathName))
    # #Makes the offical lists containing the text
    # tickerList = []
    # priceList = []
    # nameList = []
    # for ticker in tickers:
    #     tickerList.append(ticker.text)
    # for price in prices:
    #     priceList.append(price.text)
    # for name in names:
    #     nameList.append(name.text)

    # driver.close() #closes driver once done extracting data

    # #let's put the market data into a pandas dataframe
    # d = {'Company': nameList,'Ticker Symbol': tickerList,'Last Price': priceList}

#testing
# attributeNames = ["Ticker","Company Name","Last Price","Change","%Change","Date Bought","Shares","Cost/Share","Total Equity","Total Change","Total %Change","Div/Share","DivPayDate","1yr Est","Volume"]
# attributeLists = []

# tickers = attributeLists.append([]) 
# attributeLists[0].append("hey")
# attributeLists[0].append("hi")
# names = attributeLists.append([])

# lastPrices = []
# changes = []
# percentChanges = []
# tradeDates = []
# shares = []
# costPerShare = []
# totalEquities = []
# totalChanges = []
# totalPercentChanges = []
# divPerShare = []
# divPayDates = []
# oneYearEsts = []
# volumes = []
# print(attributeLists)