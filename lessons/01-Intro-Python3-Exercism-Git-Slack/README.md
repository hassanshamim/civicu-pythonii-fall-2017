# Python level II Day 1 

## Welcome!!!
Thank you all for being willing to take time out of your day to learn some Python! It's our goal in this class to provide students with the skills needed to start making real projects and to be able to access and collect data. We will be focusing primarily on the backend side of things and will spend most of our time working with 3rd party APIs as well as building our own using the Django REST Framework. Day one of this class will focus on setting things up so that we'll be successful throughout the rest of our time together. Below you'll find a list of class objectives and information about the tools we'll be using during the next 8 weeks. 

### Tonight's objectives
* Get to know one another
* Review Course objectives / syllabus
* Class communication channels (Slack, email, GitHub)
* Get working dev environment setup (Python 3, setting up virtualenvs)
* Explain how we will use Git and GitHub (forking repos, setting upstream repo, pushing to fork)
* Introduce Exercism tool and solve a code challenge
* Take Python general knowledge survey

## Class communication channels
* [Link to Class Slack Channel](hacku-2017.slack.com)
* Email hassan.has.you@gmail.com

## Setting up your environment

#### Python 3 install
* [Python 3 install on Mac with Brew](http://python-guide-pt-br.readthedocs.io/en/latest/starting/install3/osx/)
* [Main installation page](https://www.python.org/downloads/)

#### Possible text editors
* [Sublime Text 3](https://www.sublimetext.com/3)
* [Visual Studio Code](https://code.visualstudio.com/)

#### Virtual environments
* [Article on virtual environments](https://realpython.com/blog/python/python-virtual-environments-a-primer/)

## Using Git & GitHub
Throughout this course we will be using Git and GitHub as a convenient way to share code with one another and to monitor student's progress. Bellow you'll find a link to an interactive GitHub tutorial and instructions for how we will share work with one another. 

* [Link to interactive GitHub tutorial](https://try.github.io/levels/1/challenges/1)

#### Steps for class GitHub setup
* Fork the class repo to your GitHub account
  * [class repo](https://github.com/hackoregon/civicu-pythonii-summer-2017)
* Clone the forked repo onto your local machine
  * `git clone <github_url_to_forked_repo>`
* Move into the directory of the repo you just cloned
* Run the command `git remote -v` you should see the repo you forked to your GitHub as `origin`
* Link your forked repo to the original
  * [docs on configuring a remote fork](https://help.github.com/articles/configuring-a-remote-for-a-fork/)
  * URL for `upsteam` repo: `https://github.com/hackoregon/civicu-pythonii-summer-2017.git`
* Sync your forked repo with the original
  * We will follow the process in the link below to get new code for each day in class
  * [docs on syncing a fork](https://help.github.com/articles/syncing-a-fork/)
* Make a new directory using your name as the title inside the `student-work` directory in the class repo. Using the command `mkdir <your_name_here>`
* Inside your newly created directory use the command `touch README.md` to create a new README.md file 
* Use git to add and commit the file you just created 
    * Remember the commands `git status`, `git add`, and `git commit -m "your message here"`
* Push the changes to your GitHub fork (called `origin`) with the command `git push origin master`
* Go to your forked `civicu-pythonii-summer-2017` repo on GitHub and make a pull request against the class repo with your changes
  * URL to your forked repo `https://github.com/<your_user_name>/civicu-pythonii-summer-2017`
  * Click on `new pull request` button
  * Make sure the base fork is: `hackoregon/civicu-pythonii-summer-2017` and that the base branch is `master`
  * Click `create pull request`

## Introduction to Exercism
[Exercism.io](http://exercism.io/languages/python/about) is a really cool learning resource that has a selection of ready made code challenges with included tests that we will use occasionally during our course. We will only use the code challenges in Exercism when they apply directly to what we're learning but will follow a similar format for custom in class challenges.

In order to get Exercism setup on your computer please follow the link below: 
[Exercism CLI install](http://exercism.io/clients/cli)

Once you have the CLI installed, be sure to configure it.  On the command line:

`exercism configure —key=YOUR_API_KEY`

`exercism configure --dir=/PATH/TO/YOUR/STUDENT/WORK/FOLDER`

Once the CLI for Exercism is installed run the command `exercism fetch python word-count` to get the mini exercise we will be solving. Once you've solved the problem push the solution with `exercism submit <path_to_solution_file>`. While you're solving this problem you should receive an invite to the Exercism team for our class. This will allow students to comment on each others solutions and share the different problems they've solved. 

## Python general knowledge survey
The link below will lead you to a survey about your current level of Python knowledge. It's completely anonymous and will be used as a way to tailor instruction according to the needs of the class. We ask that you complete the form before leaving tonight and do so without looking up answers while you're filling it out. It's perfectly ok if you aren't familiar with everything in the survey, just fill out what you can.
[Python Knowledge survey](https://docs.google.com/forms/d/e/1FAIpQLSeTHygb_hcfFRYdY0Lv9xdyVASFGPiDYTgp7hYHt-IiKT2pBQ/viewform?usp=sf_link)
