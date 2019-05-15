# Airbnb_Pricing
Final project of INFO 6105 by Team - 8 
Predicting the price of room based on the number of beds, bathroom, bedroom and amineties.
Also predicting the price with surge price.

Following Folders are included:
- Data
First it is needed to download the data from insideairbnb.com/boston. Using Docker image you can clean the data according to the model. To run docker uses the command by going into the folder where the initial files are stored. docker run nidhi1993/pipeline. Save all the data in this folder.
  
- Code

AutoML - It contains all the files related to autoML. We have used Tpot and H20 models.

EDA - It contains all the files related to EDA.

Pipeline-Docker: It shows the implimentation of pipeline and docker. we have used dask pipeling for cleaning of the data. Giving the aribnb.csv as input we will get the cleaned data.

SurgePrice- It contains the model to predict the surge price based on the day.

Webapp- We have implimented flask to deploy our web application. We would be hosting the webapp on heroku. Filling out the required inputs we would get the predicted price.

Heroku - It contains all the files needed to deploy the heroku app.

Using the model.

To obtain cleand data you have to download the data and clean it using docker as mentioned above.

The web application has a simple user interface where giving the required inputs it will give you the predicted price.


project proposal Doc: http://tiny.cc/airbnbpricing

Project Report: https://bit.ly/2GDXJ91

Data collected from : http://insideairbnb.com/boston

Heroku app - https://bostonairbnbpriceprediction.herokuapp.com/
