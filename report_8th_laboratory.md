# 8th Laboratory's Report


## Tanase Teofil:

-Completion: Translation from Romanian to English on autoInsertTweets and main methods.
	     Used coverage to make sure unit testing covered over 80% of possible tests on autoInsertTweets and main methods.
	     Cleaned up code.
	     Optimised main method.
-To do: further optimise the code.

## Bejenariu Razvan-Andrei:

-   Completed unit testing for functions in main especially the unfiltered tweets ones
    
-   Created a new database for unfiltered tweets and new routes for unfiltered tweets (at the request of team 4)
	- [Main](https://github.com/georgeboghez/CLEF2020-CheckThat-Lab-Team5/blob/master/Heroku%20Test/main.py)
	- [Unit testing functions](https://github.com/georgeboghez/CLEF2020-CheckThat-Lab-Team5/blob/master/Heroku%20Test/tests/test_main.py)  	
-  Researching and learning unit testing in python, how to work with Flask routes.
 -  To continue to optimize the code and improve the app in general

## Roșu Cristian-Mihai:

-   Completed this week:
    -   Unit tests for the all() and special() methods corresponding to “/all” and “/secret” routes in test_main.py - test_index() and test_special(), respectively ([Github](https://github.com/georgeboghez/CLEF2020-CheckThat-Lab-Team5/blob/master/Heroku%20Test/tests/test_main.py))
    -   Help create a new database table for unfiltered tweets and new Flask routes relating to it - “/all_unfiltered_tweets” and “/all_unfiltered_tweets/<int:count>” - in main.py
   -   Problems this week: Researching and adapting to unit test in python, ‘unittest’ specifically, and using them to test Flask routes
    
-   Plans for next week: Further improve on unit tests and raise code coverage, as well as help our joining team with their filtering functionality


## Placinta Radu:
-   Created unit testing for 2 functions from the crawler.py file ( getTweets and getTweetsByUsers);
    
-   I ran into multiple problems trying to write the testing code correctly;
    
-   For the next week I plan on improving/cleaning my code and collaborating with my team members in order to improve functionality and integration with the other teams’ modules;
-   Link to code (test_getTweets and test_getTweetsByUsers):
    
-   [https://github.com/georgeboghez/CLEF2020-CheckThat-Lab-Team5/blob/master/Heroku%20Test/tests/test_crawler.py](https://github.com/georgeboghez/CLEF2020-CheckThat-Lab-Team5/blob/master/Heroku%20Test/tests/test_crawler.py)

## Boghez George:

-   Completed this week:
	-   Unit Testing for the main's Flask route ”/post” ([github code](https://github.com/georgeboghez/CLEF2020-CheckThat-Lab-Team5/blob/66acd811a143888fe38da1b14ac4dac5cbfa2177/Heroku%20Test/tests/test_main.py#L37))
    
	-   Code review, quick fixes for the other tests, solved conflicts
    
	-   Integration of the new updates from the filtering module alongside Ioan Sava
    
	-   New route for unfiltered tweets, a new table for them, and increased the number of tweets to retrieve ([github code - unfiltered_tweets, getCountUnfilteredTweets](https://github.com/georgeboghez/CLEF2020-CheckThat-Lab-Team5/blob/master/Heroku%20Test/main.py))
    

-   Problems this week: Research for unit testing in python, integration of the new changes team 4 has made, respond to the filtering module team’s requests
    
-   Plans for next week: Increase the performance of our service, give corresponding feedback to my teammates, work alongside team 4’s members in order to improve the filtering module, research for front-end
