# $language = "python"
# $interface = "1.0"

#
#
# Modified for Gold labs
# Purpose:
# This script demonstrates resets the devices to default config. 
# It sends different sets of commands based on the device type and also checks the appropriate prompts before sending the right commands.
#

import re

def getpodno (ip,port):
	x = int(ip.split(".")[3])-240
	if int(port) >= 2066 and int(port) <= 2079 and int(port) != 2078:
		x = (x*2) - 1
		return str(x)
	elif int(port) >= 2078 and int(port) <= 2092 and int(port) != 2079:
		x = (x*2)
		return str(x)
	else:
		return ""

initialTab = crt.GetScriptTab()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Main():
	
	WLC_COMMANDS = """
clear config
y
reset system
ny


"""
	
	ROUTER_COMMANDS = """
copy bootflash:underlay-new running-config



"""
	
	SWITCH_COMMANDS = """
copy flash:underlay-new running-config



"""
	reset_current_tab_only_flag = 0
	if crt.Arguments and crt.Arguments[0] == 'currentonly':
		reset_current_tab_only_flag = 1
		response = crt.Dialog.MessageBox("Are you sure you want to RESET the individual device in current active session?", "Confirm", BUTTON_YESNO)
	else:
		response = crt.Dialog.MessageBox("Are you sure you want to RESET the devices in active sessions?", "Confirm", BUTTON_YESNO)

	if response != IDYES:
		return

	# Activate each tab in order from left to right, and issue the command in each "connected" tab...
	skippedTabs = ""
	for i in range(1, crt.GetTabCount()+1):
		
		tab = crt.GetTab(i)
		
		if reset_current_tab_only_flag == 1:
			tab = crt.GetScriptTab()
		
		tab.Activate()
		
		if tab.Session.Connected == True:
			
			podno = getpodno(tab.Session.RemoteAddress, tab.Session.RemotePort)
			if " - pod-" not in tab.Caption and podno != "":
				temp = tab.Caption + " - pod-" + podno
				temp = re.sub(r'\s+\(\d+\)', '', temp)
				tab.Caption = temp
			
			
			if "WLC" in tab.Caption:
				tab.Screen.Send("\n")
				while True:				
					if not tab.Screen.WaitForCursor(1):
						break
				tab.Screen.Send("\n")
				row = tab.Screen.CurrentRow
				prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
				prompt = prompt.strip()
				if "ser:" in prompt:
					tab.Screen.Send("dnac" + "\n")
					tab.Screen.Send("dnac123" + "\n")
				elif "WLC" in prompt:
					pass
				else:
					crt.Dialog.MessageBox("Could not understand the prompt of tab - " + tab.Caption + ". Hence skipping that one")
					continue
				
				for line in WLC_COMMANDS.split("\n"):
					tab.Screen.Send(line + "\n")
			
			elif "-3850-" in tab.Caption or "-4503-" in tab.Caption or "-9300-" in tab.Caption or "-ASR" in tab.Caption or "-ISR" in tab.Caption:
				tab.Screen.Send("\r\n")
				tab.Screen.Send("\r\n")
				while True:
					if not tab.Screen.WaitForCursor(1):
						break
				
				tab.Screen.Send("\r\n")
				row = tab.Screen.CurrentRow
				prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
				prompt = prompt.strip()
				
				if "(config" in prompt:
					tab.Screen.Send("end" + "\n")
					crt.Dialog.MessageBox("Device already booted up - " + tab.Caption + ". Hence skipping that one")
					if reset_current_tab_only_flag == 1:
						break
					else:
						continue
				elif "initial configuration dialog" in prompt:
					tab.Screen.Send("no" + "\n")
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
							
					tab.Screen.Send("yes" + "\n")
					tab.Screen.Send("\r\n")
					tab.Screen.Send("\r\n")
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
					tab.Screen.Send("\r\n")       
					tab.Screen.Send("en" + "\n")
					
					while True:
						if not tab.Screen.WaitForCursor(1):
							break		
					
					tab.Screen.Send("\r\n")
					row = tab.Screen.CurrentRow
					prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
					prompt = prompt.strip()
					
					#crt.Dialog.MessageBox("this is the prompt valude - " + prompt + ". Hence skipping that one")					
					#if "#" not in prompt:
					#	tab.Screen.Send("dnac123" + "\n")
				
					while True:
						if not tab.Screen.WaitForCursor(1):
							break

					row = tab.Screen.CurrentRow
					prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
					prompt = prompt.strip()
					
					if ">" in prompt:
						tab.Screen.Send("en" + "\n")
					
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
					
					tab.Screen.Send("\n")
					
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
					
					row = tab.Screen.CurrentRow
					prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
					prompt = prompt.strip()
					
					if ">" in prompt:
						crt.Dialog.MessageBox("The standard enable passwords are not working. Please check manually for the tab - " + tab.Caption)
						continue

				elif "sername" in prompt:
					tab.Screen.Send("dnac" + "\n")
					
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
					
					tab.Screen.Send("dnac123" + "\n")
					
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
					
					row = tab.Screen.CurrentRow
					prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
					prompt = prompt.strip()
					
					if ">" in prompt:
						tab.Screen.Send("en" + "\n")
						
						while True:
							if not tab.Screen.WaitForCursor(1):
								break
						
						row = tab.Screen.CurrentRow
						prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
						prompt = prompt.strip()
						
						if "#" not in prompt:
							tab.Screen.Send("dnac123" + "\n")
					
					elif "sername" in prompt:
						crt.Dialog.MessageBox("The standard username / password are not working. Please check manually for the tab - " + tab.Caption)
						continue
					
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
					
					row = tab.Screen.CurrentRow
					prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
					prompt = prompt.strip()
					
					if ">" in prompt:
						tab.Screen.Send("en" + "\n")
						
						while True:
							if not tab.Screen.WaitForCursor(1):
								break
						
						tab.Screen.Send("\n")
					
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
					
					row = tab.Screen.CurrentRow
					prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
					prompt = prompt.strip()
					
					if ">" in prompt:
						crt.Dialog.MessageBox("The standard enable passwords are not working. Please check manually for the tab - " + tab.Caption)
						continue
					
					crt.Dialog.MessageBox("Device already booted up - " + tab.Caption + ". Hence skipping that one")
					if reset_current_tab_only_flag == 1:
						break
					else:
						continue

				elif ">" in prompt:
					tab.Screen.Send("en" + "\n")
					
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
					
					row = tab.Screen.CurrentRow
					prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
					prompt = prompt.strip()
					
					if "#" not in prompt:
						tab.Screen.Send("dnac123" + "\n")
				
					while True:
						if not tab.Screen.WaitForCursor(1):
							break

					row = tab.Screen.CurrentRow
					prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
					prompt = prompt.strip()
					
					if ">" in prompt:
						tab.Screen.Send("en" + "\n")
					
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
					
					tab.Screen.Send("\n")
					
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
					
					row = tab.Screen.CurrentRow
					prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
					prompt = prompt.strip()
					
					if ">" in prompt:
						crt.Dialog.MessageBox("The standard enable passwords are not working. Please check manually for the tab - " + tab.Caption)
						continue
					
					crt.Dialog.MessageBox("Device already booted up - " + tab.Caption + ". Hence skipping that one")
					if reset_current_tab_only_flag == 1:
						break
					else:
						continue


				elif "More" in prompt:
					tab.Screen.Send("q" + "\n")
					crt.Dialog.MessageBox("Device already booted up - " + tab.Caption + ". Hence skipping that one")
					if reset_current_tab_only_flag == 1:
						break
					else:
						continue
				elif "#" in prompt:
					crt.Dialog.MessageBox("Device already booted up - " + tab.Caption + ". Hence skipping that one")
					if reset_current_tab_only_flag == 1:
						break
					else:
						continue
				else:
					crt.Dialog.MessageBox("Could not understand the prompt of tab - " + tab.Caption + ". Hence skipping that one")
					if reset_current_tab_only_flag == 1:
						break
					else:
						continue
				
				if "-3850-" in tab.Caption or "-9300-" in tab.Caption or "-ASR" in tab.Caption or "-ISR" in tab.Caption:
					for line in SWITCH_COMMANDS.split("\n"):
						tab.Screen.Send(line + "\n")
					
					tab.Screen.Send("\n")
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
						
					tab.Screen.Send("\n")    
				elif "-4503-" in tab.Caption:
					for line in ROUTER_COMMANDS.split("\n"):
						tab.Screen.Send(line + "\n")

					tab.Screen.Send("\n")
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
							
					tab.Screen.Send("\n")        
		
		if reset_current_tab_only_flag == 1:
			break
		
Main()

