import json
from datetime import datetime
import plotly.express as px
import plotly.io as pio


def convert_date(iso_string):
    d = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
    return d.strftime('%A %d %B %Y')

def convert_f_to_c(temp_in_farenheit):
    celcius = ((float(temp_in_farenheit)-32)*5 / 9)
    celcius = round(celcius, 1)
    return celcius


with open("data/forecast_10days.json") as file:
    weather_data = json.load(file)


minimum_temp_lst = []
maximum_temp_lst = []
minimum_real_feel = []
minimum_real_feel_shade = []
day_lst = []

for day in weather_data["DailyForecasts"]:    
    
    date = convert_date(day["Date"])
    day_lst.append(date)

    min_temp_f = day["Temperature"]["Minimum"]["Value"]
    min_temp_c = convert_f_to_c(min_temp_f)
    minimum_temp_lst.append(min_temp_c)

    max_temp_f = day["Temperature"]["Maximum"]["Value"]
    max_temp_c = convert_f_to_c(max_temp_f)
    maximum_temp_lst.append(max_temp_c)
    
    min_feel_f = day["RealFeelTemperature"]["Minimum"]["Value"]
    min_feel_c = convert_f_to_c(min_feel_f)
    minimum_real_feel.append(min_feel_c)

    min_shade_f = day["RealFeelTemperatureShade"]["Minimum"]["Value"]
    min_shade_c = convert_f_to_c(min_shade_f)
    minimum_real_feel_shade.append(min_shade_c)

data = {
    "Date": day_lst,
    "Minimum Temp": minimum_temp_lst,
    "Maximum Temp": maximum_temp_lst,
    "Minimum Real Feel": minimum_real_feel,
    "Minimum Shade": minimum_real_feel_shade,
}

pio.templates.default = "plotly_dark"

fig = px.line(data, 
    x="Date",
    y=["Minimum Temp", "Maximum Temp"],
    title="Forecast Highs and Lows"
)
fig.update_traces(
    mode = 'lines+markers'
)

fig.update_layout(
    yaxis_title = "Temperature in C",
    xaxis_title = "Day"
)

fig.show() 


fig2=px.line(data,
    x="Date",
    y=["Minimum Temp", "Minimum Real Feel", "Minimum Shade"],
    title= "Shade Temperatures"
)

fig2.update_traces(
    mode = 'lines+markers',
    
)

fig2.update_layout(
    yaxis_title = "Temperature in C",
    xaxis_title = "Day"
)

fig2.show()