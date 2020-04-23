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
TRADING_VIEW_STOCKS_URL = "https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap/"
TRADING_VIEW_MAIN_URL = "https://www.tradingview.com/"
driver = webdriver.Chrome(CHROME_DRIVER_PATH) #main driver

#USER INPUT
username = "fabriorder"
password = "Swimming1!"

bf.signInUser(driver,TRADING_VIEW_MAIN_URL,username,password)

# d = bf.readDataToDictionary(CHROME_DRIVER_PATH,TRADING_VIEW_STOCKS_URL)
# #let's put the market data into a pandas dataframe
# df = pd.DataFrame(d)
# pd.set_option("display.max_rows", None, "display.max_columns", None)
# print(df)  #or can save to csv file 