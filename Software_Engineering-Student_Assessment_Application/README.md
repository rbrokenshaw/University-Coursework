# Team 2 Software Engineering project v2

Instructions for downloading and editing system:

Pull the latest version from Git:

1. Go to Terminal/ Command Line and navigate to a folder where you want to save the project.
2. type 'git init'
3. type 'git clone git@gitlab.cs.cf.ac.uk:c1535557/team-2-software-engineering-project-v2.git'

The project should now be in your folder. Make sure you 'git pull origin master' often to get the latest code. You probably won't be able to push any code you've written if you haven't 'pulled' first.

The project has been set up as a package. The file 'login.py' has been set up as the main page, and all the other 'windows' of the system are in the 'sections' folder.

How to run the program:

1. Open 'login.py' in Sublime Text (or text editor of choice)
2. Run the file by going to Tools > Build or press Cmd/Ctrl + B
3. the Login page should pop up, and you can navigate to your section from here

How to Build Your Own Section:

1. Go to the sections folder and open your section file in Sublime Text
2. The basic skeleton is already done. Don't change the main Frame class, just build your section inside the frame. If you need multiple frames (say for a menu), build each frame as a separate class and call them using buttons. Look in either the student menu or staff menu file to see how this is done.

** DON'T PUSH CODE TO THIS GITLAB UNLESS YOU'RE SURE EVERYTHING WORKS AND YOU HAVEN'T BROKEN ANYTHING!! ;) **