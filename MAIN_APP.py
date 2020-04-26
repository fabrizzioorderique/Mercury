###############################################################################################
###                                   PROJECT MERCURY GUI                                   ###
###                                                                                         ###
### @author Piero Orderique                                                                 ###
###############################################################################################

import pandas as pd
from tkinter import Tk, Label, Entry, PhotoImage, Button, filedialog, messagebox, scrolledtext, INSERT
from tkinter.ttk import Progressbar, Combobox

YAHOO_FINANCE_URL = "https://finance.yahoo.com/"

#USER INPUT
usersWebsite = YAHOO_FINANCE_URL
username = "jakeowens107@gmail.com"
password = "Swimming1!"
filePath = ""
#portfolio = "Primary"

print("WHATTTTTT")
#import backendFunctions as bf # import when ready to call funcitons!

#################   MAIN GUI    ##################
DARK_BLUE = '#09173b'
BRIGHT_ORANGE = '#d69704'

def startSignInPage():
    #window
    signInWindow = Tk()
    signInWindow.title('Mercury Sign In Page')
    signInWindow.geometry('600x350')
    signInWindow.config(bg=DARK_BLUE)
    #window Label
    titleLabel = Label(signInWindow, text="Project Mercury", font=("Times New Roman Bold", 30),bg=DARK_BLUE,fg='white') #create object
    titleLabel.grid(column=0, row=0, padx=13,pady=10) #set it's position

    #logo
    mercuryLogo = PhotoImage(file = "C:\\Users\\fabri\\OneDrive\\Documents\\web-bot\\mercuryLogo.png")
    logoLbl = Label(image=mercuryLogo)
    logoLbl.place(relx=0.1, rely=0.2)

    #username
    usrnmeLbl = Label(signInWindow,text="Username:",font=("Arial Bold",13),bg=BRIGHT_ORANGE)
    usrnmeLbl.place(relx = 0.55,rely = 0.26) 
    usrnmeText = Entry(signInWindow,width=30)
    usrnmeText.insert(9,username) #DELETE THIS when multiple accounts are supported 
    usrnmeText.place(relx = 0.55, rely = 0.36)  
    usrnmeText.focus()
    #password
    passwordLbl = Label(signInWindow,text="Password:",font=("Arial Bold",13),bg=BRIGHT_ORANGE)
    passwordLbl.place(relx = 0.55,rely = 0.56) #grid(column=0,row=1,pady=30)
    passwordText = Entry(signInWindow,width=30)
    passwordText.insert(9,password)
    passwordText.place(relx = 0.55, rely = 0.66) 

    #sign in button
    def signIn():
        signInWindow.destroy()
        directoryPage()
    signInButton = Button(signInWindow,text="Sign In",font=("Arial Bold",13),command = signIn,bg='light blue')
    signInButton.place(relx = 0.55, rely = 0.87)

    #END
    signInWindow.mainloop()

def directoryPage():
    #window
    directoryPage = Tk()
    directoryPage.title('Select Directory Page')
    directoryPage.geometry('440x50')
    #window Label
    instructions = "Select a Directory to Store Data:"
    titleLabel = Label(directoryPage, text=instructions, font=("Times New Roman", 14),bg='white',fg='black') #create object
    titleLabel.grid(column = 0, row=0, padx=3,pady=5) #place(relx=0.09,rely=0.2) 
    #path selector button
    def chooseDir():
        global filePath
        filePath = filedialog.askdirectory()
        filePath += "/myPortfolio.csv"
        dirButton.destroy()
        titleLabel.config(font=("Times New Roman",9),text="Market Data will be stored in\n"+filePath)
        def nextButton():
            directoryPage.destroy()
            loadDataPage()
        nextButton = Button(directoryPage,text="Next >",font=("Arial",9),command=nextButton)
        nextButton.grid(column=1,row=0,padx=10,pady=5)
    dirButton = Button(directoryPage,text="Choose Directory",font=("Arial",9),command=chooseDir)
    dirButton.grid(column=1,row=0,padx=10,pady=5)

