"""
Weather Alert System
====================
Generates weather warnings, reminders, and travel safety alerts.
Demonstrates: Rule-based AI, threshold checking, multiple alert types.
"""

from typing import List, Dict


class WeatherAlertSystem:
    """
    Analyzes weather data and generates intelligent alerts.
    Alert types: Temperature, Precipitation, Wind, Air Quality, Travel Safety.
    Demonstrates: OOP with multiple specialized methods.
    """

    # Severity levels
    LEVEL_INFO = 'info'
    LEVEL_WARNING = 'warning'
    LEVEL_DANGER = 'danger'

    def check_alerts(self, weather: Dict, forecast: List[Dict] = None) -> List[Dict]:
        """Main entry point: check all alert conditions."""
        alerts = []
        if not weather:
            return alerts

        # Current weather alerts
        alerts.extend(self._check_temperature(weather))
        alerts.extend(self._check_humidity(weather))
        alerts.extend(self._check_wind(weather))
        alerts.extend(self._check_current_condition(weather))

        # Forecast-based alerts
        if forecast:
            alerts.extend(self._check_forecast_warnings(forecast))

        # Add helpful reminders even when no warnings
        if not alerts:
            alerts.extend(self._get_general_reminders(weather))

        return alerts

    def _check_temperature(self, weather: Dict) -> List[Dict]:
        """Check temperature-related alerts."""
        alerts = []
        temp = weather.get('temperature', 20)
        feels = weather.get('feels_like', temp)

        if temp >= 40:
            alerts.append({
                'type': 'Extreme Heat',
                'icon': '🌡️🔥',
                'level': self.LEVEL_DANGER,
                'title': 'Extreme Heat Warning',
                'message': f'Dangerously hot at {temp}°C. Avoid outdoor activities between 11am–4pm. '
                          f'Drink water every 30 minutes. Seek air-conditioned spaces.'
            })
        elif temp >= 35:
            alerts.append({
                'type': 'High Heat',
                'icon': '🌡️',
                'level': self.LEVEL_WARNING,
                'title': 'High Temperature Alert',
                'message': f'It\'s {temp}°C — very hot. Stay hydrated, wear light clothing, '
                          f'use sunscreen, and limit time outdoors during midday.'
            })
        elif temp <= -10:
            alerts.append({
                'type': 'Severe Cold',
                'icon': '🥶❄️',
                'level': self.LEVEL_DANGER,
                'title': 'Severe Cold Warning',
                'message': f'Extreme cold at {temp}°C! Risk of frostbite on exposed skin in minutes. '
                          f'Wear heavy thermal layers, gloves, scarves, and hat.'
            })
        elif temp <= 0:
            alerts.append({
                'type': 'Freezing',
                'icon': '❄️',
                'level': self.LEVEL_WARNING,
                'title': 'Freezing Temperatures',
                'message': f'Temperature is {temp}°C — below freezing. Roads may be icy. '
                          f'Wear warm winter clothing and watch your step.'
            })

        # Feels-like discrepancy
        if abs(feels - temp) >= 5:
            if feels > temp:
                alerts.append({
                    'type': 'Heat Index',
                    'icon': '💧',
                    'level': self.LEVEL_INFO,
                    'title': 'High Humidity Heat Index',
                    'message': f'Air temperature is {temp}°C but feels like {feels}°C due to humidity. '
                              f'Take it slower than usual.'
                })
            else:
                alerts.append({
                    'type': 'Wind Chill',
                    'icon': '🌬️',
                    'level': self.LEVEL_INFO,
                    'title': 'Wind Chill Effect',
                    'message': f'Temperature is {temp}°C but feels like {feels}°C due to wind chill. '
                              f'Add an extra warm layer.'
                })

        return alerts

    def _check_humidity(self, weather: Dict) -> List[Dict]:
        """Check humidity alerts."""
        alerts = []
        humidity = weather.get('humidity', 50)
        temp = weather.get('temperature', 20)

        if humidity >= 85 and temp >= 28:
            alerts.append({
                'type': 'High Humidity',
                'icon': '💧',
                'level': self.LEVEL_WARNING,
                'title': 'Oppressive Humidity',
                'message': f'Humidity is {humidity}% — feels muggy and oppressive. '
                          f'Dehydration risk is higher. Drink water frequently.'
            })
        elif humidity <= 20:
            alerts.append({
                'type': 'Dry Air',
                'icon': '🏜️',
                'level': self.LEVEL_INFO,
                'title': 'Very Dry Air',
                'message': f'Humidity is only {humidity}%. Use moisturizer, lip balm, '
                          f'and drink extra water to prevent dehydration.'
            })

        return alerts

    def _check_wind(self, weather: Dict) -> List[Dict]:
        """Check wind alerts."""
        alerts = []
        wind = weather.get('wind_speed', 0)

        if wind >= 60:
            alerts.append({
                'type': 'Storm Wind',
                'icon': '🌪️',
                'level': self.LEVEL_DANGER,
                'title': 'Dangerous Wind Warning',
                'message': f'Wind speed at {wind} km/h — dangerous! Stay indoors, '
                          f'avoid trees and unstable structures. Flights may be delayed.'
            })
        elif wind >= 40:
            alerts.append({
                'type': 'Strong Wind',
                'icon': '💨',
                'level': self.LEVEL_WARNING,
                'title': 'Strong Wind Alert',
                'message': f'Strong winds at {wind} km/h. Secure loose items, '
                          f'be careful with umbrellas. Outdoor activities may be uncomfortable.'
            })
        elif wind >= 25:
            alerts.append({
                'type': 'Windy',
                'icon': '🌬️',
                'level': self.LEVEL_INFO,
                'title': 'Windy Conditions',
                'message': f'Moderate winds at {wind} km/h. Bring a windbreaker '
                          f'and prepare for breezy outdoor walking.'
            })

        return alerts

    def _check_current_condition(self, weather: Dict) -> List[Dict]:
        """Check current condition-based alerts."""
        alerts = []
        condition = weather.get('condition', '').lower()
        code = weather.get('weather_code', 0)

        if code in [95, 96, 99]:  # Thunderstorm
            alerts.append({
                'type': 'Thunderstorm',
                'icon': '⛈️',
                'level': self.LEVEL_DANGER,
                'title': 'Thunderstorm Active',
                'message': 'Thunderstorm in progress! Seek indoor shelter, avoid open areas, '
                          'tall trees, and water. Unplug electronics if possible.'
            })
        elif code in [65, 82]:  # Heavy rain
            alerts.append({
                'type': 'Heavy Rain',
                'icon': '🌧️',
                'level': self.LEVEL_WARNING,
                'title': 'Heavy Rainfall',
                'message': 'Heavy rain — flooding possible in low areas. Carry waterproof gear, '
                          'avoid driving through standing water.'
            })
        elif code in [75, 86]:  # Heavy snow
            alerts.append({
                'type': 'Heavy Snow',
                'icon': '❄️',
                'level': self.LEVEL_WARNING,
                'title': 'Heavy Snow Warning',
                'message': 'Heavy snowfall expected. Roads may be hazardous, '
                          'flights/trains delays possible. Dress warmly in waterproof layers.'
            })
        elif code in [45, 48]:  # Fog
            alerts.append({
                'type': 'Fog',
                'icon': '🌫️',
                'level': self.LEVEL_WARNING,
                'title': 'Foggy Conditions',
                'message': 'Heavy fog reduces visibility. Drive carefully, plan extra time '
                          'for travel. Sightseeing photos may be affected.'
            })
        elif 'rain' in condition or code in [51, 53, 55, 61, 63, 80, 81]:
            alerts.append({
                'type': 'Rain',
                'icon': '🌧️',
                'level': self.LEVEL_INFO,
                'title': 'Rain Expected',
                'message': 'Light to moderate rain. Bring an umbrella or rain jacket. '
                          'Indoor attractions are a good plan today.'
            })

        return alerts

    def _check_forecast_warnings(self, forecast: List[Dict]) -> List[Dict]:
        """Check forecast for upcoming severe weather."""
        alerts = []

        # Look ahead for severe weather in next 3 days
        for i, day in enumerate(forecast[:3]):
            code = day.get('weather_code', 0)
            if code in [95, 96, 99]:
                alerts.append({
                    'type': 'Upcoming Storm',
                    'icon': '⛈️',
                    'level': self.LEVEL_WARNING,
                    'title': f'Storm Expected on {day["short_date"]}',
                    'message': f'Thunderstorm forecast for {day["day_name"]} ({day["short_date"]}). '
                              f'Plan indoor activities or adjust your itinerary.'
                })
                break

        # Check temperature swings
        if len(forecast) >= 2:
            tomorrow = forecast[1]
            today = forecast[0]
            temp_change = tomorrow['temp_max'] - today['temp_max']
            if abs(temp_change) >= 10:
                direction = 'cooler' if temp_change < 0 else 'warmer'
                alerts.append({
                    'type': 'Temperature Change',
                    'icon': '📉' if temp_change < 0 else '📈',
                    'level': self.LEVEL_INFO,
                    'title': f'Big Temperature Change Tomorrow',
                    'message': f'Tomorrow will be {abs(temp_change)}°C {direction} than today. '
                              f'Adjust your clothing accordingly.'
                })

        return alerts

    def _get_general_reminders(self, weather: Dict) -> List[Dict]:
        """Provide helpful reminders when no warnings exist."""
        reminders = []
        temp = weather.get('temperature', 20)
        condition = weather.get('condition', '').lower()

        if 'clear' in condition or 'sun' in condition:
            if temp > 20:
                reminders.append({
                    'type': 'UV Reminder',
                    'icon': '☀️',
                    'level': self.LEVEL_INFO,
                    'title': 'Perfect Weather',
                    'message': 'Beautiful sunny conditions! Don\'t forget sunscreen and sunglasses. '
                              'Great day for outdoor sightseeing.'
                })
        elif 'cloud' in condition:
            reminders.append({
                'type': 'Mild Weather',
                'icon': '⛅',
                'level': self.LEVEL_INFO,
                'title': 'Comfortable Conditions',
                'message': 'Pleasant cloudy weather — ideal for walking tours without harsh sun.'
            })

        return reminders
