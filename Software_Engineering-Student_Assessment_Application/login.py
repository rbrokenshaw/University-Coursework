from tkinter import *
import tkinter.messagebox
import csv
from sections.main_menu_staff import MainMenuStaff
from sections.main_menu_student import MainMenuStudent

class Login(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.grid()
		self.getLogin()

	# Login form
	def getLogin(self):
		lblLoginTitle = Label(self, text='Academic Testing Software', font=('Courier New', 20, 'bold'), fg='firebrick3')
		lblLoginTitle.grid(row=0, column=0, columnspan=3, padx=10, pady=20, sticky=N)

		lblLoginDescription = Label(self, text='Please enter your login details:', font=('verdana', 12, 'bold'))
		lblLoginDescription.grid(row=1, column=0, columnspan=3, padx=10, pady=(0,10), sticky=W)

		self.varUserType = StringVar(value="Staff")

		lblEnterUserNumber = Label(self, text='User Type:', font=('verdana', 12, 'bold'))
		lblEnterUserNumber.grid(row=3, column=0, columnspan=2, padx=(30,0), sticky=W)

		lblEnterUserNumber = Label(self, text='User Number:', font=('verdana', 12, 'bold'))
		lblEnterUserNumber.grid(row=4, column=0, columnspan=2, padx=(30,0), sticky=W)

		lblEnterUserPassword = Label(self, text='Password:', font=('verdana', 12, 'bold'))
		lblEnterUserPassword.grid(row=5, column=0, columnspan=2, padx=(30,0), sticky=W)

		optionMenuUserType = OptionMenu(self, self.varUserType, "Staff", "Student")
		optionMenuUserType.grid(row=3, column=2, sticky=W)

		self.entryUserNumber = Entry(self)
		self.entryUserNumber.grid(row=4, column=2, padx=(0,30), sticky=N)

		self.entryUserPassword = Entry(self, show="*")
		self.entryUserPassword.grid(row=5, column=2, padx=(0,30), sticky=N)

		buttonLoginUser = Button(self, text="Login", font=('verdana', 12, 'normal'), width=8, height=2)
		buttonLoginUser['command']=self.loginUser
		buttonLoginUser.grid(row=6, column=2, padx=(0,30), pady=10, sticky=E)

		lblLoginDemo = Label(self, text='Logins for demonstration:\n staff username: SF00001, password: password\n student username: ST00001, password: password', font=('verdana', 9, 'bold'))
		lblLoginDemo.grid(row=8, column=0, columnspan=3, sticky=NSEW)

		lblBypassDescription = Label(self, text='Bypass the login (for testing purposes only):', font=('verdana', 9, 'bold'))
		lblBypassDescription.grid(row=9, column=0, columnspan=3, sticky=NSEW)

		buttonBypassStaff = Button(self, text="Staff Menu", font=('verdana', 12, 'normal'))
		buttonBypassStaff['command']=self.openStaffMenu
		buttonBypassStaff.grid(row=10, column=0, sticky=W)

		buttonBypassStudent = Button(self, text="Student Menu", font=('verdana', 12, 'normal'))
		buttonBypassStudent['command']=self.openStudentMenu
		buttonBypassStudent.grid(row=10, column=2, sticky=E)

	# Log the user in
	def loginUser(self):		
		userType = self.varUserType.get()
		userNumber = self.entryUserNumber.get()
		userNumber = userNumber.upper()
		userPassword = self.entryUserPassword.get()
		userNumberExists = 0

		# Check if user has selected 'Staff'
		if userType == "Staff":

			# Make a list of the staff in the csv file for checking usernames and passwords
			userList = []
			with open("./users/staff.csv") as staff_csv:
				csv_reader = csv.reader(staff_csv, delimiter=',')
				next(staff_csv)
				for row in staff_csv:
					a = "".join(row)
					aSplit = a.split(",")
					userList.append(aSplit)

			# Identify staff numbers, first names and last names
			for i in userList:
				userNumberFromDB = i[0]
				userFirstNameFromDB = i[2]
				userSecondNameFromDB = i[3]

				# Check for a matching staff number
				if userNumberFromDB == userNumber:
					userNumberExists = 1
					userPasswordFromDB = i[1]

					#Check for matching password
					if userPasswordFromDB == userPassword:
						userToWrite = userNumberFromDB + "," + userFirstNameFromDB + "," + userSecondNameFromDB
						with open("./users/userloggedin.txt", 'w') as text_file:
							text_file.write(userToWrite)
						self.openStaffMenu()
					else:
						tkinter.messagebox.showinfo("Login Failed", "Sorry, that password is incorrect")

			if userNumberExists == 0:
				tkinter.messagebox.showinfo("Login Failed", "Sorry, that User Number is incorrect")

		# Check if user has selected 'Student'
		elif userType == "Student":
			userList = []
			with open("./users/students.csv") as students_csv:
				csv_reader = csv.reader(students_csv, delimiter=',')
				next(students_csv)
				for row in students_csv:
					a = "".join(row)
					aSplit = a.split(",")
					userList.append(aSplit)

			# Identify student numbers, first names and last names
			for i in userList:
				userNumberFromDB = i[0]
				userFirstNameFromDB = i[2]
				userSecondNameFromDB = i[3]

				# Check for matching student number
				if userNumberFromDB == userNumber:
					userNumberExists = 1
					userPasswordFromDB = i[1]

					# Check for matching password
					if userPasswordFromDB == userPassword:
						userToWrite = userNumberFromDB + "," + userFirstNameFromDB + "," + userSecondNameFromDB
						with open("./users/userloggedin.txt", 'w') as text_file:
							text_file.write(userToWrite)						
						self.openStudentMenu()
					else:
						tkinter.messagebox.showinfo("Login Failed", "Sorry, that password is incorrect")

			if userNumberExists == 0:
				tkinter.messagebox.showinfo("Login Failed", "Sorry, that User Number is incorrect")

	# Open the Staff menu in a new frame
	def openStaffMenu(self):
		self.newWindow = Toplevel(self.master)
		self.app = MainMenuStaff(self.newWindow)
		self.centre()
		root.withdraw()

	# Open the Student menu in a new frame
	def openStudentMenu(self):
		self.newWindow = Toplevel(self.master)
		self.app = MainMenuStudent(self.newWindow)
		self.centre()
		root.withdraw()

	# Centre the new window
	def centre(self):
		self.newWindow.withdraw()
		self.newWindow.update_idletasks()
		x = (self.newWindow.winfo_screenwidth() - self.newWindow.winfo_reqwidth()) / 2
		y = (self.newWindow.winfo_screenheight() - self.newWindow.winfo_reqheight()) / 2
		self.newWindow.geometry("+%d+%d" % (x, y))
		self.newWindow.deiconify()


#DO NOT CHANGE ANYTHING BELOW THIS!!!! IMPORTANT!!!
# Identify the root
root = Tk()
root.title("Academic Testing Software")
app = Login(root)

# Centre the root window when it launches
root.withdraw()
root.update_idletasks()
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.geometry("+%d+%d" % (x, y))
root.deiconify()

# Launch the root window
root.mainloop() 