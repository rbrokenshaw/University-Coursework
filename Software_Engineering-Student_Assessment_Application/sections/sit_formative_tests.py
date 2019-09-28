from tkinter import *
import csv, random, os, re
import tkinter.messagebox
import os.path
import pandas as pd

# Set the current test selected by the user
selectedTest = ""
# Set the first attempt score
attempt1Score = 0
# Set the second attempt score
attempt2Score = 0
# Set the third attempt score
attempt3Score = 0
# Store all attempts for comparison
allAttempts = []

#Formative Tests
class FormativeTestMenu(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.grid()
		self.getMenu()

	# Formative Test Menu
	def getMenu(self):

		# Title and Description
		lblTestTitle = Label(self, text='Formative Test Menu', font=('Courier New', 25, 'bold'), fg='firebrick3')
		lblTestTitle.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky=N)
		
		lblTestTitle = Label(self, text='Here is a list of available tests. Please select the test you would like to attempt:', font=('verdana', 12, 'normal'))
		lblTestTitle.grid(row=2, column=0, columnspan=5, padx=70, pady=(0,30), sticky=N)

		# Make a list of tests in the test directory
		self.testList = os.listdir("tests/formative/CMT001/")	
		self.testListBox = Listbox(self, width=25)
		self.testListBox.grid(row=3, column=2, sticky=N)

		for i in self.testList:
			i = re.sub(".csv", "", i)
			self.testListBox.insert(END, i)

		# Open test button
		buttonOpenTest = Button(self, text="Open Test", font=('verdana', 12, 'normal'), width=20, height=2, fg="green")
		buttonOpenTest['command']=self.openTest
		buttonOpenTest.grid(row=5, column=2, padx=20, pady=20, sticky=N)

		# Return to main menu button
		buttonReturn = Button(self, text="Return To Main Menu", font=('verdana', 12, 'normal'), width=20, height=2)
		buttonReturn['command']=self.openMainMenu
		buttonReturn.grid(row=6, column=2, padx=20, pady=5, sticky=N)

		# Exit system button
		buttonExit = Button(self, text="Exit", font=('verdana', 12, 'normal'), width=8, height=2)
		buttonExit['command']=self.exitSystem
		buttonExit.grid(row=7, column=2, padx=20, pady=5, sticky=N)

	# Open the selected test
	def openTest(self):

		# Get the selected test from the list
		testBoxSelection = (self.testListBox.curselection())

		try:
			testBoxSelection = testBoxSelection[0]
			global selectedTest
			selectedTest = self.testList[testBoxSelection]
			self.newWindow = Toplevel(self.master)

			# Create the results CSV file if none exists
			if os.path.isfile("./results/formative/" + selectedTest):
				pass
			else:
				with open ("./results/formative/" + selectedTest, mode="a") as results_csv:
					results_writer = csv.writer(results_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
					results_writer.writerow(['Student Number', 'Attempt No', 'Score', 'q1Answer', 'q2Answer', 'q3Answer', 'q4Answer', 'q5Answer', 'q6Answer', 'q7Answer', 'q8Answer', 'q9Answer', 'q10Answer'])

			# Open the test in a new window
			self.app = Test(self.newWindow)
		
		except IndexError:
			tkinter.messagebox.showinfo("Error", "Please select a test from the list")

	# Close the test menu frame
	def openMainMenu(self):
		self.master.destroy()

	# Exit the system
	def exitSystem(self):
		if tkinter.messagebox.askokcancel("Quit", "Are you sure you wish to exit the system?"):
			self.quit()

# The test frame
class Test(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.grid()
		self.attempts = 0
		self.getTestTitle()
		self.getTestQuestions()

	#show the test name, number of attempts and button to return to the formative test menu
	def getTestTitle(self):

		# Get the user logged in and see if they have taken the test before
		user_file = open("./users/userloggedin.txt", 'r')
		user = user_file.readline()
		userDetailsList = user.split(",")
		self.userNumber = userDetailsList[0]
		tests = user_file.readline()
		self.testsDone = tests.split(",")

		# Determine how many times user has previously sat the selected test as well as their scores using Pandas
		resultsInfo = pd.read_csv("./results/formative/" + selectedTest)
		resultsInfo.columns = ["Student_Number", "Attempt_No", "Score", "q1Answer", "q2Answer", "q3Answer", "q4Answer", "q5Answer", "q6Answer", "q7Answer", "q8Answer", "q9Answer", "q10Answer"]
		userList = list(resultsInfo.Student_Number)

		# Adjust the number of attempts if the test has been sat by this user before
		self.attempts += userList.count(self.userNumber)

		# Get the test name
		testName = selectedTest
		testName = re.sub(".csv", "", testName)
		lblTestTitle = Label(self, text=testName, font=('Courier New', 25, 'bold'), fg='firebrick3')
		lblTestTitle.grid(row=0, column=0, columnspan=5, padx=10, pady=(20,0), sticky=NW)

		if self.attempts == 0:
			self.lblAttempts = Label(self, text="You have 3 attempts. So far you have made " + str(self.attempts) + " attempts.", font=('verdana', 16, 'normal'), justify=LEFT)
			self.lblAttempts.grid(row=1, column=0, columnspan=10, padx=10, sticky=W)

		else:
			self.lblAttempts = Label(self, text="You have 3 attempts. So far you have made " + str(self.attempts) + " attempts.", font=('verdana', 16, 'normal'), justify=LEFT)
			self.lblAttempts.grid(row=1, column=0, columnspan=5, padx=10, sticky=W)

		# Show Highest Score
		self.lblHighestScore = Label(self, text="", font=('verdana', 16, 'bold'), justify=RIGHT)
		self.lblHighestScore.grid(row=1, column=6, columnspan=2, pady=(10,0), sticky=E)

		# See answers button
		self.buttonSeeAnswers = Button(self, text="See Answers", font=('verdana', 12, 'normal'), width=17, height=2, state = 'disabled')
		self.buttonSeeAnswers['command']=self.checkToViewAnswers
		self.buttonSeeAnswers.grid(row=0, column=5, padx=20, columnspan=2, pady=20, sticky=E)

		# Return to main menu
		buttonMainMenu = Button(self, text='Return to Tests Menu', font=('verdana', 12, 'normal'), width=20, height=2)
		buttonMainMenu['command']=self.closeWindow
		buttonMainMenu.grid(row=0, column=7, padx=20, pady=20, columnspan=1, sticky=SE)

	def checkToViewAnswers(self):
		if tkinter.messagebox.askokcancel("Warning", "You are about to be shown the answers for this test. You will not be allowed any more attempts. If you wish to continue, press 'OK', otherwise, press 'Cancel'"):
			self.showAnswers()

	# Get the questions from the csv file and lay them out with radiobuttons.
	def getTestQuestions(self):

		# Open the test csv file
		with open("tests/formative/CMT001/" + selectedTest) as test_file:
			test_reader = csv.reader(test_file, delimiter=',')

			# Count the number of questions in the csv file
			self.questionCount = 0

			#QUESTION 1
			try:
				Q1 = next(test_reader)
				self.questionCount += 1
				self.question1 = Q1[1]
				self.correctAnswer1 = Q1[2]

				answers = []
				answers.append(Q1[2])
				answers.append(Q1[3])
				answers.append(Q1[4])
				answers.append(Q1[5])
				random.shuffle(answers)

				lblQuestion1 = Label(self, text="1. " + self.question1, font=('verdana', 12, 'normal'), wraplength=400, justify=LEFT)
				lblQuestion1.grid(row=3, column=0, columnspan=4, padx=(30,20), pady=(20,10), sticky=W)

				self.varQuestion1 = StringVar(value=0)

				Q1R1 = Radiobutton(self, variable=self.varQuestion1, value=answers[0])
				Q1R1.grid(row=4, column=0, sticky=E)

				self.lblQ1A1 = Label(self, text=answers[0], font=('verdana', 12, 'normal'), anchor=W)
				self.lblQ1A1.grid(row=4, column=1, sticky=W)

				Q1R2 = Radiobutton(self, variable=self.varQuestion1, value=answers[1])
				Q1R2.grid(row=5, column=0, sticky=E)

				self.lblQ1A2 = Label(self, text=answers[1], font=('verdana', 12, 'normal'))
				self.lblQ1A2.grid(row=5, column=1, sticky=W)

				Q1R3 = Radiobutton(self, variable=self.varQuestion1, value=answers[2])
				Q1R3.grid(row=4, column=2, sticky=E)

				self.lblQ1A3 = Label(self, text=answers[2], font=('verdana', 12, 'normal'))
				self.lblQ1A3.grid(row=4, column=3, sticky=W)

				Q1R4 = Radiobutton(self, variable=self.varQuestion1, value=answers[3])
				Q1R4.grid(row=5, column=2, sticky=E)

				self.lblQ1A4 = Label(self, text=answers[3], font=('verdana', 12, 'normal'))
				self.lblQ1A4.grid(row=5, column=3, sticky=W)

			except StopIteration:
				pass


			#QUESTION 2
			try:
				Q2 = next(test_reader)
				self.questionCount += 1
				self.question2 = Q2[1]
				self.correctAnswer2 = Q2[2]

				answers = []
				answers.append(Q2[2])
				answers.append(Q2[3])
				answers.append(Q2[4])
				answers.append(Q2[5])
				random.shuffle(answers)


				lblQuestion2 = Label(self, text="2. " + self.question2, font=('verdana', 12, 'normal'), wraplength=400, justify=LEFT)
				lblQuestion2.grid(row=6, column=0, columnspan=4, padx=(30,20), pady=(20,10), sticky=W)

				self.varQuestion2 = StringVar(value=0)

				Q2R1 = Radiobutton(self, variable=self.varQuestion2, value=answers[0])
				Q2R1.grid(row=7, column=0, sticky=E)

				self.lblQ2A1 = Label(self, text=answers[0], font=('verdana', 12, 'normal'))
				self.lblQ2A1.grid(row=7, column=1, sticky=W)

				Q2R2 = Radiobutton(self, variable=self.varQuestion2, value=answers[1])
				Q2R2.grid(row=8, column=0, sticky=E)

				self.lblQ2A2 = Label(self, text=answers[1], font=('verdana', 12, 'normal'))
				self.lblQ2A2.grid(row=8, column=1, sticky=W)

				Q2R3 = Radiobutton(self, variable=self.varQuestion2, value=answers[2])
				Q2R3.grid(row=7, column=2, sticky=E)

				self.lblQ2A3 = Label(self, text=answers[2], font=('verdana', 12, 'normal'))
				self.lblQ2A3.grid(row=7, column=3, sticky=W)

				Q2R4 = Radiobutton(self, variable=self.varQuestion2, value=answers[3])
				Q2R4.grid(row=8, column=2, sticky=E)

				self.lblQ2A4 = Label(self, text=answers[3], font=('verdana', 12, 'normal'))
				self.lblQ2A4.grid(row=8, column=3, sticky=W)

			except StopIteration:
				pass

			#QUESTION 3
			try:
				Q3 = next(test_reader)
				self.questionCount += 1
				self.question3 = Q3[1]
				self.correctAnswer3 = Q3[2]

				answers = []
				answers.append(Q3[2])
				answers.append(Q3[3])
				answers.append(Q3[4])
				answers.append(Q3[5])
				random.shuffle(answers)

				lblQuestion3 = Label(self, text="3. " + self.question3, font=('verdana', 12, 'normal'), wraplength=400, justify=LEFT)
				lblQuestion3.grid(row=9, column=0, columnspan=4, padx=(30,20), pady=(20,10), sticky=W)

				self.varQuestion3 = StringVar(value=0)

				Q3R1 = Radiobutton(self, variable=self.varQuestion3, value=answers[0])
				Q3R1.grid(row=10, column=0, sticky=E)

				self.lblQ3A1 = Label(self, text=answers[0], font=('verdana', 12, 'normal'))
				self.lblQ3A1.grid(row=10, column=1, sticky=W)

				Q3R2 = Radiobutton(self, variable=self.varQuestion3, value=answers[1])
				Q3R2.grid(row=11, column=0, sticky=E)

				self.lblQ3A2 = Label(self, text=answers[1], font=('verdana', 12, 'normal'))
				self.lblQ3A2.grid(row=11, column=1, sticky=W)

				Q3R3 = Radiobutton(self, variable=self.varQuestion3, value=answers[2])
				Q3R3.grid(row=10, column=2, sticky=E)

				self.lblQ3A3 = Label(self, text=answers[2], font=('verdana', 12, 'normal'))
				self.lblQ3A3.grid(row=10, column=3, sticky=W)

				Q3R4 = Radiobutton(self, variable=self.varQuestion3, value=answers[3])
				Q3R4.grid(row=11, column=2, sticky=E)

				self.lblQ3A4 = Label(self, text=answers[3], font=('verdana', 12, 'normal'))
				self.lblQ3A4.grid(row=11, column=3, sticky=W)

			except StopIteration:
				pass

			#QUESTION 4
			try:
				Q4 = next(test_reader)
				self.questionCount += 1
				self.question4 = Q4[1]
				self.correctAnswer4 = Q4[2]

				answers = []
				answers.append(Q4[2])
				answers.append(Q4[3])
				answers.append(Q4[4])
				answers.append(Q4[5])
				random.shuffle(answers)

				lblQuestion4 = Label(self, text="4. " + self.question4, font=('verdana', 12, 'normal'), wraplength=400, justify=LEFT)
				lblQuestion4.grid(row=12, column=0, columnspan=4, padx=(30,20), pady=(20,10), sticky=W)

				self.varQuestion4 = StringVar(value=0)

				Q4R1 = Radiobutton(self, variable=self.varQuestion4, value=answers[0])
				Q4R1.grid(row=13, column=0, sticky=E)

				self.lblQ4A1 = Label(self, text=answers[0], font=('verdana', 12, 'normal'))
				self.lblQ4A1.grid(row=13, column=1, sticky=W)

				Q4R2 = Radiobutton(self, variable=self.varQuestion4, value=answers[1])
				Q4R2.grid(row=14, column=0, sticky=E)

				self.lblQ4A2 = Label(self, text=answers[1], font=('verdana', 12, 'normal'))
				self.lblQ4A2.grid(row=14, column=1, sticky=W)

				Q4R3 = Radiobutton(self, variable=self.varQuestion4, value=answers[2])
				Q4R3.grid(row=13, column=2, sticky=E)

				self.lblQ4A3 = Label(self, text=answers[2], font=('verdana', 12, 'normal'))
				self.lblQ4A3.grid(row=13, column=3, sticky=W)

				Q4R4 = Radiobutton(self, variable=self.varQuestion4, value=answers[3])
				Q4R4.grid(row=14, column=2, sticky=E)

				self.lblQ4A4 = Label(self, text=answers[3], font=('verdana', 12, 'normal'))
				self.lblQ4A4.grid(row=14, column=3, sticky=W)

			except StopIteration:
				pass

			#QUESTION 5
			try:
				Q5 = next(test_reader)
				self.questionCount += 1
				self.question5 = Q5[1]
				self.correctAnswer5 = Q5[2]

				answers = []
				answers.append(Q5[2])
				answers.append(Q5[3])
				answers.append(Q5[4])
				answers.append(Q5[5])
				random.shuffle(answers)

				lblQuestion5 = Label(self, text="5. " + self.question5, font=('verdana', 12, 'normal'), wraplength=400, justify=LEFT)
				lblQuestion5.grid(row=15, column=0, columnspan=4, padx=(30,20), pady=(20,10), sticky=W)

				self.varQuestion5 = StringVar(value=0)

				Q5R1 = Radiobutton(self, variable=self.varQuestion5, value=answers[0])
				Q5R1.grid(row=16, column=0, sticky=E)

				self.lblQ5A1 = Label(self, text=answers[0], font=('verdana', 12, 'normal'))
				self.lblQ5A1.grid(row=16, column=1, sticky=W)

				Q5R2 = Radiobutton(self, variable=self.varQuestion5, value=answers[1])
				Q5R2.grid(row=17, column=0, sticky=E)

				self.lblQ5A2 = Label(self, text=answers[1], font=('verdana', 12, 'normal'))
				self.lblQ5A2.grid(row=17, column=1, sticky=W)

				Q5R3 = Radiobutton(self, variable=self.varQuestion5, value=answers[2])
				Q5R3.grid(row=16, column=2, sticky=E)

				self.lblQ5A3 = Label(self, text=answers[2], font=('verdana', 12, 'normal'))
				self.lblQ5A3.grid(row=16, column=3, sticky=W)

				Q5R4 = Radiobutton(self, variable=self.varQuestion5, value=answers[3])
				Q5R4.grid(row=17, column=2, sticky=E)

				self.lblQ5A4 = Label(self, text=answers[3], font=('verdana', 12, 'normal'))
				self.lblQ5A4.grid(row=17, column=3, sticky=W)

			except StopIteration:
				pass

			#QUESTION 6
			try:
				Q6 = next(test_reader)
				self.questionCount += 1
				self.question6 = Q6[1]
				self.correctAnswer6 = Q6[2]

				answers = []
				answers.append(Q6[2])
				answers.append(Q6[3])
				answers.append(Q6[4])
				answers.append(Q6[5])
				random.shuffle(answers)

				lblQuestion6 = Label(self, text="6. " + self.question6, font=('verdana', 12, 'normal'), wraplength=400, justify=LEFT)
				lblQuestion6.grid(row=3, column=4, columnspan=4, padx=(30,20), pady=(20,10), sticky=W)

				self.varQuestion6 = StringVar(value=0)

				Q6R1 = Radiobutton(self, variable=self.varQuestion6, value=answers[0])
				Q6R1.grid(row=4, column=4, sticky=E)

				self.lblQ6A1 = Label(self, text=answers[0], font=('verdana', 12, 'normal'))
				self.lblQ6A1.grid(row=4, column=5, sticky=W)

				Q6R2 = Radiobutton(self, variable=self.varQuestion6, value=answers[1])
				Q6R2.grid(row=5, column=4, sticky=E)

				self.lblQ6A2 = Label(self, text=answers[1], font=('verdana', 12, 'normal'))
				self.lblQ6A2.grid(row=5, column=5, sticky=W)

				Q6R3 = Radiobutton(self, variable=self.varQuestion6, value=answers[2])
				Q6R3.grid(row=4, column=6, sticky=E)

				self.lblQ6A3 = Label(self, text=answers[2], font=('verdana', 12, 'normal'))
				self.lblQ6A3.grid(row=4, column=7, sticky=W)

				Q6R4 = Radiobutton(self, variable=self.varQuestion6, value=answers[3])
				Q6R4.grid(row=5, column=6, sticky=E)

				self.lblQ6A4 = Label(self, text=answers[3], font=('verdana', 12, 'normal'))
				self.lblQ6A4.grid(row=5, column=7, sticky=W)

			except StopIteration:
				pass

			#QUESTION 7
			try:
				Q7 = next(test_reader)
				self.questionCount += 1
				self.question7 = Q7[1]
				self.correctAnswer7 = Q7[2]

				answers = []
				answers.append(Q7[2])
				answers.append(Q7[3])
				answers.append(Q7[4])
				answers.append(Q7[5])
				random.shuffle(answers)

				lblQuestion7 = Label(self, text="7. " + self.question7, font=('verdana', 12, 'normal'), wraplength=400, justify=LEFT)
				lblQuestion7.grid(row=6, column=4, columnspan=4, padx=(30,20), pady=(20,10), sticky=W)

				self.varQuestion7 = StringVar(value=0)

				Q7R1 = Radiobutton(self, variable=self.varQuestion7, value=answers[0])
				Q7R1.grid(row=7, column=4, sticky=E)

				self.lblQ7A1 = Label(self, text=answers[0], font=('verdana', 12, 'normal'))
				self.lblQ7A1.grid(row=7, column=5, sticky=W)

				Q7R2 = Radiobutton(self, variable=self.varQuestion7, value=answers[1])
				Q7R2.grid(row=8, column=4, sticky=E)

				self.lblQ7A2 = Label(self, text=answers[1], font=('verdana', 12, 'normal'))
				self.lblQ7A2.grid(row=8, column=5, sticky=W)

				Q7R3 = Radiobutton(self, variable=self.varQuestion7, value=answers[2])
				Q7R3.grid(row=7, column=6, sticky=E)

				self.lblQ7A3 = Label(self, text=answers[2], font=('verdana', 12, 'normal'))
				self.lblQ7A3.grid(row=7, column=7, sticky=W)

				Q7R4 = Radiobutton(self, variable=self.varQuestion7, value=answers[3])
				Q7R4.grid(row=8, column=6, sticky=E)

				self.lblQ7A4 = Label(self, text=answers[3], font=('verdana', 12, 'normal'))
				self.lblQ7A4.grid(row=8, column=7, sticky=W)

			except StopIteration:
				pass

			#QUESTION 8
			try:
				Q8 = next(test_reader)
				self.questionCount += 1
				self.question8 = Q8[1]
				self.correctAnswer8 = Q8[2]

				answers = []
				answers.append(Q8[2])
				answers.append(Q8[3])
				answers.append(Q8[4])
				answers.append(Q8[5])
				random.shuffle(answers)

				lblQuestion8 = Label(self, text="8. " + self.question8, font=('verdana', 12, 'normal'), wraplength=400, justify=LEFT)
				lblQuestion8.grid(row=9, column=4, columnspan=4, padx=(30,20), pady=(20,10), sticky=W)

				self.varQuestion8 = StringVar(value=0)

				Q8R1 = Radiobutton(self, variable=self.varQuestion8, value=answers[0])
				Q8R1.grid(row=10, column=4, sticky=E)

				self.lblQ8A1 = Label(self, text=answers[0], font=('verdana', 12, 'normal'))
				self.lblQ8A1.grid(row=10, column=5, sticky=W)

				Q8R2 = Radiobutton(self, variable=self.varQuestion8, value=answers[1])
				Q8R2.grid(row=11, column=4, sticky=E)

				self.lblQ8A2 = Label(self, text=answers[1], font=('verdana', 12, 'normal'))
				self.lblQ8A2.grid(row=11, column=5, sticky=W)

				Q8R3 = Radiobutton(self, variable=self.varQuestion8, value=answers[2])
				Q8R3.grid(row=10, column=6, sticky=E)

				self.lblQ8A3 = Label(self, text=answers[2], font=('verdana', 12, 'normal'))
				self.lblQ8A3.grid(row=10, column=7, sticky=W)

				Q8R4 = Radiobutton(self, variable=self.varQuestion8, value=answers[3])
				Q8R4.grid(row=11, column=6, sticky=E)

				self.lblQ8A4 = Label(self, text=answers[3], font=('verdana', 12, 'normal'))
				self.lblQ8A4.grid(row=11, column=7, sticky=W)

			except StopIteration:
				pass

			#QUESTION 9
			try:
				Q9 = next(test_reader)
				self.questionCount += 1
				self.question9 = Q9[1]
				self.correctAnswer9 = Q9[2]

				answers = []
				answers.append(Q9[2])
				answers.append(Q9[3])
				answers.append(Q9[4])
				answers.append(Q9[5])
				random.shuffle(answers)

				lblQuestion9 = Label(self, text="9. " + self.question9, font=('verdana', 12, 'normal'), wraplength=400, justify=LEFT)
				lblQuestion9.grid(row=12, column=4, columnspan=4, padx=(30,20), pady=(20,10), sticky=W)

				self.varQuestion9 = StringVar(value=0)

				Q9R1 = Radiobutton(self, variable=self.varQuestion9, value=answers[0])
				Q9R1.grid(row=13, column=4, sticky=E)

				self.lblQ9A1 = Label(self, text=answers[0], font=('verdana', 12, 'normal'))
				self.lblQ9A1.grid(row=13, column=5, sticky=W)

				Q9R2 = Radiobutton(self, variable=self.varQuestion9, value=answers[1])
				Q9R2.grid(row=14, column=4, sticky=E)

				self.lblQ9A2 = Label(self, text=answers[1], font=('verdana', 12, 'normal'))
				self.lblQ9A2.grid(row=14, column=5, sticky=W)

				Q9R3 = Radiobutton(self, variable=self.varQuestion9, value=answers[2])
				Q9R3.grid(row=13, column=6, sticky=E)

				self.lblQ9A3 = Label(self, text=answers[2], font=('verdana', 12, 'normal'))
				self.lblQ9A3.grid(row=13, column=7, sticky=W)

				Q9R4 = Radiobutton(self, variable=self.varQuestion9, value=answers[3])
				Q9R4.grid(row=14, column=6, sticky=E)

				self.lblQ9A4 = Label(self, text=answers[3], font=('verdana', 12, 'normal'))
				self.lblQ9A4.grid(row=14, column=7, sticky=W)

			except StopIteration:
				pass

			#QUESTION 10
			try:
				Q10 = next(test_reader)
				self.questionCount += 1
				self.question10 = Q10[1]
				self.correctAnswer10 = Q10[2]

				answers = []
				answers.append(Q10[2])
				answers.append(Q10[3])
				answers.append(Q10[4])
				answers.append(Q10[5])
				random.shuffle(answers)

				lblQuestion10 = Label(self, text="10. " + self.question10, font=('verdana', 12, 'normal'), wraplength=400, justify=LEFT)
				lblQuestion10.grid(row=15, column=4, columnspan=4, padx=(30,20), pady=(20,10), sticky=W)

				self.varQuestion10 = StringVar(value=0)

				Q10R1 = Radiobutton(self, variable=self.varQuestion10, value=answers[0])
				Q10R1.grid(row=16, column=4, sticky=E)

				self.lblQ10A1 = Label(self, text=answers[0], font=('verdana', 12, 'normal'))
				self.lblQ10A1.grid(row=16, column=5, sticky=W)

				Q10R2 = Radiobutton(self, variable=self.varQuestion10, value=answers[1])
				Q10R2.grid(row=17, column=4, sticky=E)

				self.lblQ10A2 = Label(self, text=answers[1], font=('verdana', 12, 'normal'))
				self.lblQ10A2.grid(row=17, column=5, sticky=W)

				Q10R3 = Radiobutton(self, variable=self.varQuestion10, value=answers[2])
				Q10R3.grid(row=16, column=6, sticky=E)

				self.lblQ10A3 = Label(self, text=answers[2], font=('verdana', 12, 'normal'))
				self.lblQ10A3.grid(row=16, column=7, sticky=W)

				Q10R4 = Radiobutton(self, variable=self.varQuestion10, value=answers[3])
				Q10R4.grid(row=17, column=6, sticky=E)

				self.lblQ10A4 = Label(self, text=answers[3], font=('verdana', 12, 'normal'))
				self.lblQ10A4.grid(row=17, column=7, sticky=W)

			except StopIteration:
				pass

			# Test submit button
			self.buttonSubmit = Button(self, text='Submit', font=('verdana', 12, 'normal'), width=10, height=2)
			self.buttonSubmit.grid(row=18, column=7, padx=20, pady=20, sticky=SE)
			self.buttonSubmit['command']=self.storeResponse

			# If test has been completed before, show the answers immediately
			for i in self.testsDone:
				if i == selectedTest:
					self.showAnswers()

	# This function checks the selected answers, stores their response calculates the user's score
	def storeResponse(self):
		# If the submit button is pressed when the limit is reached, alert the user the immediately show them the correct answers
		if self.attempts >= 3:
			tkinter.messagebox.showinfo("Limit Reached", "You have reached your limit of attempts for this test.")
			self.showAnswers()
		
		else:
			# Initialise the user's score to 0
			score = 0

			# Assign an empty string to each answer in case there are fewer than 10 questions in the test
			q1Answer = "x"
			q1Result = "x"
			q2Answer = "x"
			q2Result = "x"
			q3Answer = "x"
			q3Result = "x"
			q4Answer = "x"
			q4Result = "x"
			q5Answer = "x"
			q5Result = "x"
			q6Answer = "x"
			q6Result = "x"
			q7Answer = "x"
			q7Result = "x"
			q8Answer = "x"
			q8Result = "x"
			q9Answer = "x"
			q9Result = "x"
			q10Answer = "x"
			q10Result = "x"

			# For each question, if the user has selected the correct answer then add 1 to the score for that attempt
			try:
				#QUESTION 1 RESPONSE
				q1Answer = self.varQuestion1.get()
				q1CorrectAnswer = self.correctAnswer1

				if q1Answer == q1CorrectAnswer:
					score += 1
					q1Result = "correct"
				else:
					q1Result = "incorrect"

				#QUESTION 2 RESPONSE
				q2Answer = self.varQuestion2.get()
				q2CorrectAnswer = self.correctAnswer2

				if q2Answer == q2CorrectAnswer:
					score += 1
					q2Result = "correct"
				else:
					q2Result = "incorrect"

				#QUESTION 3 RESPONSE
				q3Answer = self.varQuestion3.get()
				q3CorrectAnswer = self.correctAnswer3

				if q3Answer == q3CorrectAnswer:
					score += 1
					q3Result = "correct"
				else:
					q3Result = "incorrect"

				#QUESTION 4 RESPONSE
				q4Answer = self.varQuestion4.get()
				q4CorrectAnswer = self.correctAnswer4

				if q4Answer == q4CorrectAnswer:
					score += 1
					q4Result = "correct"
				else:
					q4Result = "incorrect"

				#QUESTION 5 RESPONSE
				q5Answer = self.varQuestion5.get()
				q5CorrectAnswer = self.correctAnswer5

				if q5Answer == q5CorrectAnswer:
					score += 1
					q5Result = "correct"
				else:
					q5Result = "incorrect"

				#QUESTION 6 RESPONSE
				q6Answer = self.varQuestion6.get()
				q6CorrectAnswer = self.correctAnswer6

				if q6Answer == q6CorrectAnswer:
					score += 1
					q6Result = "correct"
				else:
					q6Result = "incorrect"

				#QUESTION 7 RESPONSE
				q7Answer = self.varQuestion7.get()
				q7CorrectAnswer = self.correctAnswer7

				if q7Answer == q7CorrectAnswer:
					score += 1
					q7Result = "correct"
				else:
					q7Result = "incorrect"

				#QUESTION 8 RESPONSE
				q8Answer = self.varQuestion8.get()
				q8CorrectAnswer = self.correctAnswer8

				if q8Answer == q8CorrectAnswer:
					score += 1
					q8Result = "correct"
				else:
					q8Result = "incorrect"

				#QUESTION 9 RESPONSE
				q9Answer = self.varQuestion9.get()
				q9CorrectAnswer = self.correctAnswer9

				if q9Answer == q9CorrectAnswer:
					score += 1
					q9Result = "correct"
				else:
					q9Result = "incorrect"

				#QUESTION 10 RESPONSE
				q10Answer = self.varQuestion10.get()
				q10CorrectAnswer = self.correctAnswer10

				if q10Answer == q10CorrectAnswer:
					score += 1
					q10Result = "correct"
				else:
					q10Result = "incorrect"

			except AttributeError:
				pass

			#Save the score of each attempt
			if self.attempts == 0:
				self.buttonSeeAnswers['state'] = 'normal'
				global attempt1Score
				attempt1Score += score
				global allAttempts
				allAttempts.append(score)

			elif self.attempts == 1:
				global attempt2Score
				attempt2Score += score
				allAttempts.append(score)

			elif self.attempts == 2:
				global attempt3Score
				attempt3Score += score
				allAttempts.append(score)

			# Check that the user has selected an answer to every question
			if q1Answer == "0" or q2Answer == "0" or q3Answer == "0" or q4Answer == "0" or q5Answer == "0" or q6Answer == "0" or q7Answer == "0" or q8Answer == "0" or q9Answer == "0" or q10Answer == "0":
				tkinter.messagebox.showinfo("Error", "Please select an answer for every quesion")

			# If the user has scored less than full marks show them their score
			elif score < self.questionCount:
				score = str(score)
				questionCount = str(self.questionCount)
				tkinter.messagebox.showinfo("Result", "You scored " + score + " out of " + questionCount + ".")
				
				# Save their score to the results csv
				attemptNo = self.attempts
				attemptNoForStats = attemptNo
				attemptNoForStats += 1

				global selectedTest

				with open ("./results/formative/" + selectedTest, mode="a") as results_csv:
					results_writer = csv.writer(results_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
					results_writer.writerow([self.userNumber, attemptNoForStats, score, q1Result, q2Result, q3Result, q4Result, q5Result, q6Result, q7Result, q8Result, q9Result, q10Result])
				
				# Add one to the number of attempts
				self.attempts += 1

				# Update the attempts label
				if self.attempts == 1:
					self.lblAttempts['text'] = "You have 3 attempts. So far you have made " + str(self.attempts) + " attempt."
				else:
					self.lblAttempts['text'] = "You have 3 attempts. So far you have made " + str(self.attempts) + " attempts."

				highestScore = max(allAttempts)
				self.lblHighestScore['text'] = "Your highest score: " + str(highestScore)

				# If the user has already attempted three times, show the correct answer
				if self.attempts == 3:
					self.showAnswers()

			# If the user has scored full marks show them their score
			else:
				score = str(score)
				questionCount = str(self.questionCount)
				tkinter.messagebox.showinfo("Result", "Congratulations, you scored " + score + " out of " + questionCount + "!")
				
				# Save their score to the results csv
				attemptNo = self.attempts
				attemptNoForStats = attemptNo
				attemptNoForStats += 1

				with open ("./results/formative/" + selectedTest, mode="a") as results_csv:
					results_writer = csv.writer(results_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
					results_writer.writerow([self.userNumber, attemptNoForStats, score, q1Result, q2Result, q3Result, q4Result, q5Result, q6Result, q7Result, q8Result, q9Result, q10Result])
				
				# Add one to the number of attempts
				self.attempts += 1

				# Update the attempts label
				self.lblAttempts['text'] = "Well done, you answered all questions correctly in " + str(self.attempts) + " attempts."

				highestScore = max(allAttempts)

				# Update the highest score label
				self.lblHighestScore['text'] = "Your highest score: " + str(highestScore)

				# Show the correct answers
				self.showAnswers()

	#Close the test window
	def closeWindow(self):
		self.master.destroy()

	#after 3 attempts or all correct show the correct answers in green.
	def showAnswers(self):
		# Disable the 'Show Answers' button
		self.buttonSeeAnswers['state'] = 'disabled'

		# Disable the 'Submit' button
		self.buttonSubmit['state'] = 'disabled'

		# Update the attempts label
		if self.attempts == 1:
			self.lblAttempts['text'] = "You completed the test in " + str(self.attempts) + " attempt."
		else:
			self.lblAttempts['text'] = "You completed the test in " + str(self.attempts) + " attempts."
		
		# Note in the text file that this test has been completed
		completedTest = selectedTest + ","
		with open("./users/userloggedin.txt", 'a') as text_file:
			text_file.write(completedTest)

		try:
			#Question 1 - show correct answer
			if self.lblQ1A1['text'] == self.correctAnswer1:
				self.lblQ1A1['fg']="green"
			elif self.lblQ1A2['text'] == self.correctAnswer1:
				self.lblQ1A2['fg']='green'
			elif self.lblQ1A3['text'] == self.correctAnswer1:
				self.lblQ1A3['fg']="green"
			elif self.lblQ1A4['text'] == self.correctAnswer1:
				self.lblQ1A4['fg']="green"

			#Question 2 - show correct answer
			if self.lblQ2A1['text'] == self.correctAnswer2:
				self.lblQ2A1['fg']="green"
			elif self.lblQ2A2['text'] == self.correctAnswer2:
				self.lblQ2A2['fg']='green'
			elif self.lblQ2A3['text'] == self.correctAnswer2:
				self.lblQ2A3['fg']="green"
			elif self.lblQ2A4['text'] == self.correctAnswer2:
				self.lblQ2A4['fg']="green"

			#Question 3 - show correct answer
			if self.lblQ3A1['text'] == self.correctAnswer3:
				self.lblQ3A1['fg']="green"
			elif self.lblQ3A2['text'] == self.correctAnswer3:
				self.lblQ3A2['fg']='green'
			elif self.lblQ3A3['text'] == self.correctAnswer3:
				self.lblQ3A3['fg']="green"
			elif self.lblQ3A4['text'] == self.correctAnswer3:
				self.lblQ3A4['fg']="green"

			#Question 4 - show correct answer
			if self.lblQ4A1['text'] == self.correctAnswer4:
				self.lblQ4A1['fg']="green"
			elif self.lblQ4A2['text'] == self.correctAnswer4:
				self.lblQ4A2['fg']='green'
			elif self.lblQ4A3['text'] == self.correctAnswer4:
				self.lblQ4A3['fg']="green"
			elif self.lblQ4A4['text'] == self.correctAnswer4:
				self.lblQ4A4['fg']="green"

			#Question 5 - show correct answer
			if self.lblQ5A1['text'] == self.correctAnswer5:
				self.lblQ5A1['fg']="green"
			elif self.lblQ5A2['text'] == self.correctAnswer5:
				self.lblQ5A2['fg']='green'
			elif self.lblQ5A3['text'] == self.correctAnswer5:
				self.lblQ5A3['fg']="green"
			elif self.lblQ5A4['text'] == self.correctAnswer5:
				self.lblQ5A4['fg']="green"

			#Question 6 - show correct answer
			if self.lblQ6A1['text'] == self.correctAnswer6:
				self.lblQ6A1['fg']="green"
			elif self.lblQ6A2['text'] == self.correctAnswer6:
				self.lblQ6A2['fg']='green'
			elif self.lblQ6A3['text'] == self.correctAnswer6:
				self.lblQ6A3['fg']="green"
			elif self.lblQ6A4['text'] == self.correctAnswer6:
				self.lblQ6A4['fg']="green"

			#Question 7 - show correct answer
			if self.lblQ7A1['text'] == self.correctAnswer7:
				self.lblQ7A1['fg']="green"
			elif self.lblQ7A2['text'] == self.correctAnswer7:
				self.lblQ7A2['fg']='green'
			elif self.lblQ7A3['text'] == self.correctAnswer7:
				self.lblQ7A3['fg']="green"
			elif self.lblQ7A4['text'] == self.correctAnswer7:
				self.lblQ7A4['fg']="green"

				#Question 8 - show correct answer
			if self.lblQ8A1['text'] == self.correctAnswer8:
				self.lblQ8A1['fg']="green"
			elif self.lblQ8A2['text'] == self.correctAnswer8:
				self.lblQ8A2['fg']='green'
			elif self.lblQ8A3['text'] == self.correctAnswer8:
				self.lblQ8A3['fg']="green"
			elif self.lblQ8A4['text'] == self.correctAnswer8:
				self.lblQ8A4['fg']="green"

			#Question 9 - show correct answer
			if self.lblQ9A1['text'] == self.correctAnswer9:
				self.lblQ9A1['fg']="green"
			elif self.lblQ9A2['text'] == self.correctAnswer9:
				self.lblQ9A2['fg']='green'
			elif self.lblQ9A3['text'] == self.correctAnswer9:
				self.lblQ9A3['fg']="green"
			elif self.lblQ9A4['text'] == self.correctAnswer9:
				self.lblQ9A4['fg']="green"

			#Question 10 - show correct answer
			if self.lblQ10A1['text'] == self.correctAnswer10:
				self.lblQ10A1['fg']="green"
			elif self.lblQ10A2['text'] == self.correctAnswer10:
				self.lblQ10A2['fg']='green'
			elif self.lblQ10A3['text'] == self.correctAnswer10:
				self.lblQ10A3['fg']="green"
			elif self.lblQ10A4['text'] == self.correctAnswer10:
				self.lblQ10A4['fg']="green"

		except AttributeError:
			pass
