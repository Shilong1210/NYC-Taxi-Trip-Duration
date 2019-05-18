import numpy as np
import math
import pandas as pd
from sklearn.decomposition import PCA

# Haversine distance
def hav_distance(lat1, lng1, lat2, lng2):
    lat1, lng1, lat2, lng2 = map(np.radians, (lat1, lng1, lat2, lng2))
    AVG_EARTH_RADIUS = 6371
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = np.sin(lat * 0.5) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lng * 0.5) ** 2
    h = 2 * AVG_EARTH_RADIUS * np.arcsin(np.sqrt(d))
    return h

# Euclidean distance
def euc_distance(lat1,lng1,lat2,lng2):
    lat1, lng1, lat2, lng2 = map(np.radians, (lat1, lng1, lat2, lng2))
    AVG_EARTH_RADIUS = 6371
    e = math.sqrt((AVG_EARTH_RADIUS * (lat1-lat2))**2+(AVG_EARTH_RADIUS * (lng1-lng2))**2)
    return e

# Manhattan distance
def man_distance(lat1,lng1,lat2,lng2):
    a = hav_distance(lat1, lng1, lat1, lng2)
    b = hav_distance(lat1, lng1, lat2, lng1)
    return a + b

def preprocess(data):    
    # Convert multi-class label to one-hot value
    tmp = data.copy()
    tmp['hour'] = tmp['hour'].map({0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:1,8:1,9:1,10:1,11:2,12:2,13:2,
                  14:3,15:3,16:3,17:3,18:4,19:4,20:4,21:5,22:5,23:5})
    for i in range(1,7):
        if(tmp['month'][0]==i):
            tmp['month_'+str(i)]=[1]
        else:
            tmp['month_'+str(i)]=[0]
    for i in range(6):
        if(tmp['hour'][0]==i):
            tmp['hour_'+str(i)]=[1]
        else:
            tmp['hour_'+str(i)]=[0]
    for i in range(1,8):
        if(tmp['day'][0]==i):
            tmp['day_'+str(i)]=[1]
        else:
            tmp['day_'+str(i)]=[0]
    
    # Replace samples of no record with mean value
    mean_tmp = 51.07
    tmp['temp'] = tmp['temp'].replace(9999.9,mean_tmp)
    mean_tmp = 9.11
    tmp['visib'] = tmp['visib'].replace(999.9,mean_tmp)
    mean_tmp = 5.12
    tmp['wdsp'] = tmp['wdsp'].replace(999.9,mean_tmp)
    mean_tmp = 21.49
    tmp['gust'] = tmp['gust'].replace(999.9,mean_tmp)
    mean_tmp = 62.04
    tmp['max'] = tmp['max'].replace(9999.9,mean_tmp)
    mean_tmp = 42.26
    tmp['min'] = 0.089
    mean_tmp = np.mean([item for item in tmp['prcp'] if item != 99.99])
    tmp['prcp'] = tmp['prcp'].replace(999.9,mean_tmp)
    
    # PCA of coordinates
    tmp['pca0'] = 0
    tmp['pca1'] = 0
    
    # Convert binary labels to numerical labels
    tmp['fog'] = tmp['fog'].astype(int,copy=True,errors='raise')
    tmp['rain_drizzle'] = tmp['rain_drizzle'].astype(int,copy=True,errors='raise')
    tmp['snow_ice_pellets'] = tmp['snow_ice_pellets'].astype(int,copy=True,errors='raise')
    tmp['hail'] = tmp['hail'].astype(int,copy=True,errors='raise')
    tmp['thunder'] = tmp['thunder'].astype(int,copy=True,errors='raise')
    
    hav = []
    euc = []
    man = []
    lat1 = tmp['pickup_latitude'].values
    lng1 = tmp['pickup_longitude'].values
    lat2 = tmp['dropoff_latitude'].values
    lng2 = tmp['dropoff_longitude'].values
    for i in range(len(tmp)):
        hav.append(hav_distance(lat1[i],lng1[i],lat2[i],lng2[i]))
        euc.append(euc_distance(lat1[i],lng1[i],lat2[i],lng2[i]))
        man.append(man_distance(lat1[i],lng1[i],lat2[i],lng2[i]))
    tmp['hav_distance'] = hav
    tmp['euc_distance'] = euc
    tmp['man_distance'] = man
    
    no_use = ['pickup_datetime','dropoff_datetime','date','date2','year',
          'pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude','sndp','month','hour','day']
    
    feature_names = [f for f in tmp.columns if f not in no_use]
    
    tmp['hav_distance'][0] = scale(tmp['hav_distance'][0],3.35,3.67)
    tmp['euc_distance'][0] = scale(tmp['euc_distance'][0],3.84,4.4)
    tmp['man_distance'][0] = scale(tmp['man_distance'][0],4.33,4.87)
    tmp['temp'][0] = scale(tmp['temp'][0],51.07,15.36)
    tmp['visib'][0] = scale(tmp['visib'][0],9.11,1.34)
    tmp['wdsp'][0] = scale(tmp['wdsp'][0],5.12,2.17)
    tmp['gust'][0] = scale(tmp['gust'][0],21.49,4.65)
    tmp['max'][0] = scale(tmp['max'][0],62.04,16.47)
    tmp['min'][0] = scale(tmp['min'][0],42.26,14.7)
    tmp['prcp'][0] = scale(tmp['prcp'][0],0.089,0.23)

    return tmp[feature_names]

def scale(x,mean,std):
    return (x-mean)/std


def merge(test,weather):
    tmp = test.copy()
    date_time = pd.to_datetime(tmp['pickup_datetime'])
    
    date = date_time.dt.date
    date = [str(day) for day in date]
    month = date_time.dt.month
    month = month.map({1:1,2:2,3:3,4:4,5:5,6:6,7:6,8:5,9:4,10:3,11:2,12:1})
    day = date_time.dt.weekday+1
    hour = date_time.dt.hour
    
    tmp['date2'] = date
    tmp['month'] = month
    tmp['day'] = day
    tmp['hour'] = hour
    
    tmp = tmp.merge(weather,how = 'left',left_on='date2',right_on='date')
    
    return tmp