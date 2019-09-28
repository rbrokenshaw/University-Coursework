
from tkinter import *
import tkinter.messagebox
from sections.sit_formative_tests import FormativeTestMenu
from sections.sit_summative_tests import SummativeTestMenu
from sections.view_results import ViewResults

class MainMenuStudent(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.grid()
		self.getMainMenu()

	# Student Menu
	def getMainMenu(self):

		# Get the logged in user's name
		with open("./users/userloggedin.txt") as text_file:
			userInfo = text_file.read()
			userInfoList = userInfo.split(",")
			secondName = re.sub("\n", "", userInfoList[2])
			userName = userInfoList[1] + " " + secondName

		# the menu items
		lblMenuTitle = Label(self, text='Main Menu', font=('Courier New', 25, 'bold'), fg='firebrick3')
		lblMenuTitle.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky=N)

		lblMenuTitle = Label(self, text='Welcome, ' + userName + "! Please select a task:", font=('verdana', 12, 'bold'))
		lblMenuTitle.grid(row=1, column=0, columnspan=3, padx=100, pady=(0,10), sticky=N)

		buttonFormativeTests = Button(self, text="Formative Tests", font=('verdana', 12, 'normal'), width=30, height=2)
		buttonFormativeTests['command']=self.openFormativeTests
		buttonFormativeTests.grid(row=2, column=1, padx=20, pady=10, sticky=N)

		buttonSummativeTests = Button(self, text="Summative Tests", font=('verdana', 12, 'normal'), width=30, height=2)
		buttonSummativeTests['command']=self.openSummativeTests
		buttonSummativeTests.grid(row=3, column=1, padx=20, pady=10, sticky=N)

		buttonViewResults = Button(self, text="View Results for Summative Tests", font=('verdana', 12, 'normal'), width=30, height=2)
		buttonViewResults['command']=self.openViewResults
		buttonViewResults.grid(row=4, column=1, padx=20, pady=10, sticky=N)
		buttonViewResults['state'] = 'disabled'

		buttonExitSystem = Button(self, text="Exit", font=('verdana', 12, 'normal'), width=8, height=2)
		buttonExitSystem['command']=self.exitSystem
		buttonExitSystem.grid(row=5, column=1, padx=20, pady=10, sticky=N)

	# Open Formative Tests in new frame
	def openFormativeTests(self):
		self.newWindow = Toplevel(self.master)
		self.app = FormativeTestMenu(self.newWindow)
		self.centre()

	# Open Summative Tests in new frame
	def openSummativeTests(self):
		self.newWindow = Toplevel(self.master)
		self.app = SummativeTestMenu(self.newWindow)
		self.centre()

	# Open View Results in new frame
	def openViewResults(self):
	 	self.newWindow = Toplevel(self.master)
	 	self.app = ViewResults(self.newWindow)
	 	self.centre()

	# Exit system
	def exitSystem(self):
		if tkinter.messagebox.askokcancel("Quit", "Are you sure you wish to log out and exit the system?"):
			self.quit()	

	# Centre the new window
	def centre(self):
		self.newWindow.update_idletasks()
		x = (self.newWindow.winfo_screenwidth() - self.newWindow.winfo_reqwidth()) / 2
		y = (self.newWindow.winfo_screenheight() - self.newWindow.winfo_reqheight()) / 2
		self.newWindow.geometry("+%d+%d" % (x, y))
		self.newWindow.deiconify()