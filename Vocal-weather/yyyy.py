import dateparser
import re
from datetime import datetime
import requests
from datetime import datetime, timedelta, timezone
from nltk.tokenize import word_tokenize , sent_tokenize
from nltk.tag import pos_tag
import os
# from conn import conn , cursor
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
load_dotenv()
from transformers import pipeline


def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language="fr-FR"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text
    
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
        return cancellation_details

open_cage_key = 'beb562d5d1af48d08571ca30efefa548'
open_weather_key = 'a8527a566c604665851222658241003'

def extract_city(text):
    ner_pipeline = pipeline("ner", model="xlm-roberta-large-finetuned-conll03-english", aggregation_strategy="simple")
    citiy = ner_pipeline(text)
    for citie in citiy:
       cities =  citie['word']
    return cities


def geocode_city(city_name):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={open_cage_key}'
    response = requests.get(url)
    if response.json()['results']:
        return response.json()['results'][0]['geometry']
    return None


def get_weather_for_weekend(lat, lon, weekend_start_date):
    print("Saturday's Weather:")
    get_weather(lat, lon, weekend_start_date.strftime("%Y-%m-%d"))
    
    sunday_date = weekend_start_date + timedelta(days=1)
    print("\nSunday's Weather:")
    get_weather(lat, lon, sunday_date.strftime("%Y-%m-%d"))

def get_weather(lat, lon, target_date_str=None, target_time_of_day=None):
    if target_date_str is None:
        print("Target date string is required.")
        city = None
        lat = 0
        lon = 0
        requested_date = None
        weather_status = None
        requested_date = None
        weather_status = "failed"
        STTError =  "Target date string is required."
        return
    try:
        formatted_date = datetime.strptime(target_date_str, "%Y-%m-%d")
    except ValueError as e:
        print(f"Error parsing target date string: {e}")
        city = None
        lat = 0
        lon = 0
        requested_date = None
        weather_status = None
        requested_date = None
        weather_status = "failed"
        STTError =  e 
        
        return

    url = f"http://api.weatherapi.com/v1/forecast.json?key={open_weather_key}&q={lat},{lon}&dt={formatted_date}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if target_time_of_day:
            for forecast in data.get('forecast', {}).get('forecastday', []):
              date = forecast.get('date')
            if date == target_date_str:
                for hour_data in forecast.get('hour', []):
                    hour_time = datetime.strptime(hour_data['time'], "%Y-%m-%d %H:%M").time()
                    if is_time_in_target_period(hour_time, target_time_of_day):
                        display_hourly_weather(hour_data)
                for day_data in data.get('daily', []):

                    if day_data['date'] == date:
                       print(f"Weather for {date}:")
                       print(f"    Average Temperature: {day_data['temp']['day']}°C")
                       print(f"    Max Wind: {day_data['wind_speed']} kph")
                       print(f"    Total Precipitation: {day_data['precipitation']} mm")
                       print(f"    Condition: {day_data['weather']['description']}")
    
        else:
                weather_data = response.json()['forecast']['forecastday'][0]  
                print(f"Weather for {formatted_date.strftime('%Y-%m-%d')}:")
                display_daily_weather(weather_data)
    else:
             print(f"Failed to retrieve weather data. Status code: {response.status_code}")
             city = None
             lat = 0
             lon = 0
             requested_date = None
             weather_status = None
             requested_date = None
             weather_status = "failed"
             STTError = response.status_code


def display_daily_weather(daily_data):
    avg_temp_c = daily_data['day']['avgtemp_c']
    max_wind_kph = daily_data['day']['maxwind_kph']
    total_precip_mm = daily_data['day']['totalprecip_mm']
    condition = daily_data['day']['condition']['text']

    print(f"\tAverage Temperature: {avg_temp_c}°C")
    print(f"\tMax Wind: {max_wind_kph} kph")
    print(f"\tTotal Precipitation: {total_precip_mm} mm")
    print(f"\tCondition: {condition}")

def find_next_weekend():
    today = datetime.now()
    saturday = today + timedelta((5-today.weekday()) % 7)
    if today.weekday() > 5:  
        saturday += timedelta(days=7)
    return saturday

def is_time_in_target_period(hour_time, target_time_of_day):
       time_of_day_mapping = {
        'matin': 'morning',
        'après-midi': 'afternoon',
        'soir': 'evening',
        'nuit': 'night'
    }
    
       if target_time_of_day in time_of_day_mapping:
        target_time_of_day = time_of_day_mapping[target_time_of_day]
    
       if target_time_of_day == 'morning' and 6 <= hour_time.hour < 12:
        return True
       elif target_time_of_day == 'afternoon' and 12 <= hour_time.hour < 18:
        return True
       elif target_time_of_day in ['evening', 'night'] and (18 <= hour_time.hour < 24 or 0 <= hour_time.hour < 6):
        return True
    
       return False

def display_hourly_weather(hourly_data):

    temp_c = hourly_data['temp_c']
    condition = hourly_data['condition']['text']
    wind_kph = hourly_data['wind_kph']
    precip_mm = hourly_data['precip_mm'] if 'precip_mm' in hourly_data else 0  
    print(f"\tTemperature: {temp_c}°C")
    print(f"\tCondition: {condition}")
    print(f"\tWind: {wind_kph} kph")

    if precip_mm > 0:
        print(f"\tPrecipitation: {precip_mm} mm")

