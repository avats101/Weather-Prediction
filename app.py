# !pip install opencage
from flask import Flask, render_template, request
app = Flask(__name__)  # initializing Flask app
@app.route("/")
def index():
    return render_template('index.html')
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == "POST":
        import datetime
        import calendar,time
        from statsmodels.tsa.arima.model import ARIMA
        from collections import namedtuple
        import requests
        import pandas as pd
        from opencage.geocoder import OpenCageGeocode
        import config

        current_time_exact= datetime.datetime.now()
        current_time=current_time_exact.strftime("%Y-%m-%d %H:%M:%S")
        current_year=int(current_time_exact.strftime("%Y"))        
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
        
        # x_cord="19.0760"
        # y_cord="72.8777"
        geocoder = OpenCageGeocode(config.opencagekey)
        city=request.form['city'] 
        # city = u'Mumbai'
        results = geocoder.geocode(city)
        x_cord=str(results[0]['geometry']['lat'])
        y_cord=str(results[0]['geometry']['lng']) 

        df1 = []
        features = ['temperatureMin','temperatureMax','sunriseTime','sunsetTime']
        DailySummary = namedtuple("DailySummary", features)        

        for time in epoch_time_list:
            if time<1293840000 or time>=1325376000:
                BASE_URL = "https://api.darksky.net/forecast/"+config.darkskykey+"/"+x_cord+","+y_cord+"," + str(time)+"?exclude=currently,flags,alerts,hourly"#here latitude,longitude variable is yet to be used
                response = requests.get(BASE_URL)
                data = response.json()
                if "daily" in data:
                    df = pd.DataFrame(data["daily"]["data"])
                    if 'temperatureHigh' in data['daily']['data']:
                        temperatureMax = df.at[0, 'temperatureHigh']
                    else:
                        temperatureMax=df.at[0,'temperatureMax']
                    if 'temperatureLow' in data['daily']['data']:
                        temperatureMin = df.at[0, 'temperatureLow']
                    else:
                        temperatureMin=df.at[0,'temperatureMin']
                df1.append(DailySummary(sunriseTime = df.at[0, 'sunriseTime'],sunsetTime = df.at[0, 'sunsetTime'],temperatureMin =temperatureMin,temperatureMax = temperatureMax ))            
        res = pd.DataFrame(df1, columns=features)
        tempMin=res['temperatureMin']
        tempMax=res['temperatureMax']
        
        # MIN MODEL
        model = ARIMA(tempMin, order=(1,0,0))
        model_fit = model.fit()
        forecast_min = round(((model_fit.forecast().tolist()[0])-32)*5/9,2)
        # MAX MODEL
        model = ARIMA(tempMax, order=(1,0,0))
        model_fit = model.fit()
        forecast_max = round(((model_fit.forecast().tolist()[0])-32)*5/9,2)

        return render_template('index.html', max=forecast_max,min=forecast_min)  
    return('index.html')


app.run(host="0.0.0.0",debug=True)              
