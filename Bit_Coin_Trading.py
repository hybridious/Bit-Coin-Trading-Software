import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
#imports GUI Dev Enviroment V
import tkinter as tk
from tkinter import ttk
import urllib
import json
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)

style.use("ggplot")

f = Figure(figsize=(10,6), dpi=100)
a = f.add_subplot(111)

exchange = "BTC-e"
DatCounter = 9000
programName = "btce"

resampleSize = "15 Min"

DataPace = "1d"
candleWidth = 0.008

def changeTimeFrame(tf):
    global DataPace
    global DatCounter

    if tf == "7d" and resampleSize == "1Min":
        popupmsg("Too much data chosen, choose smaller timeframe")
    else:
        DataPace = tf
        DatCounter = 9000


def changeSampleSize(size,width):
    global resampleSize
    global DatCounter
    global candleWidth
    if DataPace == "7d" and resampleSize == "1Min":
        popupmsg("Too much data chosen, choose smaller timeframe")

    elif DataPace == "tick":
        popupmsg("You are currently viewing Tick data, not OHLC")

    else:
        resampleSize = size
        DatCounter = 9000
        candleWidth = width
    
        

def changeExchange(toWhat,pn):
    global exchange;
    global DatCounter;
    global programName;

    exchange = toWhat
    programName = pn
    DatCounter = 9000


def popupmsg(msg):
    popup=tk.Tk()

    def leavemini():
        popup.destroy()

    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    b1= ttk.Button(popup, text="Okay", command = leavemini)
    b1.pack()
    popup.mainloop()
#Pulls live data from text file, will eventually parse from server
def animate(i):
    #acess the JSON data from BTC-E and converts to proper format
    dataLink = 'https://btc-e.com/api/3/trades/btc_usd?limit=2000'
    data = urllib.request.urlopen(dataLink)
    data = data.read().decode("utf-8")
    data = json.loads(data)

    
    data = data["btc_usd"]
    data = pd.DataFrame(data)

    buys = data[(data['type']=="bid")]
    buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
    buyDates = (buys["datestamp"]).tolist()

    #pulls specific data from Json file 
    sells = data[(data['type']=="ask")]
    sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
    sellDates = (sells["datestamp"]).tolist()

    a.clear()

    a.plot_date(buyDates, buys["price"], "#00A3E0", label="buys")
    a.plot_date(sellDates, sells["price"], "#183A54", label="sells")
    #creates legend for buy and sell
    a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
             ncol=2, borderaxespad=0)

    title = "BTC-e BTCUSD Prices\nLast Price: "+str(data["price"][1999])
    a.set_title(title)

    
            
#Main class
class SeaOfBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.wm_title(self, "Bit Coin Trading")
        #frame for window
        container = tk.Frame(self) 
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #creats menu bar
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save Settings", command = lambda: popupmsg("Not suported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command = quit)
        menubar.add_cascade(label="File", menu=filemenu)

        exchangeChoice = tk.Menu(menubar, tearoff=1)
        exchangeChoice.add_command(label="BTC-e",
                                   command=lambda: changeExchange("BTC-e","btce"))
        exchangeChoice.add_command(label="Bitfinex",
                                   command=lambda: changeExchange("BitFinex","bitfinex"))
        exchangeChoice.add_command(label="Bitstamp",
                                   command=lambda: changeExchange("Bitstamp","bitstamp"))
        exchangeChoice.add_command(label="Huobi",
                                   command=lambda: changeExchange("Huobi","huobi"))
        #Creates menubar for exchange
        menubar.add_cascade(label="Exchange", menu=exchangeChoice)
        
        dataTF = tk.Menu(menubar, tearoff=1)
        dataTF.add_command(label = "Tick",
                           command=lambda: changeTimeFrame('tick'))
        dataTF.add_command(label = "1 Day",
                           command=lambda: changeTimeFrame('1d'))

        dataTF.add_command(label = "3 Day",
                           command=lambda: changeTimeFrame('3d'))

        dataTF.add_command(label = "1 Week",
                           command=lambda: changeTimeFrame('7d'))
        menubar.add_cascade(label = "Date Time Frame", menu = dataTF)
        # Time by minutes
        OHLCI = tk.Menu(menubar, tearoff=1)
        OHLCI.add_command(label = "Tick",
                          command = lambda: changeTimeFrame('tick'))
        OHLCI.add_command(label = "1 minute",
                          command = lambda: changeSampleSize('1Min', 0.0005))
        OHLCI.add_command(label = "5 minute",
                          command = lambda: changeSampleSize('5Min', 0.0003))
        OHLCI.add_command(label = "15 minute",
                          command = lambda: changeSampleSize('15Min', 0.0008))
        OHLCI.add_command(label = "30 minute",
                          command = lambda: changeSampleSize('30Min', 0.0016))
        OHLCI.add_command(label = "1 hour",
                          command = lambda: changeSampleSize('1H', 0.032))
        OHLCI.add_command(label = "3 hour",
                          command = lambda: changeSampleSize('3H', 0.096))

        menubar.add_cascade(label ="OHLC Interval", menu=OHLCI)
       






        

        tk.Tk.config(self, menu=menubar)
                
        
        self.frames = {}
        #defines what is to be stored in the frame, continually adding pages 
        for F in (StartPage, BTCe_Page):
        
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()


#page leads to all other pages        
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text=("""This application was built for FUN, use at your own risk! All code is open source"""), font="LARGE_FONT")
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Agree",
                            command=lambda: controller.show_frame(BTCe_Page))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree",
                            command=quit)
        button2.pack()

        


#built but not used in dev enivorment
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page One!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()



#page containing live graph, currently sourcing from server
class BTCe_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        
        #dimentions of graph
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand = True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        
        
        
app = SeaOfBTCapp()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=5000)
app.mainloop()
