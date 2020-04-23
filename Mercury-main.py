###############################################################################################
###                                      PROJECT MERCURY                                    ###
###                                                                                         ###
### @author Piero Orderique                                                                 ###
###############################################################################################

from selenium import webdriver 
import pandas as pd
import backendFunctions as bf
from time import sleep

CHROME_DRIVER_PATH = "C:\\Users\\fabri\\miniconda3\\Lib\\site-packages\\selenium\\webdriver\\chrome\\chromedriver.exe"
TRADING_VIEW_MAIN_URL = "https://www.tradingview.com/"
YAHOO_FINANCE_URL = "https://finance.yahoo.com/"
driver = webdriver.Chrome(CHROME_DRIVER_PATH) #main driver

#USER INPUT
usersWebsite = YAHOO_FINANCE_URL
username = "jakeowens107@gmail.com"
password = "Swimming1!"

if bf.user_signed_in(driver,usersWebsite,username,password):
    print("-----------------------------------------------------\nCollecting Data...")
else:
    print("Sign in Error: Check internet connection and speed.")

#TODO Have the names of the stocks that users written on a file so that it is stored and read from there 
        #Have loaded stocks displayed and ask if they want to remove/add stocks to their list

# d = bf.readDataToDictionary(CHROME_DRIVER_PATH,TRADING_VIEW_STOCKS_URL)
# #let's put the market data into a pandas dataframe
# df = pd.DataFrame(d)
# pd.set_option("display.max_rows", None, "display.max_columns", None)
# print(df)  #or can save to csv file 