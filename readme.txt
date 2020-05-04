That is how I made answerbot work:

1. Created new app named 'answerbotloco' on heroku: https://dashboard.heroku.com/new-app 
2. Performed all steps from 'Deploy using Heroku Git' section of 'Deploy' tab of my app on Heroku:
  	- installed Heroku CLI
	- checked Git installed (if you have no Git: https://git-scm.com/downloads)
	- made in Windows cmd: 
		cd <Path_To_Answerbot>/answerbotloco/
		git init
		heroku git:remote -a answerbotloco
		git add .
		git commit -am "make it better"
		git push heroku master

3. Switched to 'Resources' tab ('https://dashboard.heroku.com/apps/answerbotloco/resources'). 
Dyno with text 'worker python main.py' must appear. Powered it on.


Then it should work. 

Main changes I did: 
	added 'runtime.txt' file with python version information
	modified 'requirements.txt'
	added 'Procfile' with 'worker python main.py'
	