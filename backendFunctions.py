from selenium import webdriver 
import pandas as pd
import backendFunctions as bf
from pynput.keyboard import Key,Controller
from time import sleep

def readDataToDictionary(driver,websiteUrl):
    '''
    Holds the implementation for reading in the data from the website and creating a dictionary out of it
    that contains a list of the attributes passed on to it.

    INPUTS:
    *driver - the driver that is being used
    *websiteUrl - the Trading View Website. If the website changes, every implementation used below will 
    most likely have to change as well.
    *attributeList - For the attribute/column list, the name of the attribute can be changed on the list, 
    but the order in which each attribute is in MUST BE KEPT THE SAME

    OUTPUTS:
    *d - a dictionary containing the information for each attribute in attributeList
    '''
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

def signInUser(driver,websiteUrl,USERNAME,PASSWORD):
    '''
    Signs in the user based on the username and password given
    '''
    driver.get(websiteUrl) #load site
    keyboard = Controller() #make keyboard
    WAIT_TIME = 2 #default wait time for pages to load in seconds

    signInButton = driver.find_element_by_class_name("tv-header__link.tv-header__link--signin.js-header__signin")
    signInButton.click() #click sign in button
    
    sleep(WAIT_TIME)
    keyboard.type(USERNAME)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    keyboard.type(PASSWORD) #wait for sign in screen to load and type in username and password

    sleep(2*WAIT_TIME)
    logInBox = driver.find_element_by_class_name("tv-button.tv-button--no-border-radius.tv-button--size_large.tv-button--primary_ghost.tv-button--loader")
    logInBox.click()
    return None
