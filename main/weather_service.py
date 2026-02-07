import requests
import logging

logger = logging.getLogger(__name__)


def get_weather_data(latitude, longitude):
    """
    Fetch weather data from Open-Meteo API.
    
    Args:
        latitude: Latitude coordinate (float)
        longitude: Longitude coordinate (float)
    
    Returns:
        dict: Weather data containing current temperature, wind speed, and hourly forecast
        None: If API call fails
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,wind_speed_10m,weather_code',
            'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code',
            'timezone': 'auto'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract current weather
        current = data.get('current', {})
        hourly = data.get('hourly', {})
        
        weather_info = {
            'temperature': current.get('temperature_2m'),
            'wind_speed': current.get('wind_speed_10m'),
            'weather_code': current.get('weather_code'),
            'time': current.get('time'),
            'hourly_temperatures': hourly.get('temperature_2m', [])[:24],  # Next 24 hours
            'hourly_humidity': hourly.get('relative_humidity_2m', [])[:24],
            'hourly_wind_speed': hourly.get('wind_speed_10m', [])[:24],
            'hourly_weather_codes': hourly.get('weather_code', [])[:24],
        }
        
        return weather_info
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in weather service: {str(e)}")
        return None


def get_weather_description(weather_code):
    """
    Convert WMO weather code to human-readable description.
    
    Args:
        weather_code: WMO Weather Interpretation Code (0-99)
    
    Returns:
        str: Weather description
    """
    # WMO Weather Interpretation Codes (simplified)
    weather_descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }
    
    return weather_descriptions.get(weather_code, "Unknown weather condition")
