"""RIPE ATLAS Probe Version 3 (ID:23232)"""
#Tkinter imports
import tkinter as tk
#Web imports
import urllib
from urllib import request
import json

#Scientist imports
import pandas as pd
import numpy as np

#Matplotlib imports
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

#System imports
import sys
import datetime

#Prepared definitions
matplotlib.use("TkAgg")
f = Figure(figsize=(9,5), dpi=100, facecolor='white')
a = f.add_subplot(1,1,1, axisbg='white')
style.use(['ggplot'])
matplotlib.rcParams.update({'font.size': 8})
matplotlib.rcParams.update({'font.family': "monospace"})


#Frames and Tkinter
class RipeFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class RipeProbeReporter(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="favicon.ico")
        tk.Tk.wm_title(self, "RIPE Probe RTT Graph")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        frame1 = RipeFrame(container, self)
        frame1.configure(background="white")
        frame1.grid(row=0, column=0, sticky="wesn")
        frame1.tkraise()
        

def read_data(i):
    import datetime

    endTime = datetime.datetime.now().replace(microsecond=0)
    endTime = endTime.isoformat()
    startTime = datetime.datetime.now() - datetime.timedelta(hours=12)
    startTime = startTime.replace(microsecond=0)
    startTime = startTime.isoformat()

    url = ("https://stat.ripe.net/data/atlas-ping-measurements/data.json?probe_id=23232&measurement_id=2&starttime=" + startTime + "&endtime=" + endTime + "&resolution=0&display_mode=condensed")

    data = urllib.request.urlopen(url)
    data = data.readall().decode("utf-8")
    data = json.loads(data)
        
    data = data["data"]["measurements"]
    data = pd.DataFrame(data)

    RTT = data
 
    RTT["timestamps"] = np.array(RTT["timestamp"]).astype("datetime64[s]")
    timeRTT = (RTT["timestamps"]).tolist()

    RTT_MEAN = data
    RTT_MEAN["timestamps"] = np.array(RTT_MEAN["timestamp"]).astype("datetime64[s]")
    timeRTT_MEAN = (RTT_MEAN["timestamps"]).tolist()
    
    a.clear()

    a.plot_date(timeRTT, RTT["rtt_med"], "#3366CC", label="RTT_MEAN")
    a.plot_date(timeRTT_MEAN, RTT_MEAN["rtt_95pct"], "#FF0000", label="RTT_MAX")

    a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
             ncol=2, borderaxespad=0)

    title = "RIPE PROBE NSR\nLast RTT: "+str(data["rtt_med"][118])
    a.set_title(title, fontsize=12)
  

#Main
def main():
    app = RipeProbeReporter()
    ani = animation.FuncAnimation(f, read_data, interval=1000)
    app.mainloop()
   

if __name__ == '__main__':
    main()
