# 12th Laboratory's Report


## Tanase Teofil:

Completion:
- Created the design.psd of the platform alongside Elisa Giurgea.
- Added code for multi-threading using background tasks alongside George, Razvan and Radu.

To do: 
- Further optimise the code and help my team.
- To help on the front-end side.

## Bejenariu Razvan-Andrei:

Completed:

-   Added a POST request with Radu in order to send the number of new tweets to Alexandru Oloieri's module
-   Added code for multi-threading using background tasks alongside George, Teofil and Radu.    	

To do:

-  Use coverage to make sure unit testing covered over 80% of possible tests.

## Roșu Cristian-Mihai:

-   Completed this week: 
    - Wrote unit tests for the newly modified crawler.py in test_crawler.py
    - Raised crawler.py code coverage to 95%
    - Helped coleagues with other test classes 
-   Problems this week: Finding and using the right pyhton packages and services for running unit tests locally
-   Plans for next week: Efficiently divide work among the cooperating teams and further help with integration


## Placinta Radu:
-   Completed this week:
	- Added a POST request (along with Razvan) in order to send the number of new tweets to Alexandru Oloieri's module
	- Added multi-threading along with George, Razvan and Teofil.
	- Cleaned up, rearranged the code

-   Plans for next week:
	- To further optimize/clean the code.
	- Research related to REST, front-end design etc.

## Boghez George:
-   Completed this week:
	-   Assigned tasks to my teammates after getting all the necessary information from the conversations we had with the other team
	
	-   Integrated alongside Cristian Rosu and Catalin Sumanaru a functionality for listening the new events that occur on a database (in order to send the data dynamically to the frontend component)
	
	-   The mentioned integration required a database migration (from mLab to AWS, mainly made by Catalin) because the database I created and we used with a free plan didn't grant us root privileges, and we made sure everything works as expected
	
	-   Created a multithreading way of inserting tweets into the database (in order to fix the unexpected of heroku, which used to stop the insertion after 30 seconds) alongside Razvan Bejenariu, Radu Placinta and Teofil Tanase. Then, I had to revisit the code and implement a background task in python with rq https://devcenter.heroku.com/articles/python-rq
	
	-   Reviewed other members' work
-   Plans for next week: 
	-   Unit testing for the code we have written over the past week
	-   Lend a hand to the other team if necessary
