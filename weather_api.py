import requests
import logging
from datetime import datetime
from pprint import pprint
import os


logging.basicConfig(filename='weather.log', level=logging.INFO)


def main():

    
    city, country = get_city_country()

    try:
        data = get_current_conditions(city, country)

        if data:
            forecast_items =  data['list']
            for forecast in forecast_items:
                current_temp_f = extract_temperature(forecast)
                temp_desc = extract_temp_desc(forecast)
                wind_speed = extract_wind_speed(forecast)
                date= extract_date(forecast)

                date_display = f'on {date}'
                temp_display = f'''The temperature in {city.title()}, {country.upper()} will be 
                {current_temp_f:.2f} F with wind speed of {wind_speed:.2f} mph'''              

                output = f'{date_display} {temp_display} and {temp_desc}'
                print(output)
                logging.info('Successful query with result: ' + output)

        else:
            logging.info('Location %s, %s not found' % (city, country))
            print('This location was not found.')

    except Exception:  # TODO handle different types of error
        # As this is the first statement in the except block, a stack trace will be logged too
        logging.exception('Error fetching current weather data for %s, %s' % (city, country))
        # These are errors that a user can't fix. The developer needs to fix it.
        print('Sorry, there was an error fetching data. '
              'Please check your internet connection, and if that\'s ok, report this to the developer.')

def get_city_country():
    '''
    asks users city and country then returns them
    '''
    city = input('Please enter city name? ')
    country = input(f'What country is {city} in? ')

    return city, country


def get_current_conditions(city, country):
    '''
    takes city and country then returns json data or none if city or country not found
    '''

    url = 'http://api.openweathermap.org/data/2.5/forecast'

    key = os.environ.get('WEATHER_KEY')  # Make sure you set this environment variable
    assert key is not None  # raises an error if environment variable is not set

    # parameters for the API
    location = '%s,%s' % (city, country)
    params = {'q': location, 'units': 'imperial', 'APPID': key}

    response = requests.get(url, params)

    # Status codes of 200 mean the request was received and processed without error
    if response.status_code == 200:
        return response.json()

    # The API returns 404 (Not Found) if the location can't be found. Check for this and return None
    if response.status_code == 404:
        return None

    # Any other errors, raise an exception
    response.raise_for_status()  # Raise an exception if the status code is not 2xx or 3xx

def extract_temperature(data):
    '''
    extracts temperture from json data and returns it
    '''
    return data['main']['temp']

def extract_temp_desc(data):
    '''
    extracts the description of the weather in the data and returns it
    '''
    return data['weather'][0]['description']

def extract_wind_speed(data):
    '''
    extracts the wind speed of the weather in the data and returns it
    '''
    return data['wind']['speed']


def extract_date(data):
    timestamp = data['dt']  # Unix timestamp
    date = datetime.fromtimestamp(timestamp)  # Convert to a datetime, for humans
    return date


if __name__ == '__main__':
    main()
