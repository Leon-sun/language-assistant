"""
Location service for resolving user location from various sources.
"""
import requests
import logging
from typing import Dict, Optional, Tuple
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

# Default fallback location (Ottawa, Canada)
DEFAULT_LATITUDE = 45.4247
DEFAULT_LONGITUDE = -75.6950
DEFAULT_CITY = "Ottawa, CA"


def get_client_ip(request) -> str:
    """
    Safely extract client IP address from request.
    Checks X-Forwarded-For header first (for proxies), then REMOTE_ADDR.
    
    Args:
        request: Django request object
    
    Returns:
        str: Client IP address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # X-Forwarded-For can contain multiple IPs, take the first one
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def geocode_city(city_name: str) -> Optional[Dict[str, any]]:
    """
    Geocode a city name to latitude/longitude using Nominatim (OpenStreetMap).
    Results are cached for 24 hours.
    
    Args:
        city_name: Name of the city to geocode
    
    Returns:
        dict: Contains 'latitude', 'longitude', 'city', 'country' if successful
        None: If geocoding fails
    """
    if not city_name or not city_name.strip():
        return None
    
    city_name = city_name.strip()
    
    # Check cache first
    cache_key = f"geocode_{city_name.lower()}"
    cached_result = cache.get(cache_key)
    if cached_result:
        logger.info(f"Using cached geocoding result for: {city_name}")
        return cached_result
    
    try:
        # Use Nominatim (OpenStreetMap) geocoding API (free, no key required)
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': city_name,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'Dictionary-Project/1.0'  # Required by Nominatim
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data and len(data) > 0:
            result = data[0]
            location_data = {
                'latitude': float(result.get('lat', 0)),
                'longitude': float(result.get('lon', 0)),
                'city': result.get('address', {}).get('city') or 
                        result.get('address', {}).get('town') or 
                        result.get('address', {}).get('village') or
                        city_name,
                'country': result.get('address', {}).get('country', ''),
                'display_name': result.get('display_name', city_name)
            }
            
            # Cache for 24 hours (86400 seconds)
            cache.set(cache_key, location_data, 86400)
            logger.info(f"Geocoded '{city_name}' to {location_data['latitude']}, {location_data['longitude']}")
            
            return location_data
        else:
            logger.warning(f"No geocoding results found for: {city_name}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error geocoding city '{city_name}': {str(e)}")
        return None
    except (ValueError, KeyError) as e:
        logger.error(f"Error parsing geocoding response for '{city_name}': {str(e)}")
        return None


def geolocate_by_ip(ip_address: str) -> Optional[Dict[str, any]]:
    """
    Get approximate location from IP address using ip-api.com (free tier).
    
    Args:
        ip_address: IP address to geolocate
    
    Returns:
        dict: Contains 'latitude', 'longitude', 'city', 'country' if successful
        None: If IP geolocation fails
    """
    if not ip_address or ip_address in ['127.0.0.1', 'localhost', '::1']:
        logger.warning(f"Invalid or localhost IP address: {ip_address}")
        return None
    
    # Check cache first
    cache_key = f"ipgeo_{ip_address}"
    cached_result = cache.get(cache_key)
    if cached_result:
        logger.info(f"Using cached IP geolocation result for: {ip_address}")
        return cached_result
    
    try:
        # Use ip-api.com (free, no key required for basic usage)
        url = f"http://ip-api.com/json/{ip_address}"
        params = {
            'fields': 'status,message,country,regionName,city,lat,lon'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') == 'success':
            location_data = {
                'latitude': float(data.get('lat', 0)),
                'longitude': float(data.get('lon', 0)),
                'city': data.get('city', ''),
                'country': data.get('country', ''),
                'region': data.get('regionName', ''),
                'display_name': f"{data.get('city', '')}, {data.get('country', '')}".strip(', ')
            }
            
            # Cache for 24 hours
            cache.set(cache_key, location_data, 86400)
            logger.info(f"IP geolocation for {ip_address}: {location_data['display_name']}")
            
            return location_data
        else:
            logger.warning(f"IP geolocation failed for {ip_address}: {data.get('message', 'Unknown error')}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error geolocating IP '{ip_address}': {str(e)}")
        return None
    except (ValueError, KeyError) as e:
        logger.error(f"Error parsing IP geolocation response for '{ip_address}': {str(e)}")
        return None


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """
    Validate that coordinates are within valid ranges.
    
    Args:
        latitude: Latitude value
        longitude: Longitude value
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        lat = float(latitude)
        lon = float(longitude)
        return -90 <= lat <= 90 and -180 <= lon <= 180
    except (ValueError, TypeError):
        return False


def resolve_location(request) -> Dict[str, any]:
    """
    Resolve user location using priority order:
    A) GPS coordinates from request (lat/lon query params)
    B) City name from request (geocode to lat/lon)
    C) IP-based geolocation
    D) Default location (Ottawa)
    
    Args:
        request: Django request object
    
    Returns:
        dict: Contains 'latitude', 'longitude', 'city', 'source', 'display_name'
              source is one of: 'gps', 'city', 'ip', 'default'
    """
    # Priority A: GPS coordinates from request
    lat_param = request.GET.get('lat') or request.POST.get('lat')
    lon_param = request.GET.get('lon') or request.POST.get('lon')
    
    if lat_param and lon_param:
        try:
            latitude = float(lat_param)
            longitude = float(lon_param)
            
            if validate_coordinates(latitude, longitude):
                logger.info(f"Using GPS coordinates from request: {latitude}, {longitude}")
                return {
                    'latitude': latitude,
                    'longitude': longitude,
                    'city': 'GPS Location',
                    'country': '',
                    'source': 'gps',
                    'display_name': f"GPS Location ({latitude:.4f}, {longitude:.4f})"
                }
            else:
                logger.warning(f"Invalid GPS coordinates: {latitude}, {longitude}")
        except (ValueError, TypeError):
            logger.warning(f"Could not parse GPS coordinates: {lat_param}, {lon_param}")
    
    # Priority B: City name from request
    city_param = request.GET.get('city') or request.POST.get('city')
    if city_param:
        location_data = geocode_city(city_param)
        if location_data:
            logger.info(f"Using geocoded city: {city_param}")
            location_data['source'] = 'city'
            return location_data
        else:
            logger.warning(f"Geocoding failed for city: {city_param}")
    
    # Priority C: IP-based geolocation
    client_ip = get_client_ip(request)
    if client_ip:
        location_data = geolocate_by_ip(client_ip)
        if location_data:
            logger.info(f"Using IP-based geolocation for IP: {client_ip}")
            location_data['source'] = 'ip'
            location_data['is_approximate'] = True
            return location_data
        else:
            logger.warning(f"IP geolocation failed for IP: {client_ip}")
    
    # Priority D: Default location
    logger.info(f"Using default location: {DEFAULT_CITY}")
    return {
        'latitude': DEFAULT_LATITUDE,
        'longitude': DEFAULT_LONGITUDE,
        'city': DEFAULT_CITY,
        'country': 'CA',
        'source': 'default',
        'display_name': DEFAULT_CITY,
        'is_default': True
    }
