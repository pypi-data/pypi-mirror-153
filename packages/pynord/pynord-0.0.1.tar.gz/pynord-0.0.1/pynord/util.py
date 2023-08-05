import subprocess
import random
import json
import sys
import os

printer = print
class helper:
	def run(command: str, timeout):
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		try:
			process.wait(timeout=timeout)
			log = process.communicate()[0].decode('utf-8')
		except subprocess.TimeoutExpired:
			process.kill()
			log = 'WARNING: Timeout Error Occurred.'
		return log
	def print(message):
		printer(message)

class util():
	def parse(self, string):
		# parsing nordvpn status
		if 'Status' in string:
			string = string[string.find('Status:'):]
			string = string.split('\n')
			if 'Disconnected' in string[0]:
				status = False
			else:
				status = True
			return status
		# parsing nordvpn --version
		elif 'NordVPN Version' in string:
			version = string.split()[2]
			return True
		elif 'command not found' in string:
			return False
		else:
			pass

	def check_install(self):
		# verify linux
		if sys.platform not in ['linux', 'linux2']:
			raise Exception('PyNord can only be run in a Linux enviroment.')
		# check nordvpn installation
		if 'command not found' in subprocess.getoutput('nordvpn --version'):
			selection = input("NordVPN Linux Client is not installed. Do you want to install it now? [Y/n] ").strip()
			if selection == 'Y':
				os.system('sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)')
			else:
				raise Exception('NordVPN is not installed. \nhttps://support.nordvpn.com/Connectivity/Linux/1325531132/Installing-and-using-NordVPN-on-Debian-Ubuntu-Raspberry-Pi-Elementary-OS-and-Linux-Mint.htm')

	def print(self, string):
		string = str(string)
		if self.verbose and string.strip():
			helper.print(string)

	def system(self, command, timeout=None):
		log = helper.run(command=command, timeout=timeout)
		return log





			