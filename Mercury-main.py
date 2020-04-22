###############################################################################################
###                                      PROJECT MERCURY                                    ###
###                                                                                         ###
### @author Piero Orderique                                                                 ###
###############################################################################################

from selenium import webdriver 
import pandas as pd
import backendFunctions as bf

CHROME_DRIVER_PATH = "C:\\Users\\fabri\\miniconda3\\Lib\\site-packages\\selenium\\webdriver\\chrome\\chromedriver.exe"
TRADING_VIEW_URL = "https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap/"

d = bf.readDataToDictionary(CHROME_DRIVER_PATH,TRADING_VIEW_URL)

#let's put the market data into a pandas dataframe
df = pd.DataFrame(d)
pd.set_option("display.max_rows", None, "display.max_columns", None)
print(df)  #or can save to csv file 