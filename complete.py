import datetime
current_time_exact= datetime.datetime.now()
current_time=current_time_exact.strftime("%Y-%m-%d %H:%M:%S")
current_year=int(current_time_exact.strftime("%Y"))
import calendar,time
current_epoch_time=calendar.timegm(time.strptime(current_time, '%Y-%m-%d %H:%M:%S'))
tmrw_epoch_time=current_epoch_time+86400
epoch_time_list=[tmrw_epoch_time]
epoch_time=tmrw_epoch_time
for year in range(current_year-1,2007,-1):
    if (( year%400 == 0)or (( year%4 == 0 ) and ( year%100 != 0))):
        epoch_time=epoch_time-31622400
        epoch_time_list.append(epoch_time)
    else:
        epoch_time=epoch_time-31536000
        epoch_time_list.append(epoch_time)
epoch_time_list.reverse()
import requests
import pandas as pd
from collections import namedtuple
df1 = []
features = ['temperatureMin','temperatureMax','sunriseTime','sunsetTime']
DailySummary = namedtuple("DailySummary", features)
apikey="24f425975f71f30890d8d790e82cc8bc"
x_cord="28.7041"
y_cord="77.1025" 
for time in epoch_time_list:
    if time<1293840000 or time>=1325376000:
        BASE_URL = "https://api.darksky.net/forecast/"+apikey+"/"+x_cord+","+y_cord+"," + str(time)+"?exclude=currently,flags,alerts,hourly"#here latitude,longitude variable is yet to be used
        response = requests.get(BASE_URL)
        data = response.json()
        if "daily" in data:
            df = pd.DataFrame(data["daily"]["data"])
            df1.append(DailySummary(sunriseTime = df.at[0, 'sunriseTime'],sunsetTime = df.at[0, 'sunsetTime'],temperatureMin = df.at[0, 'temperatureLow'],temperatureMax = df.at[0, 'temperatureHigh']))                  
res = pd.DataFrame(df1, columns=features)
tempMin=res['temperatureMin']
tempMax=res['temperatureMax']
import pandas as pd
from pandas import Series
from statsmodels.tsa.arima.model import ARIMA
model = ARIMA(tempMin, order=(1,0,0))
model_fit = model.fit()
forecast_min = model_fit.forecast()
print(forecast_min)
model = ARIMA(tempMax, order=(1,0,0))
model_fit = model.fit()
forecast_max = model_fit.forecast()
print(forecast_max)
# clear all the logs is still left
# Change the order by seeing this https://people.duke.edu/~rnau/411arim3.htm