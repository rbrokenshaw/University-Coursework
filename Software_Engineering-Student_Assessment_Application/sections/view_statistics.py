
#Importing all the required packages.

import tkinter as tk
import os, re
import tkinter.messagebox
import os.path
import pandas as pd
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#Setting up the statitistics frame.

class ViewStatistics(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.viewstats()
        
    #Check the formative results folder for test results and put them in a list.

    def viewstats(self):
        lblTestTitle = tk.Label(self, text='Statistics for Formative Tests', font=('Courier New', 25, 'bold'), fg='firebrick3')
        lblTestTitle.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky=tk.N)
        
        lblTestTitle = tk.Label(self, text='Please select the test you would like to view the statistics of:', font=('verdana', 12, 'normal'))
        lblTestTitle.grid(row=2, column=0, columnspan=3, padx=100, pady=(0,10), sticky=tk.N)

        self.testList = os.listdir("tests/formative/CMT001/")    
        self.testListBox = tk.Listbox(self, width=30)
        self.testListBox.grid(row=3, column=1, sticky=tk.N)

        for i in self.testList:
            i = re.sub(".csv", "", i)
            self.testListBox.insert(tk.END, i)
            
        #The options buttons. E.g. view the selected stats and view comparrison page.

        buttonstatMenu = tk.Button(self, text="View statistics for selected test", font=('verdana', 12, 'normal'), width=30, height=2)
        buttonstatMenu['command']=self.openTeststats
        buttonstatMenu.grid(row=5, column=1, padx=20, pady=(20, 5), sticky=tk.N)
        
        buttonstatMenu = tk.Button(self, text="View comparison of all tests taken", font=('verdana', 12, 'normal'), width=30, height=2)        
        buttonstatMenu['command']=self.opencomp
        buttonstatMenu.grid(row=6, column=1, padx=20, pady=(5, 20), sticky=tk.N)

        buttonstatMenu = tk.Button(self, text="Return To Main Menu", font=('verdana', 12, 'normal'), width=20, height=2)
        buttonstatMenu['command']=self.openMainMenu
        buttonstatMenu.grid(row=7, column=1, padx=20, pady=5, sticky=tk.N)

        buttonstatMenu = tk.Button(self, text="Exit", font=('verdana', 12, 'normal'), width=8, height=2)
        buttonstatMenu['command']=self.exitSystem
        buttonstatMenu.grid(row=8, column=1, padx=20, pady=5, sticky=tk.N)        
        
