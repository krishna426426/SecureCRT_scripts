# $language = "python"
# $interface = "1.0"

#
# Author: Anand Kanani
#
# Purpose:
# This script demonstrates resets the devices to default config. 
# It sends different sets of commands based on the device type and also checks the appropriate prompts before sending the right commands.
#

import re

def getpodno (ip,port):
	x = int(ip.split(".")[3])-10
	if int(port) >= 2002 and int(port) <= 2008:
		x = (x*2) - 1
		return str(x)
	elif int(port) >= 2010 and int(port) <= 20016:
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
wr mem
delete /force nvram:*.cer
delete /force nvram:*pnp*
delete /f *pnp*

write erase

reload
y

"""
	
	SWITCH_COMMANDS = """
wr mem
delete /force nvram:*.cer
delete /force nvram:*pnp*
delete /f *pnp*

write erase

reload
y

"""
	reset_current_tab_only_flag = 0
	if crt.Arguments and crt.Arguments[0] == 'currentonly':
		reset_current_tab_only_flag = 1
		response = crt.Dialog.MessageBox("Are you sure you want to CONFIGURE the individual device with underlay configuration?", "Confirm", BUTTON_YESNO)
	else:
		response = crt.Dialog.MessageBox("Are you sure you want to CONFIGURE all the devices in active sessions with underlay configuration?", "Confirm", BUTTON_YESNO)

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
					tab.Screen.Send("netadmin" + "\n")
					tab.Screen.Send("Dnac123!" + "\n")
				elif "WLC" in prompt:
					pass
				else:
					crt.Dialog.MessageBox("Could not understand the prompt of tab - " + tab.Caption + ". Hence skipping that one")
					continue
				
				for line in WLC_COMMANDS.split("\n"):
					tab.Screen.Send(line + "\n")
			
			elif "Fusion" in tab.Caption or "Border" in tab.Caption or "Edge" in tab.Caption:
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
				elif "initial configuration dialog" in prompt:
					tab.Screen.Send("no" + "\n")
					tab.Screen.Send("yes" + "\n")
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
					tab.Screen.Send("\r\n")
					tab.Screen.Send("en" + "\n")
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
					
					row = tab.Screen.CurrentRow
					prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
					prompt = prompt.strip()
					
					if "#" not in prompt:
						tab.Screen.Send("Dnac123!" + "\n")
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
					
					row = tab.Screen.CurrentRow
					prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
					prompt = prompt.strip()
					
					if ">" in prompt:
						tab.Screen.Send("en" + "\n")

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
					tab.Screen.Send("netadmin" + "\n")
					
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
					
					tab.Screen.Send("Dnac123!" + "\n")
					
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
							tab.Screen.Send("Dnac123!" + "\n")
					
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
					
				elif ">" in prompt:
					tab.Screen.Send("en" + "\n")
					
					while True:
						if not tab.Screen.WaitForCursor(1):
							break
					
					row = tab.Screen.CurrentRow
					prompt = tab.Screen.Get(row, 0, row, tab.Screen.CurrentColumn - 1)
					prompt = prompt.strip()
					
					if "#" not in prompt:
						tab.Screen.Send("Dnac123!" + "\n")
				
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
						
				elif "More" in prompt:
					tab.Screen.Send("q" + "\n")
				elif "#" in prompt:
					pass
				else:
					crt.Dialog.MessageBox("Could not understand the prompt of tab - " + tab.Caption + ". Hence skipping that one")
					continue
				
				if "Edge1" in tab.Caption:
					selected_cmd_file = open('Edge1_config.txt', 'r')
					selected_cmd_file.seek(0)
					for each_line in selected_cmd_file.readlines():
						tab.Screen.Send(each_line + "\n")
					selected_cmd_file.close()
				
				if "Edge2" in tab.Caption:
					selected_cmd_file = open('Edge2_config.txt', 'r')
					selected_cmd_file.seek(0)
					for each_line in selected_cmd_file.readlines():
						tab.Screen.Send(each_line + "\n")
					selected_cmd_file.close()

				if "Fusion1" in tab.Caption:
					selected_cmd_file = open('Fusion1_config.txt', 'r')
					selected_cmd_file.seek(0)
					for each_line in selected_cmd_file.readlines():
						tab.Screen.Send(each_line + "\n")
					selected_cmd_file.close()

				if "Fusion2" in tab.Caption:
					selected_cmd_file = open('Fusion2_config.txt', 'r')
					selected_cmd_file.seek(0)
					for each_line in selected_cmd_file.readlines():
						tab.Screen.Send(each_line + "\n")
					selected_cmd_file.close()

				if "Border1" in tab.Caption:
					selected_cmd_file = open('Border1_config.txt', 'r')
					selected_cmd_file.seek(0)
					for each_line in selected_cmd_file.readlines():
						tab.Screen.Send(each_line + "\n")
					selected_cmd_file.close()

				if "Border2" in tab.Caption:
					selected_cmd_file = open('Border2_config.txt', 'r')
					selected_cmd_file.seek(0)
					for each_line in selected_cmd_file.readlines():
						tab.Screen.Send(each_line + "\n")
					selected_cmd_file.close()
		
		if reset_current_tab_only_flag == 1:
			break
		
Main()
