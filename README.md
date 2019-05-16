# NYC-Taxi-Trip-Duration
APAM 4990 Project

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
Example:  
Pickup datetime: 2015-11-08 02:22:25+00:00  
Pickup longitude: 40.733608  
Pickup latitude: -74.003098  
Dropoff longitude: 40.836803  
Dropoff latitude: -73.941643  
Passenger count: 1
