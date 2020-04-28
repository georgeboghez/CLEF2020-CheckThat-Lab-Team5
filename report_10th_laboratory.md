# 9th Laboratory's Report


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

-   Completed this week:
    -   Unit tests for the all() and special() methods corresponding to “/all” and “/secret” routes in test_main.py - test_index() and test_special(), respectively ([Github](https://github.com/georgeboghez/CLEF2020-CheckThat-Lab-Team5/blob/master/Heroku%20Test/tests/test_main.py))
    -   Help create a new database table for unfiltered tweets and new Flask routes relating to it - “/all_unfiltered_tweets” and “/all_unfiltered_tweets/<int:count>” - in main.py
   -   Problems this week: Researching and adapting to unit test in python, ‘unittest’ specifically, and using them to test Flask routes
    
-   Plans for next week: Further improve on unit tests and raise code coverage, as well as help our joining team with their filtering functionality


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
