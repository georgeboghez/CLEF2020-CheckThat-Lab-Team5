# 10th Laboratory's Report


## Tanase Teofil:

Completion:
-   Translation from Romanian to English on autoInsertTweets and main methods.
-   Used coverage to make sure unit testing covered over 80% of possible tests on autoInsertTweets and main methods.
-   Cleaned up code.
-   Optimised main method.
To do: 
-   further optimise the code.

## Bejenariu Razvan-Andrei:

-   Translated error messages to English
-   Used coverage to make sure unit testing covered over 80% of possible tests on main methods.     	
-   Cleaned up code

-  To continue to optimize the code and improve the app in general

## Roșu Cristian-Mihai:

-   Completed this week: Improved previous unit tests to raise code coverage in main.py
-   Problems this week: Researching and adapting to unit test in python
-   Plans for next week: Maintaint good code structure and planning


## Placinta Radu:
-   Completed this week:
	- Improved the unit test for the getTweets function in the crawler.
	- Translated the error messages to English.
-   Issues:
	- Ran into a few problems when writing the tests.
-   Plans for next week:
	- To further optimize/clean the code.
	- Research related to testing, front-end design etc.

## Boghez George:

-   Completed this week:
	-   Improved Unit Tests for enriching the coverage
    
	-   Reviewed code, solved conflicts,  
	
	-   Made sure team 4 is constantly provided with tweets for training their algorithm having in mind to grow their dataset significantly
	
	-   Ensured other teams' members have access to the database, providing them corresponding information when needed 
	
	-   Integrated the new filtering methods, which include the implementation of the Naive Bayes algorithm for filtering the tweets, alongside Ioan Sava
    
-   Plans for next week: 
	-   While integrating Ioan's algorithm, we noticed the request to introduce the tweets into the database takes longer than 30 seconds, therefore exceeding the heroku's request timeout and the job not having the needed time to insert all the tweets. I have done some research and found out we could solve this issue by creating a background job https://devcenter.heroku.com/articles/background-jobs-queueing, https://devcenter.heroku.com/articles/python-rq
	-   We're planning on starting the front-end development
