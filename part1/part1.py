import json
from datetime import datetime

DEGREE_SYBMOL = u"\N{DEGREE SIGN}C"

def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees and celcius symbols.
    
    Args:
        temp: A string representing a temperature.
    Returns:cd
        A string contain the temperature and 'degrees celcius.'
    """
    return f"{temp}{DEGREE_SYBMOL}"

def convert_date(iso_string):
    """Converts an ISO formatted date into a human readable format.
    

    Returns:
        A date formatted like: Weekday Date Month Year
    """
    d = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
    return d.strftime('%A %d %B %Y')

def convert_f_to_c(temp_in_farenheit):
    celcius = ((float(temp_in_farenheit)-32)*5 / 9)
    celcius = round(celcius, 1)
    return celcius
    

def calculate_mean(total, num_items):
    mean = total / num_items
    mean = round(mean, 1)
    return mean

def process_weather(forecast_file):
    """Converts raw weather data into meaningful text.

    Args:
        forecast_file: A string representing the file path to a file
            containing raw weather data.
    Returns:
        A string containing the processed and formatted weather data.
    """
    final_string = ""

    with open(f"{forecast_file}") as file:
        weather_data = json.load(file)

        data_structure = []

        for day in weather_data["DailyForecasts"]:
            weather_dictionary = {
                "Date": "",
                "Minimum Temperature": "",
                "Maximum Temperature": "",
                "Day": "",
                "Day Rain Probability": "",
                "Night": "",
                "Night Rain Probability": "",
            }
        
            date = convert_date(day["Date"])
            weather_dictionary["Date"] = date

            min_temp_f = day["Temperature"]["Minimum"]["Value"]
            min_temp_c = convert_f_to_c(min_temp_f)
            weather_dictionary["Minimum Temperature"] = min_temp_c
        
            max_temp_f = day["Temperature"]["Maximum"]["Value"]
            max_temp_c = convert_f_to_c(max_temp_f)
            weather_dictionary["Maximum Temperature"] = max_temp_c

            day_description = day["Day"]["LongPhrase"]
            weather_dictionary["Day"] = day_description
        
            day_rain_probability = day["Day"]["RainProbability"]
            weather_dictionary["Day Rain Probability"] = day_rain_probability
        
            night_description = day["Night"]["LongPhrase"]
            weather_dictionary["Night"] = night_description
        
            night_rain_probability = day["Night"]["RainProbability"]
            weather_dictionary["Night Rain Probability"] = night_rain_probability        

            data_structure.append(weather_dictionary)

        lowest_temps = [(weather_d['Minimum Temperature'], weather_d["Date"]) for weather_d in data_structure]
        lowest_temp = min(lowest_temps, key=lambda pair: pair[0])

        highest_temps = [(weather_d['Maximum Temperature'], weather_d["Date"]) for weather_d in data_structure]
        highest_temp = max(highest_temps, key=lambda pair: pair[0])

        sum_low = sum(dictionary["Minimum Temperature"] for dictionary in data_structure)
        sum_high = sum(dictionary["Maximum Temperature"] for dictionary in data_structure)
        average_low = calculate_mean(sum_low,len(lowest_temps))
        average_high = calculate_mean(sum_high, len(highest_temps))

    final_string += f"""{len(lowest_temps)} Day Overview\n    The lowest temperature will be {format_temperature(lowest_temp[0])}, and will occur on {lowest_temp[1]}.\n    The highest temperature will be {format_temperature(highest_temp[0])}, and will occur on {highest_temp[1]}.\n    The average low this week is {format_temperature(average_low)}.\n    The average high this week is {format_temperature(average_high)}.
"""

    for every_day in data_structure:
        final_string += f"""
-------- {every_day['Date']} --------
Minimum Temperature: {format_temperature(every_day['Minimum Temperature'])}
Maximum Temperature: {format_temperature(every_day['Maximum Temperature'])}
Daytime: {every_day['Day']}
    Chance of rain:  {every_day['Day Rain Probability']}%
Nighttime: {every_day['Night']}
    Chance of rain:  {every_day['Night Rain Probability']}%
"""
    final_string += "\n"
    return final_string

print(process_weather)

if __name__ == "__main__":
    print(process_weather("data/forecast_5days_a.json"))

