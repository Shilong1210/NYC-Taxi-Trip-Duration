# NYC-Taxi-Trip-Duration
APAM 4990 Project

# May 2019

## Files
- data

data.7z, test.7z, weather.7z
- model

l1_model, rf_model, xgb_model<br>
- Prediction

l1_prediction.csv, rf_prediction.csv, xgb_prediction.csv
- NYC Taxi Trip Duration.ipynb


## Data Preparation
 - BigQuery Public Dataset
 
    1,000,000 randomly selected data from 'bigquery-public-data.new_york.tlc_yellow_trips_2016';
    Weather data from 'bigquery-public-data.noaa_gsod.gsod2016'
    
 - Apply PCA to longitude and latitude pairs
 
## Model
 - XGBoost
 - Linear Regression
 - Random Forrest


## Web
Prediction web: http://ysl19941210.pythonanywhere.com/  
*Example:  
Pickup datetime: 2015-06-18 21:52:45+00:00  
Pickup longitude: -74.011650  
Pickup latitude: 40.702740  
Dropoff longitude: -73.990311   
Dropoff latitude: 40.773361  
Passenger count: 5*
