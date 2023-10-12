
'''
    This script does the following:
        
        *Captures the Signal Strenth (RSSI) of the used Wi-Fi and plots the variation over time in a graph


'''

#this code is not entirely the same as the one mentioned in the Lab ; some changes have been made which were inspired of 
#the source code mentioned in the link below:
#Reference : "https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/update-a-graph-in-real-time"

import subprocess
import re
import datetime
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation 



# initializing a figure in which the graph will be plotted

fig = plt.figure()
#describing how the values will be aranged
ax = fig.add_subplot(1, 1, 1)
   
#Initializing times and RSSI arrays
times , RSSIs = [] , []
  
def animate(frame,times,RSSIs):
    #launching the sub-process to capture the RSSI
    p = subprocess.Popen("netsh wlan show interfaces", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read().decode()
    m = re.findall("Name.*?:.*?(?=\S*['-])([a-zA-Z'-]+).*?Signal.*?:.*?([0-9]*)%", out, re.DOTALL)
    p.communicate()
    
    #appending the RSSIs and times arrays with the updated values
    RSSIs.append(int(m[0][1]))
    times.append(datetime.datetime.now().strftime('%H:%M:%S'))
     
    #Limit x and y lists to 100 items (this value could be augmented depending on the use case)
    times = times[-100:]
    RSSIs = RSSIs[-100:]

    # Draw x and y lists
    ax.clear()
    ax.plot(times,RSSIs)

    # Formating the plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title("{}'s RSSI over time".format(m[0][0]))
    plt.ylabel('RSSI')
    plt.xlabel('Time')
   
    print("RSSIs",RSSIs)
    print("times",times)
    #each time this function is called, it will return the tuple of the times and RSSIs values (time,RSSI)
    return ax,

#FunAnimation function which automates updating the graph by repeatedly calling the animate function
'''FunAnimation's arguments:
    *fig: the initialized figure (where we want to plot our values)
    *animate : the function to call for each frame (he frame: the single capture to each pair of values)
    *fargs: list of the optional arguments to pass to the animate function each time we call it
    *interval: the interval of time between frames
'''    
animation=FuncAnimation(fig,animate,fargs=(times,RSSIs),interval=1000)
plt.show()