#Open the results selected test in another frame.
        
    def openTeststats(self):
        testBoxSelection = (self.testListBox.curselection())
        try:
            testBoxSelection = testBoxSelection[0]
            global selectedTest
            selectedTest = self.testList[testBoxSelection]
            
            if os.path.isfile("./results/formative/" + selectedTest):
                self.newWindow = tk.Toplevel(self.master)
                self.app = statdisplay(self.newWindow)
                                
            else:
                tkinter.messagebox.showinfo("Error", "There are no statistics for this test")           
        
        except IndexError:
            tkinter.messagebox.showinfo("Error", "Please select a test from the list")
            
    def opencomp(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = testcomp(self.newWindow)

    #Returns user to main menu.

    def openMainMenu(self):
        self.master.destroy()
        
    #Exits the system

    def exitSystem(self):
        if tkinter.messagebox.askokcancel("Quit", "Are you sure you wish to exit the system?"):
            self.quit()
   
class testcomp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.dispcomp()

    def dispcomp(self):
        lblTestTitle = tk.Label(self, text='Comparison Page', font=('Courier New', 25, 'bold'), fg='firebrick3')
        lblTestTitle.grid(row=0, column=0, columnspan=12, padx=10, pady=10, sticky=tk.N)    
        
        lblTestTitle = tk.Label(self, text='This Page displays a comparison of all tests that have been taken.', font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=1, column=0, columnspan=12, padx=10, pady=10, sticky=tk.N)

        path = './results/formative/'

        folder = os.fsencode(path)
        
        #Setting up lists for the scores from each file and the file names.

        scores = []
        filenames = []

        for file in os.listdir(folder):
            filename = os.fsdecode(file)
            if filename.endswith('.csv'):
                filenames.append(filename)
                cf = pd.read_csv(path + filename)
                
                studnt = cf['Student Number']
                studlist = []
        
                for i in studnt:
                    if i not in studlist:
                        studlist.append(i)
                        
                #Set list for final score that will be appended to.
                        
                finalscore = []
        
                for i in studlist:
                    df4 = cf.loc[cf['Student Number'].isin([i])]
                    scr = df4['Score']
                    scr1 = list(scr)    
                    finscore = (scr1[-1])
                    finalscore.append(finscore)
                
                #Calculates the average score for that test then apprends it to the score list.
                
                avgfscoren = sum(finalscore)/len(finalscore)
                scores.append(avgfscoren)      
                
        # Calculates the current average for all tests.
                
        avgscores = sum(scores)/len(scores)
        strscravg = float('{0:.2f}'.format(avgscores))       
        scoretext = 'The current average score for all taken tests is: ' + str(strscravg) + ' (2dp)' 
        
        # Displays the average score of all tests taken.        
            
        lblTestTitle = tk.Label(self, text=scoretext, font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=50, column=0, columnspan=12, padx=10, pady=5, sticky=tk.N)  

        # Calculates the number of tets that currently have reults.
        
        numoftests = np.linspace(1,len(scores), len(scores))
        
        # Plotting graph of the average score per test. 
        
        f = Figure(figsize=(16,4), dpi=100)
        a = f.add_subplot(111)
        a.plot(numoftests, scores, 'ro' )
        a.plot(numoftests, scores, 'k-' )
        ticks = numoftests
        a.set_xticks(ticks)
        a.set_title('Average score for each test')
        a.set_xlabel('Test')
        a.set_ylabel('Average score')
        a.grid(True)
        a.set_ybound(0,11)
        a.set_xbound(0.9,len(filenames)+0.1)
        
        #Shortening the test names to just show the week on the graph.
        
        shortnames = []
        
        for file in filenames:
            short = file[:-4]
            shortnames.append(short)
            
        a.set_xticklabels(shortnames)        
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5,column=0,columnspan=6,rowspan=20)
        
        #Finding the higest and lowest avaerge score.
        
        lscore = min(scores)
        hscore = max(scores)        
        lscore1 = float('{0:.2f}'.format(lscore))
        hscore1 = float('{0:.2f}'.format(hscore))
        lscorestr = 'The lowest average test score is: ' + str(lscore1) + ' (2dp)'
        hscorestr = 'The highest average test score is: ' + str(hscore1) + ' (2dp)'
        trend = scores[-1] - scores[-2]
        trendf = abs(trend)
        trendf = float('{0:.2f}'.format(trendf))

        #Determine if the change between tests has been +ve or -ve and change updown accordingly.        
        
        if trend > 0:
            updown = 'increased by ' + str(trendf) + ' (2dp)'
        if trend < 0:
            updown = 'decreased by ' + str(trendf) + ' (2dp)'
        if trend == 0:
            updown = 'not changed'
            
        #Create string for use in label for the test trend.
        
        ctrend = 'The current average test score has ' + updown + ' since last the test.' 
        
        #Labels for high score, low score and change since last test.
        
        lblTestTitle = tk.Label(self, text=hscorestr, font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=51, column=0, columnspan=12, padx=10, pady=5, sticky=tk.N) 
        
        lblTestTitle = tk.Label(self, text=lscorestr, font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=52, column=0, columnspan=12, padx=10, pady=5, sticky=tk.N) 
        
        lblTestTitle = tk.Label(self, text=ctrend, font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=53, column=0, columnspan=12, padx=10, pady=5, sticky=tk.N) 
        
        #Exit buttons.   
        
        buttonstatMenu = tk.Button(self, text="Return To Statistics Menu", font=('verdana', 12, 'normal'), width=25, height=2)
        buttonstatMenu['command']=self.openMainMenu
        buttonstatMenu.grid(row=60, column=0, columnspan=12, padx=20, pady=5, sticky=tk.N)

        buttonstatMenu = tk.Button(self, text="Exit", font=('verdana', 12, 'normal'), width=8, height=2)
        buttonstatMenu['command']=self.exitSystem
        buttonstatMenu.grid(row=61, column=0, columnspan=12, padx=20, pady=5, sticky=tk.N)
        
    #Returns user to main menu.

    def openMainMenu(self):
        self.master.destroy()
        
    #Exits the system.

    def exitSystem(self):
        if tkinter.messagebox.askokcancel("Quit", "Are you sure you wish to exit the system?"):
            self.quit()
        
