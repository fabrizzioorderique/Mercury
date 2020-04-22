from selenium import webdriver 
import pandas as pd
import backendFunctions as bf

def readDataToDictionary(driverPath, websiteUrl):
    '''
    Holds the implementation for reading in the data from the website and creating a dictionary out of it
    that contains a list of the attributes passed on to it.

    INPUTS:
    *driverPath - the file path in which directory the chrome driver is installed in
    *websiteUrl - the Trading View Website. If the website changes, every implementation used below will 
    most likely have to change as well.
    *attributeList - For the attribute/column list, the name of the attribute can be changed on the list, 
    but the order in which each attribute is in MUST BE KEPT THE SAME

    OUTPUTS:
    *d - a dictionary containing the information for each attribute in attributeList
    '''
    driver = webdriver.Chrome(driverPath)
    driver.get(websiteUrl)

    names = driver.find_elements_by_class_name("tv-screener__description") 
    tickers = driver.find_elements_by_class_name("tv-screener__symbol.apply-common-tooltip") 
    prices = []
    for index, ticker in enumerate(tickers):
        xpathName = '//*[@id="js-screener-container"]/div[4]/table/tbody/tr['+str(index+1)+']/td[2]/span'
        prices.append(driver.find_element_by_xpath(xpathName))
    #Makes the offical lists containing the text
    tickerList = []
    priceList = []
    nameList = []
    for ticker in tickers:
        tickerList.append(ticker.text)
    for price in prices:
        priceList.append(price.text)
    for name in names:
        nameList.append(name.text)

    driver.close() #closes driver once done extracting data

    #let's put the market data into a pandas dataframe
    d = {'Company': nameList,'Ticker Symbol': tickerList,'Last Price': priceList}
    return d