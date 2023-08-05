from pynord.util import util
import subprocess
import random
import os

class PyNord():
	def __init__(self, verbose=False):
		self.verbose = verbose
		util.check_install(self)

	def status(self):
		raw_out = util.system(self, command='nordvpn status')
		util.print(self, raw_out)
		status = util.parse(self, string=raw_out)
		return status

	# TODO: add double vpn functionality
	def connect(self, server=False, timeout=10):
		if server:
			log = util.system(self, command='nordvpn connect {server}', timeout=timeout)
		else:
			log = util.system(self, command='nordvpn connect', timeout=timeout)
		if self.status() is False:
			raise Exception('ERROR: VPN Connection Failed.')
		util.print(self, log)

	def disconnect(self):
		log = util.system(self, command='nordvpn disconnect')
		util.print(self, log)

	def killswitch(self, toggle: bool):
		if toggle:
			log = util.system(self, command='nordvpn set killswitch on')
		else:
			log = util.system(self, command='nordvpn set killswitch on')
		util.print(self, log)

	# TODO: add login and install functionality
	def login(self):
		return






