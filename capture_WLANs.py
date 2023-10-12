import subprocess
import re
import platform
import time
 
def capture_WLAN():
	if platform.system() == 'Linux':
		#the pipe attribute indicates that the standard stream (STDIN or STDOUT or STDERR ) should be opened e.g the stream going in/out
		#to the parent process will be inherited by the child process (this subprocess)
		p = subprocess.Popen("iwconfig", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	elif platform.system() == 'Windows':
		p = subprocess.Popen("netsh wlan show networks mode=bssid ", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	else:
		raise Exception('reached else of if statement')
		
	out = p.stdout.read().decode('unicode_escape').strip()
	print(out)
    

	if platform.system() == 'Linux':
		m = re.findall('(wlan[0-9]+)', out, re.DOTALL)
	elif platform.system() == 'Windows':
		m = re.findall('SSID.*?:.*?([A-z - 0-9 ]*)', out, re.DOTALL)
		m= re.findall("SSID.*?:.*?([a-z A-Z 0-9]+).*?Signal.*?:.*?([0-9]*)%", out, re.DOTALL)
		signal = re.findall("SSID [0-9]+ :.*?([a-z A-Z 0-9]+).*?", out, re.DOTALL)
		rssi = re.findall("Signal.*?:.*?([0-9]*)%", out, re.DOTALL)
		BSSID = re.findall("BSSID 1.*?:.*?((?:[0-9a-fA-F]:?){12})", out, re.DOTALL)
		Channel=re.findall("Channel.*?:.*?([0-9]+)", out, re.DOTALL)
	
	else:
		raise Exception('reached else of if statement')

	p.communicate()
	Channel=tuple(int(item) for item in Channel)
	rssi=tuple(int(item) for item in rssi)
	
	data=list(zip(signal,rssi,Channel,BSSID))
	print(type(data[0][3]))
	
	return data



#while True:

#	data=capture_WLAN()	
#	print(data) 
#	time.sleep(1)
	
