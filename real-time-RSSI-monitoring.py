import subprocess
import re
import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize a figure in which the graph will be plotted
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Initialize times and RSSI arrays
times, RSSIs = [], []

# Maximum number of data points to keep in the plot
max_data_points = 6

def animate(frame, times, RSSIs):
    # Launch the subprocess to capture the RSSI
    p = subprocess.Popen("netsh wlan show interfaces", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read().decode()
    m = re.findall("Name.*?:.*?(?=\S*['-])([a-zA-Z'-]+).*?Signal.*?:.*?([0-9]*)%", out, re.DOTALL)
    p.communicate()

    # Append the RSSIs and times arrays with the updated values
    RSSIs.append(int(m[0][1]))

    # Format the time directly as HH:MM:SS
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    times.append(current_time)

    # Limit x and y lists to max_data_points items
    if len(times) > max_data_points:
        times.pop(0)  # Remove the oldest time
        RSSIs.pop(0)  # Remove the corresponding RSSI value

    # Clear the plot and redraw it
    ax.clear()
    ax.plot(times, RSSIs)

    # Formatting the plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title("{}'s RSSI over time".format(m[0][0]))
    plt.ylabel('RSSI')
    plt.xlabel('Time')

    # Print RSSIs and times for debugging
    print("RSSIs", RSSIs)
    print("times", times)

    # Return the ax object as a tuple
    return ax,

# FuncAnimation function which automates updating the graph by repeatedly calling the animate function
animation = FuncAnimation(fig, animate, fargs=(times, RSSIs), interval=1000)
plt.show()
