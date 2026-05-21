"""
CityManager Module
==================
Object-Oriented module for managing China city data.
Demonstrates: Encapsulation, Class Methods, Data Management.
"""

import json
import os
from typing import List, Dict, Optional


class City:
    """
    Represents a single Chinese city.
    Demonstrates: OOP class with attributes and methods.
    """

    def __init__(self, data: dict):
        self.name = data.get('name', '')
        self.name_cn = data.get('name_cn', '')
        self.province = data.get('province', '')
        self.lat = data.get('lat', 0.0)
        self.lon = data.get('lon', 0.0)
        self.population = data.get('population', '')
        self.featured = data.get('featured', False)
        self.description = data.get('description', '')
        self.highlights = data.get('highlights', [])
        self.cuisine = data.get('cuisine', [])
        self.best_season = data.get('best_season', '')

    def to_dict(self) -> dict:
        """Convert city object to dictionary."""
        return {
            'name': self.name,
            'name_cn': self.name_cn,
            'province': self.province,
            'lat': self.lat,
            'lon': self.lon,
            'population': self.population,
            'featured': self.featured,
            'description': self.description,
            'highlights': self.highlights,
            'cuisine': self.cuisine,
            'best_season': self.best_season
        }

    def __repr__(self):
        return f"<City: {self.name} ({self.name_cn}), {self.province}>"


class CityManager:
    """
    Manages the database of Chinese cities.
    Demonstrates: Singleton-like design, data filtering, search operations.
    """

    def __init__(self, data_file: str = None):
        if data_file is None:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_file = os.path.join(base, 'data', 'cities.json')

        self._data_file = data_file
        self._cities = []
        self._load_cities()

    def _load_cities(self) -> None:
        """Load cities from JSON file (private method)."""
        try:
            with open(self._data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._cities = [City(c) for c in data.get('cities', [])]
        except FileNotFoundError:
            print(f"Warning: City data file not found at {self._data_file}")
            self._cities = []
        except json.JSONDecodeError as e:
            print(f"Error parsing city data: {e}")
            self._cities = []

    def get_all_cities(self) -> List[dict]:
        """Return all cities as dictionaries."""
        return [city.to_dict() for city in self._cities]

    def get_featured_cities(self) -> List[dict]:
        """Return only featured cities for homepage."""
        return [city.to_dict() for city in self._cities if city.featured]

    def get_city(self, city_name: str) -> Optional[dict]:
        """Find a city by English or Chinese name (case-insensitive)."""
        if not city_name:
            return None
        query = city_name.lower().strip()
        for city in self._cities:
            if (city.name.lower() == query or
                city.name_cn == city_name.strip() or
                city.name.lower().replace("'", "") == query.replace("'", "")):
                return city.to_dict()
        return None

    def search_cities(self, query: str) -> List[dict]:
        """Search cities by name, province, or description."""
        if not query:
            return self.get_all_cities()
        query = query.lower().strip()
        results = []
        for city in self._cities:
            if (query in city.name.lower() or
                query in city.name_cn or
                query in city.province.lower() or
                query in city.description.lower()):
                results.append(city.to_dict())
        return results

    def get_cities_by_province(self, province: str) -> List[dict]:
        """Filter cities by province."""
        return [city.to_dict() for city in self._cities
                if city.province.lower() == province.lower()]

    def get_all_provinces(self) -> List[str]:
        """Return list of all unique provinces."""
        provinces = sorted(set(city.province for city in self._cities))
        return provinces

    def get_total_count(self) -> int:
        """Return total number of cities in database."""
        return len(self._cities)