def parse_relative_date(text, languages):
    today = datetime.now()

    weekdays = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, ' thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6,
        'lundi': 0, 'mardi': 1, 'mercredi': 2, 'jeudi': 3, 'vendredi': 4, 'samedi': 5, 'dimanche': 6
    }
    for day, code in weekdays.items():
        if day in text.lower():
            return find_next_weekday(code, text)

    if 'today' in text.lower() or "aujourd'hui" in text.lower():
        return today
    elif 'tomorrow' in text.lower() or 'demain' in text.lower():
        return today + timedelta(days=1) 
    
    elif 'after tomorrow'in text.lower() or 'après-demain' in text.lower():
        return  today + timedelta(days=2) 

    return None



def find_next_weekday(weekday, text):
    today = datetime.now()
    days_ahead = weekday - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7

    return today + timedelta(days=days_ahead)

def extract_dates(text , languages=['en', 'fr']):
    if 'after tomorrow' in text.lower() or 'après-demain' in text.lower():
        target_date = datetime.now() + timedelta(days=2)
        return target_date.strftime("%Y-%m-%d"), None
    
    date_pattern = r'\b(?:\d{1,2}(?:st|nd|rd|th)?\s(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s\d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})\b'
    dates = re.findall(date_pattern, text)
    if dates:
        date_str = dates[0]
        try:
            # Handle different date formats
            for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d %B %Y"):
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    return parsed_date.strftime("%Y-%m-%d"), None  
                except ValueError:
                    continue
        except ValueError:
            print(f"Could not parse the date from input: {date_str}")
            city = None
            lat = 0
            lon = 0
            requested_date = None
            weather_status = None
            requested_date = None
            weather_status = "failed"
            STTError = 400

    target_time_of_day = None  
    date = dateparser.parse(text, languages=languages, settings={'PREFER_DATES_FROM': 'current_period'})
    print(date)
    if not date:
        date = parse_relative_date(text, languages)
        return date 
    if date:
        time_of_day_matches = re.search(r"morning|afternoon|evening|night|matin|après-midi|soir|nuit", text.lower())
        if time_of_day_matches:
            target_time_of_day = time_of_day_matches.group(0)
        formatted_date = date.strftime("%Y-%m-%d") 
        return formatted_date, target_time_of_day
    else:
        return None, target_time_of_day


def find_last_weekday(weekday):
    today = datetime.now()
    days_behind = today.weekday() - weekday
    if days_behind < 0:
        days_behind += 7
    return today - timedelta(days=days_behind)

def find_next_weekend():
    today = datetime.now()
    saturday = today + timedelta((5-today.weekday()) % 7)
    if today.weekday() > 5:  
        saturday += timedelta(days=7)
    return saturday

def get_weather_for_weekend(lat, lon, weekend_start_date):
    print(f"Fetching weather for Saturday, date: {weekend_start_date}")
    get_weather(lat, lon, weekend_start_date.strftime("%Y-%m-%d"))

    sunday_date = weekend_start_date + timedelta(days=1)
    print(f"Fetching weather for Sunday, date: {sunday_date}")
    get_weather(lat, lon, sunday_date.strftime("%Y-%m-%d"))

def get_date_only(datetime_obj):
    return datetime_obj.date()

def is_weather_query(text):
    weather_keywords = ['weather', 'temperature', 'météo' ,'forecast', 'rain', 'sunny', 'cloudy', 'wind', 'humidity']
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in weather_keywords)

def main():
    # text = recognize_from_microphone()
    text = "What's the forecast Alep  demain"
    
    if not is_weather_query(text):
        print("you are not ask  about the weather.")
        return 
    is_weekend_requested = 'weekend'  in text.lower()
    city = extract_city(text)
    print(city)
    
    coords = geocode_city(city)
    if coords :
            is_weekend_requested = 'week-end' in text.lower()
            if is_weekend_requested:
                weekend_start_date = find_next_weekend()
                print(f"Fetching weather for the weekend starting on: {weekend_start_date}")
                get_weather_for_weekend(coords['lat'], coords['lng'], weekend_start_date)
                requested_date =weekend_start_date
                weather_status = "ok" 
            elif not is_weekend_requested:
                 date_str, target_time_of_day = extract_dates(text)
                 print (date_str, target_time_of_day )
                 if date_str:
                   get_weather(coords['lat'], coords['lng'], date_str, target_time_of_day)
                   print(date_str, target_time_of_day)
                   requested_date = date_str
                   weather_status = "ok" 
            elif not text :
                 city = None
                 lat = 0
                 lon = 0
                 requested_date = None
                 weather_status = None
                 requested_date = None
                 weather_status = "failed"
                 STTError = 400
    if text : 
           
            stt_result = text
            stt_status =  200
            STTError = None
    else : 
            stt_result =  stt_status = None
            STTError = 404

    lat= coords['lat']
    lon = coords['lng']
    request_date = datetime.now()
    request_hour = datetime.now().hour
    cursor.execute(""" INSERT INTO WeatherRequests (RequestDate, RequestHour, City, Latitude, Longitude, RequestedDate, WeatherStatus, STTStatus, STTResult, STTError)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (request_date, request_hour, city, lat, lon, requested_date, weather_status, stt_status, stt_result , STTError ))
    conn.commit()
    conn.close()
if __name__ == "__main__":
    main()

