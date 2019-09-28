from tkinter import *

class ViewResults(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.grid()
		self.viewSummResults()

# Create a list where completed summative tests are displayed and can be selected
	def viewSummResults(self):
		lblTestTitle = Label(self, text='Summative Tests taken', font=('verdana', 20, 'bold'))
		lblTestTitle.grid(row=0, column=0, columnspan=3, sticky=W)
		lblUser=Label(self,text='You are logged in as: [insert username here]',font=('verdana',12,'bold'))
		lblUser.grid(row=1, column=0, columnspan=3)
		self.testData=Listbox(self)
		self.testData.grid(row=3, column=1)






