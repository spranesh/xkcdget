import BeautifulSoup as BS
import sys

''' This file is the Parse Module, and contains the Parse Class'''


layoutChanged 	= "XKCD has probably changed its layout. Contact us :P. \n"

class Parse:

	def __init__(self, soup, UserInterface):
		self.soup = soup
		self.UI = UserInterface
		
	def getComicNumber(self):
		'''The function returns Comic number present in the soup given'''

		#First find the li, with the "Prev" string.
		#Two of these should exist. For the top bar, and the bottom bar
		liList = self.soup.findAll("li")
		liCandidates = [liTag for liTag in liList if str(liTag).find("Prev") != -1 ]
		if len(liCandidates) !=2 : 
			self.layoutChanged()

		#Now we proceed to extract the last comic's number
		#next goes to the child, ["href"] is a dictionary reference to get the
		#attributes of the reference tag. We then strip the /'s on both side of the 
		#comic say, /foobar/, and return the comic number as an int. (Add one to get
		#current.)
		CCno = int(str(liCandidates.pop(0).next["href"]).strip('/'))+1
		return CCno


	def getImgAttr(self):
		''' The function returns an iterable containing exactly 3 elements. In order, Image URL, title, and
		mouseover text '''
		try :
			reqdImg = self.soup.findAll("img")[1]
		except: 
			self.layoutChanged()
		return [str(reqdImg[a]) for a in ("src", "alt", "title")]
	
	def layoutChanged(self):
		'''Prints an apt message about layout being Changed and exits'''
		self.UI.display(layoutChanged)
		sys.exit()
