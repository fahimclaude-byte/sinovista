"""
SinoVista - China City Weather & AI Travel Recommender
========================================================
Main Flask Application
Author: [Your Name]
Course: Object-Oriented Technology - Final Project
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from models.city_manager import CityManager
from models.weather_service import WeatherService
from models.ai_recommender import AIRecommender
from models.weather_alert import WeatherAlertSystem
import json
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sinovista-2026-china-weather-ai'

# Initialize core OOP components
city_manager = CityManager()
weather_service = WeatherService()
ai_recommender = AIRecommender()
alert_system = WeatherAlertSystem()


# ============================================================
# ROUTES - Web Pages
# ============================================================

@app.route('/')
def home():
    """Homepage - Display featured cities and search."""
    featured_cities = city_manager.get_featured_cities()
    total_cities = city_manager.get_total_count()
    provinces = city_manager.get_all_provinces()
    return render_template('index.html',
                           featured_cities=featured_cities,
                           total_cities=total_cities,
                           provinces=provinces)


@app.route('/cities')
def cities():
    """Display all China cities with filter options."""
    province = request.args.get('province', '')
    search = request.args.get('search', '')

    if search:
        all_cities = city_manager.search_cities(search)
    elif province:
        all_cities = city_manager.get_cities_by_province(province)
    else:
        all_cities = city_manager.get_all_cities()

    provinces = city_manager.get_all_provinces()
    return render_template('cities.html',
                           cities=all_cities,
                           provinces=provinces,
                           selected_province=province,
                           search_query=search)


@app.route('/city/<city_name>')
def city_detail(city_name):
    """Show detailed weather + AI recommendations for a specific city."""
    city = city_manager.get_city(city_name)
    if not city:
        return render_template('404.html'), 404

    # Get current weather and forecast
    weather_data = weather_service.get_current_weather(city)
    forecast = weather_service.get_forecast(city, days=5)

    # Generate weather alerts
    alerts = alert_system.check_alerts(weather_data, forecast)

    return render_template('city_detail.html',
                           city=city,
                           weather=weather_data,
                           forecast=forecast,
                           alerts=alerts)


@app.route('/alerts')
def all_alerts():
    """Display weather alerts across all major cities."""
    major_cities = city_manager.get_featured_cities()
    all_alerts = []
    for city in major_cities:
        weather = weather_service.get_current_weather(city)
        forecast = weather_service.get_forecast(city, days=3)
        city_alerts = alert_system.check_alerts(weather, forecast)
        for alert in city_alerts:
            alert['city'] = city['name']
            alert['city_cn'] = city['name_cn']
            all_alerts.append(alert)
    return render_template('alerts.html', alerts=all_alerts)


@app.route('/about')
def about():
    """About page describing the project."""
    return render_template('about.html')


@app.route('/map')
def map_page():
    """Interactive China Map page."""
    cities = city_manager.get_all_cities()
    return render_template('map.html', cities=cities)


@app.route('/compare')
def compare_page():
    """Weather comparison page for multiple cities."""
    cities = city_manager.get_all_cities()
    return render_template('compare.html', cities=cities)


@app.route('/quiz')
def quiz_page():
    """China Knowledge Quiz Game."""
    return render_template('quiz.html')


@app.route('/favorites')
def favorites_page():
    """Favorites page (uses localStorage on frontend)."""
    cities = city_manager.get_all_cities()
    return render_template('favorites.html', cities=cities)


# ============================================================
# API ENDPOINTS - For AJAX calls
# ============================================================

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    """Generate AI-powered travel recommendations."""
    data = request.get_json()
    city_name = data.get('city')
    preference = data.get('preference', 'general')
    budget = data.get('budget', 'medium')
    duration = data.get('duration', '3 days')

    city = city_manager.get_city(city_name)
    if not city:
        return jsonify({'error': 'City not found'}), 404

    weather = weather_service.get_current_weather(city)
    forecast = weather_service.get_forecast(city, days=5)

    recommendation = ai_recommender.generate_recommendation(
        city=city,
        weather=weather,
        forecast=forecast,
        preference=preference,
        budget=budget,
        duration=duration
    )

    return jsonify({'recommendation': recommendation, 'status': 'success'})


@app.route('/api/weather/<city_name>')
def api_weather(city_name):
    """Get weather data for a city via API."""
    city = city_manager.get_city(city_name)
    if not city:
        return jsonify({'error': 'City not found'}), 404

    weather = weather_service.get_current_weather(city)
    forecast = weather_service.get_forecast(city, days=5)
    return jsonify({
        'city': city,
        'weather': weather,
        'forecast': forecast
    })


@app.route('/api/chat', methods=['POST'])
def api_chat():
    """AI chatbot for travel questions."""
    data = request.get_json()
    user_message = data.get('message', '')
    city_name = data.get('city', None)

    city = city_manager.get_city(city_name) if city_name else None
    weather = weather_service.get_current_weather(city) if city else None

    response = ai_recommender.chat(user_message, city=city, weather=weather)
    return jsonify({'response': response})


@app.route('/api/cities/search')
def api_search_cities():
    """Quick search API for autocomplete."""
    query = request.args.get('q', '')
    results = city_manager.search_cities(query)[:10]
    return jsonify({'cities': results})


@app.route('/api/compare', methods=['POST'])
def api_compare():
    """Compare weather of multiple cities."""
    data = request.get_json()
    city_names = data.get('cities', [])

    results = []
    for name in city_names[:4]:  # Max 4 cities
        city = city_manager.get_city(name)
        if city:
            weather = weather_service.get_current_weather(city)
            forecast = weather_service.get_forecast(city, days=5)
            results.append({
                'city': city,
                'weather': weather,
                'forecast': forecast
            })

    return jsonify({'comparisons': results})


@app.route('/api/cities/all')
def api_all_cities():
    """Get all cities (for map and other features)."""
    cities = city_manager.get_all_cities()
    return jsonify({'cities': cities})


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("  SinoVista - China Weather & AI Travel Recommender")
    print("=" * 60)
    print(f"  Total cities loaded: {city_manager.get_total_count()}")
    print(f"  Provinces covered: {len(city_manager.get_all_provinces())}")
    print("=" * 60)
    print("  Server starting at: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
