# 11th Laboratory's Report


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
-   Added code for multi-threading using background tasks alongside George, Razvan and Radu.    	

To do:

-  Use coverage to make sure unit testing covered over 80% of possible tests.

## Roșu Cristian-Mihai:

-   Completed this week: 
    - Helped add a data insertion detection functionality alongside George and Cătălin
    - Removed some unnecessary Flask routes: */all* and */all/count* 
-   Problems this week: Migrating a part of our tables from mLab to AWS for portability
-   Plans for next week: Efficiently divide work among the cooperating teams and help the frontend


## Placinta Radu:
-   Completed this week:
	- Added a POST request (along with Razvan) in order to send the number of new tweets to Alexandru Oloieri's module
	
	- Cleaned up, rearranged the code

-   Plans for next week:
	- To further optimize/clean the code.
	- Research related to REST, front-end design etc.

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
