'''This is the UI module, and contains the UI class'''

# we set default external Program Variables
# External Program Name
# External Program Arguments
# External Program Arguments in case of Warning
# Default Operating System
# Path of the Operating Sytem
__EPN__ = 'zenity'
__EPA__ = "--info --title=XKCDGet --text='%s'"
__EPW__ = "--warning --title=XKCDGet --text='%s"
__OS__ = 'linux'
__OSPATH__ = 'PATH'
hasEasyGUI = True

import sys
import os

try:
	import easygui
except ImportError:
	hasEasyGUI = False

class UI:
	'''The class defines the UI.'''
	
	 
	# All variables and function Names use CamelFont Notation. Variables start with lower case,
	# and Functions with upper Case.
	#
	# The variables of this class are
	# gui - 1 if gui is to be used.
	# useExtProgram - 1 if the other external Program specified during init is to be used
	# extProgName - string containing the name of the external Program
	# extProgArgs - string containing 1 unfilled varible, that represents the external Program Args
	# hostOS - OS of the computer for which the external Program Name is valid
	# OSPath - path of the host operating system
	#
	# The class consists of private and public functions 
	# Private functions (other than __init__) are given the name __name__ for consistency, with Python 
	# programming recommendations.
	
	
	gui = 0
	useExtProgram = 0
	extProgName = ''
	extProgArgs = ''
	hostOS = ''
	OSPath = ''

	def __init__(self, args, otherProgName=__EPN__, otherProgArgs=__EPA__, passedOS=__OS__, passedPath = __OSPATH__):
		'''Inits the class by parsing args, and setting external Program.\n
		A typical example in calling Zenity would be to pass \notherProgName = "zenity"
		and \notherProgArgs="--info --title=XKCDGet --text='%s'" %s deontes, the place 
		where the text should come in.\nArguments in case of an error can be passed to 
		display itself.'''
		
		self.extProgName = otherProgName
		self.extProgArgs = otherProgArgs
		self.hostOS = passedOS
		self.OSPath = passedPath
		
		self.__setGui__(args)
		self.__setUseExtProgram__(args)


	def __setGui__(self, li):
		'''Parses Command line args and returns 1 if -g option was specified, and 0 otherwise'''
		# We have to use print in the following lines, since we do not know if the user has 
		# enabled gui mode, and whether he has the necessary libs
		if len(li) > 2:
			print " Invalid Usage. Usage is XKCDGet.py with optional -g (GUI) -c (Command line) or -n (GUI but NO Zenity) flag.\n"
			sys.exit()
		
		# we now set defaults for the operating systems
		if sys.platform == 'win32': self.gui = 1
		else: self.gui = 0
		
		# now we see if these options have been forcibly reset or not
		if len(li) == 2:
			if li[1] in ['-g', '-n']:
				self.gui = 1
			elif li[1] == '-c':
				self.gui = 0
		

	def __setUseExtProgram__(self, args):
		'''Sets by parsing args, and running through the path, if the external Program specified can be used'''
		ProgCount = 0
		if len(args) == 2 and args[1] == '-n':
			if hasEasyGUI == False:
					print "ERROR: Falling back to command line, no EasyGUI found"
					self.gui = 0
		elif sys.platform[:len(self.hostOS)]==self.hostOS:
			for root in os.environ[self.OSPath].split(':'):
				for pdir, dirs, files in os.walk(root):
					ProgCount += len([file for file in files if file == self.extProgName])

		self.useExtProgram = ProgCount


	def display(self, msgString , error = 0, errorArgs=__EPW__):
		'''A wrapper for the print function. Displays information in the proper UI'''
		if self.gui==0:
			print msgString
		else:
			if self.useExtProgram == 0:
				easygui.msgbox(message = msgString, title="XKCDGet", buttonMessage="OK")
			else:
				if not error:
					try:
						os.system("%s %s"%
								(self.extProgName, 
									self.extProgArgs % msgString.replace("'", '"')))
					except:
						self.useExtProgram = 0
						self.display(msgString, 0)
				else:
					try:
						os.system("%s %s"%
								(self.extProgName, 
									errorArgs % msgString.replace("'", '"')))
					except:
						self.useExtProgram = 0
						self.display(msgString ,error, errorArgs)
		
