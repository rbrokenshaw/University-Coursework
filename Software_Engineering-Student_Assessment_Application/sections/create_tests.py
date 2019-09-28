from tkinter import *

class CreateTests(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.grid()
		self.className()

	def className(self):
		lblTestTitle = Label(self, text='This section is under construction', font=('verdana', 20, 'bold'))
		lblTestTitle.grid(row=0, column=0, columnspan=3, sticky=W)
		