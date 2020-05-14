# $language = "python"
# $interface = "1.0"

#
# Modified for Gold labs
#
# Purpose:
# This script demonstrates resets the devices to default config. 
# It sends different sets of commands based on the device type and also checks the appropriate prompts before sending the right commands.
#

import re

def getpodno (ip,port):
	x = int(ip.split(".")[3])-240
	if int(port) >= 2067 and int(port) <= 2077 or int(port) == 2079:
		x = (x*2) - 1
		return str(x)
	elif int(port) >= 2078 and int(port) <= 2092 and int(port) != 2079:
		x = (x*2)
		return str(x)
	else:
		return ""

def Main():
	
	initialTab = crt.GetScriptTab()
	tabcount = crt.GetTabCount()
	
	for i in range(1, tabcount+1):
		tab = crt.GetTab(i)
		tab.Activate()
		
		if tab.Session.Connected == True:
			
			podno = getpodno(tab.Session.RemoteAddress, tab.Session.RemotePort)
			if " - pod-" not in tab.Caption and podno != "":
				temp = tab.Caption + " - pod-" + podno
				temp = re.sub(r'\s+\(\d+\)', '', temp)
				tab.Caption = temp
			
			
			if "WLC" in tab.Caption:
				row = tab.Screen.CurrentRow
				prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
				prompt = prompt.strip()
				if "ser:" in prompt:# or "terminate autoinstall" in prompt:
					tab.Session.Disconnect()
			
			elif "-3850-" in tab.Caption or "-4503-" in tab.Caption or "-9300-" in tab.Caption or "-ASR" in tab.Caption or "-ISR" in tab.Caption:
				tab.Screen.Send("\r\n")
				tab.Screen.Send("\r\n")
				tab.Screen.WaitForCursor(1)
				row = tab.Screen.CurrentRow
				prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
				prompt = prompt.strip()
				if "#" in prompt:
					tab.Session.Disconnect()
	
	i = 1
	while True:
		tabcount = crt.GetTabCount()
		
		if i > tabcount:
			break
		
		tab = crt.GetTab(i)
		tab.Activate()
		
		if tab.Session.Connected == False and tab.Caption != initialTab.Caption:
			tab.Close()
		else:
			i = i + 1
Main()