def loadDataPage():
    #window
    loadingPage = Tk()
    loadingPage.title('Data Collection Page')
    loadingPage.geometry('385x105')
    loadingPage.config(bg=DARK_BLUE)
    #window label
    titleLabel = Label(loadingPage, text="Loading Data...", font=("Times New Roman Bold", 14),bg=BRIGHT_ORANGE,fg='black') #create object
    titleLabel.grid(column = 0, row=0, padx=12,pady=10)
    #progress bar
    loadingBar = Progressbar(loadingPage, length=300)
    loadingBar.grid(column=0,row=1,padx=12,pady=10)
    def bar():
        from time import sleep
        global filePath
        loadingBar['value']=20
        sleep(1)
        loadingBar['value']=50
        import backendFunctions as bf
        if bf.user_signed_in(usersWebsite,username,password):
            sleep(1)
            loadingBar['value']=80
            dict_main = bf.readDataToDictionary()           
            sleep(1)
            loadingBar['value']=100
            sleep(1)
            #makes and saves df
            if len(dict_main) != 0:
                df_main = pd.DataFrame(dict_main)
                #pre analysis setup:
                for attribute in df_main.columns:
                    if attribute not in ['Ticker','Company Name']:
                        df_main[attribute] = df_main[attribute].str.replace(',','').str.replace("M",'').str.replace("%",'').str.replace('+','').astype(float)
                df_main.to_csv(filePath)
                pd.set_option("display.max_rows", None, "display.max_columns", None)
                print(df_main)
                loadingPage.destroy()
                portfolioPage(df_main)
            else:
                loadingPage.destroy()
                messagebox.askretrycancel("Data Loading Error.")
        else:
            loadingPage.destroy()
            messagebox.askretrycancel("Sign in Error","Data Collection Failed.")
    bar()

def portfolioPage(df):
    #window
    portfolioWindow = Tk()
    portfolioWindow.title('Portfolio Page')
    portfolioWindow.geometry('600x350')
    portfolioWindow.config(bg='light blue')

    #labels
    lbl1 = Label(text="Select a chart:", font=("Times New Roman",12),bg=BRIGHT_ORANGE)
    lbl2 = Label(text="My Stocks Portfolio", font=("Times New Roman",12),bg=BRIGHT_ORANGE)
    lbl1.place(relx=0.05,rely=0.01)
    lbl2.place(relx=0.65,rely=0.01)

    #show stocks list
    portfolio_display_df = df[['Ticker','Last Price']]
    scroll = scrolledtext.ScrolledText(portfolioWindow,width=22,height=19)
    scroll.place(relx=0.65,rely=0.1)
    scroll.insert(INSERT,portfolio_display_df.to_string())
    scroll.config(state='disabled')

    #choose/display chart
    comboValues = ['Select a Chart','Stocks by Price','Stocks by Total Equity']
    combo = Combobox(portfolioWindow,values=comboValues,state="readonly")
    combo.place(relx=0.05,rely=0.1)
    combo.current(0)
    def comboFunc(event):
        import matplotlib.pyplot as plt
        from time import sleep
        selection = combo.get()
        if selection == 'Stocks by Price':
            df.plot(kind='bar',x='Ticker',y='Last Price')
        elif selection == 'Stocks by Total Equity':
            df.plot(kind='bar',x='Ticker',y='Total Equity')
        portfolioWindow.destroy()
        sleep(1)
        plt.show()
        sleep(1)
        portfolioPage(df)
        print("plotted.")

    combo.bind("<<ComboboxSelected>>", comboFunc)
    portfolioWindow.mainloop()
 
# startSignInPage()
portfolioPage(pd.read_csv("C:/Users/fabri/OneDrive/Documents/DasText/csvFiles/myPortfolio.csv"))

#TODO Have the names of the stocks that users written on a file so that it is stored and read from there 
        #Have loaded stocks displayed and ask if they want to remove/add stocks to their list