#This class displays the data for individual tests.
    
class statdisplay(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.dispstat()  
        
    def dispstat(self):
        
        #Removing the .csv from the end of the test name for the display.
        
        tittlew = selectedTest        
        tittlew = tittlew[:-4]       
        
        mentitle = 'Display Page for: ' + tittlew
        
        #Title label for this page.
        
        lblTestTitle = tk.Label(self, text=mentitle, font=('Courier New', 25, 'bold'), fg='firebrick3')
        lblTestTitle.grid(row=0, column=0, columnspan=12, padx=10, pady=5, sticky=tk.N)    
        
        #Setting some globals.
        
        global average, average2, average3, highscore1, highscore2, highscore3        
    
        #Reading the csv file into a dataframe.
    
        df = pd.read_csv('./results/formative/'+ selectedTest, sep=',') 
        
        #For the 1st attempt at the test.
        
        df1at = df.loc[df['Attempt No'].isin(['1'])]
        num = df1at['Score']
        summ = sum(num)
        length = len(num)
        
        if length == 0:
            average = 0
        else:
            average  = (summ/length)
        
        #For the 2nd attempt at the test.
        
        df2at = df.loc[df['Attempt No'].isin(['2'])]
        num2 = df2at['Score']
        summ2 = sum(num2)
        length2 = len(num2)        
        
        if length2 == 0:
            average2 = 0
        else:            
            average2  = (summ2/length2)           
              
        #For the 3rd attempt at the test.
        
        df3at = df.loc[df['Attempt No'].isin(['3'])]
        num3 = df3at['Score']
        summ3= sum(num3)
        length3 = len(num3)
        
        if length3 == 0:
            average3 = 0
        else:
            average3  = (summ3/length3)       
        
        #Graph for Average score vs attempts.
        
        g1 = Figure(figsize=(6,4), dpi=100)
        a = g1.add_subplot(111)
        avdata = [average, average2, average3]
        attempsss = list([1, 2, 3])        
        a.bar(attempsss, avdata)        
        a.set_xlabel('Number of Attempts')
        a.set_ylabel('Average Score')
        a.set_title('Average Score per Attempt')
        a.grid(True)
        a.set_ybound(0,11)
        tciks = ([1,2,3])
        a.set_xticks(tciks)        
        
        canvas = FigureCanvasTkAgg(g1, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2,column=0,columnspan=6,rowspan=20)
        
         #Highscores.
        
        #Highscore1.
        
        if length == 0:
            highscore1 = 0
        else:
            num1 = df1at['Score']
            highscore1 = max(num1)                   
        
        #Highscore2.
        
        if length2 == 0:
            highscore2 = 0
        else:
            num2 = df2at['Score']
            highscore2 = max(num2)       
        
        #Highscore3.
        
        if length3 == 0:
            highscore3 = 0
        else:
            num3 = df3at['Score']
            highscore3 = max(num3)       
        
        #Average number of attempts.
        
        attempts = length*1 + length2*2 + length3*3   
        totallength = length + length2 + length3
        avgatt = attempts/totallength
        attdp = float('{0:.2f}'.format(avgatt))        
        attout = 'The average number of attempts for the test is: ' + str(attdp) + ' (2dp)'    
        
        #Average number of attempts label.
        
        lblTestTitle = tk.Label(self, text=attout, font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=27, column=0, columnspan=12, padx=10, pady=5, sticky=tk.N)
        
        #Graph for highscore vs attempts.
        
        g2 = Figure(figsize=(6,4), dpi=100)
        a = g2.add_subplot(111)
        avdata = [highscore1, highscore2, highscore3]
        attempsss = list([1, 2, 3])
        a.bar(attempsss, avdata)
        a.set_xlabel('Number of Attempts')
        a.set_ylabel('High Score')
        a.set_title('High Score per Attempt')
        a.grid(True)
        a.set_ybound(0,11)
        a.set_xticks(tciks)
        
        canvas = FigureCanvasTkAgg(g2, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2,column=6,columnspan=3,rowspan=20)
        
        #Counter for the number of students that have taken the test.
        
        studnt = df['Student Number']
        studlist = []
        
        for i in studnt:
            if i not in studlist:
                studlist.append(i)
                
        lenstud = len(studlist)                
        numbstuds = 'The number of students that have taken this test is: ' + str(lenstud)
              
        #Number of students label.
        
        lblTestTitle = tk.Label(self, text=numbstuds, font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=23, column=0, columnspan=12, padx=10, pady=5, sticky=tk.N)
        
        #Calculating the average score from the last attempt submitted.
        
        finalscore = []
        
        for i in studlist:
            df4 = df.loc[df['Student Number'].isin([i])]
            scr = df4['Score']
            scr1 = list(scr)    
            finscore = (scr1[-1])
            finalscore.append(finscore)
         
        avgfscoren = sum(finalscore)/len(finalscore)
        avgfscore = float('{0:.2f}'.format(avgfscoren))
        avgfstr = 'The average score for this test is: ' + str(avgfscore) + ' (2dp)'
        
        #Label for the average score after last attempt.
        
        lblTestTitle = tk.Label(self, text=avgfstr, font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=28, column=0, columnspan=12, padx=10, pady=5, sticky=tk.N)       
        
        #Exit buttons.        
        
        buttonstatMenu = tk.Button(self, text="Return To Statistics Menu", font=('verdana', 12, 'normal'), width=25, height=2)
        buttonstatMenu['command']=self.openMainMenu
        buttonstatMenu.grid(row=31, column=0, columnspan=12, padx=20, pady=5, sticky=tk.N)

        buttonstatMenu = tk.Button(self, text="Exit", font=('verdana', 12, 'normal'), width=8, height=2)
        buttonstatMenu['command']=self.exitSystem
        buttonstatMenu.grid(row=32, column=0, columnspan=12, padx=20, pady=5, sticky=tk.N)
        
        #Question Counter.
    
        bf = pd.read_csv('./results/formative/'+ selectedTest, sep=',')
   
        #Question Counter.
    
        anscount = []
        question = []
        numbers = np.linspace(1,10,10)
    
        for n in numbers:
            strnu = 'q' + str(int(n))   
            frame = bf[strnu+'Answer']
            counter = 0
            for i in frame:
                if i == 'correct':
                    counter +=1
                if i == 'incorrect':
                    counter +=0
            
            question.append(strnu)
            anscount.append(counter)
            
        #Creating a tuple from the two lists, then creating a dictionary from that tuple.

        tipto = tuple(zip(question,anscount))
        dicto = dict(tipto)

        #This function returns the question or questiosn that where answered incorrectly the most.
        #This is doen by finding the key with the lowest value and returning the key.

        def lowestkey(some_dict):
            
             #Set up positions so that is can be appended to.
            
            questions = []
            min_value = float("inf")
            for k, v in some_dict.items():
                if v == min_value:
                    questions.append(k)
                if v < min_value:
                    min_value = v
                    
                    #Setup output for use in the follwing code.
                    
                    questions = [] 
                    questions.append(k)

            return questions

        #Run minimums to find the questiosns aswered incorrectly the most.

        lowest = lowestkey(dicto)
        loweststr = ','.join(lowest)
        lenlow = len(lowest)

        if lenlow == 1:
            strlow = 'The question most commonly answered incorrectly is: ' + loweststr + '.'
        if lenlow >1:
            strlow = 'The questions most commonly answered incorrectly are: ' + loweststr + '.'
    
        lblTestTitle = tk.Label(self, text=strlow, font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=29, column=0, columnspan=12, padx=10, pady=5, sticky=tk.N)
        
        #Data display button.
        
        buttonstatMenu = tk.Button(self, text="View the data used in the graphs", font=('verdana', 12, 'normal'), width=30, height=2)        
        buttonstatMenu['command']=self.justdata
        buttonstatMenu.grid(row=30, column=0, columnspan=12, padx=10, pady=10, sticky=tk.N)
        
    #Shows the user the data used to make the graphs.
    
    def justdata(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = justdata(self.newWindow)
        
    #Returns user to Stats menu.

    def openMainMenu(self):
        self.master.destroy()
        
    #Exits the system.

    def exitSystem(self):
        if tkinter.messagebox.askokcancel("Quit", "Are you sure you wish to exit the system?"):
            self.quit()
        
#Just data for use if the graphs aren't clear enough.
        
class justdata(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.dispdata()  
        
    def dispdata(self):  
        
        tittlew = selectedTest        
        tittlew = tittlew[:-4]       
        
        mentitle = 'Graph data page for: ' + tittlew
        
        #Title label for this page.
        
        lblTestTitle = tk.Label(self, text=mentitle, font=('Courier New', 25, 'bold'), fg='firebrick3')
        lblTestTitle.grid(row=0, column=0, columnspan=12, padx=10, pady=10, sticky=tk.N)
        
        lblTestTitle = tk.Label(self, text='This page aims to provide the user with the exact information shown in the graphs.', font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=1, column=0, columnspan=12, padx=10, pady=10, sticky=tk.N)
        
        #Gathering the data from the global variables and fromatting it.
        
        stravg = float('{0:.2f}'.format(average))         
        avgout1 = 'Average score after 1 attempt is: ' + str(stravg) + ' (2dp)'
           
        stravg2 = float('{0:.2f}'.format(average2))         
        avgout2 = 'Average score after 2 attempts is: ' + str(stravg2) + ' (2dp)'       
                    
        stravg3 = float('{0:.2f}'.format(average3))         
        avgout3 = 'Average score after 3 attempts is: ' + str(stravg3) + ' (2dp)'    
                
        hscorestr1 = 'Highest score after 1 attempt is: ' + str(highscore1)        
        hscorestr2 = 'Highest score after 2 attempts is: ' + str(highscore2)
        hscorestr3 = 'Highest score after 3 attempts is: ' + str(highscore3)
        
        #Labels for all the data.
        
        lblTestTitle = tk.Label(self, text='This is the Average score data:', font=('verdana', 12, 'bold', 'underline'))
        lblTestTitle.grid(row=2, column=0, columnspan=12, padx=10, pady=10, sticky=tk.N)
        
        lblTestTitle = tk.Label(self, text=avgout1, font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=3, column=0, columnspan=12, padx=10, pady=10, sticky=tk.N)
        
        lblTestTitle = tk.Label(self, text=avgout2, font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=4, column=0, columnspan=12, padx=10, pady=10, sticky=tk.N)
        
        lblTestTitle = tk.Label(self, text=avgout3, font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=5, column=0, columnspan=12, padx=10, pady=10, sticky=tk.N)
        
        lblTestTitle = tk.Label(self, text='This is the high score data:', font=('verdana', 12, 'bold', 'underline'))
        lblTestTitle.grid(row=7, column=0, columnspan=12, padx=10, pady=10, sticky=tk.N)
        
        lblTestTitle = tk.Label(self, text=hscorestr1, font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=8, column=0, columnspan=12, padx=10, pady=10, sticky=tk.N)
        
        lblTestTitle = tk.Label(self, text=hscorestr2, font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=9, column=0, columnspan=12, padx=10, pady=10, sticky=tk.N)
        
        lblTestTitle = tk.Label(self, text=hscorestr3, font=('verdana', 12, 'bold'))
        lblTestTitle.grid(row=10, column=0, columnspan=12, padx=10, pady=10, sticky=tk.N)        
        
        #Exit buttons.        
        
        buttonstatMenu = tk.Button(self, text="Return To the Display Page", font=('verdana', 12, 'normal'), width=25, height=2)
        buttonstatMenu['command']=self.openMainMenu
        buttonstatMenu.grid(row=31, column=0, columnspan=12, padx=20, pady=5, sticky=tk.N)

        buttonstatMenu = tk.Button(self, text="Exit", font=('verdana', 12, 'normal'), width=8, height=2)
        buttonstatMenu['command']=self.exitSystem
        buttonstatMenu.grid(row=32, column=0, columnspan=12, padx=20, pady=5, sticky=tk.N)
        
    #Returns user to Display Page.

    def openMainMenu(self):
        self.master.destroy()
        
    #Exits the system.

    def exitSystem(self):
        if tkinter.messagebox.askokcancel("Quit", "Are you sure you wish to exit the system?"):
            self.quit()
        