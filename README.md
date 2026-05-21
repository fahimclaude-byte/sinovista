# 🏯 SinoVista (华境) — A Beautiful View of China

> **AI-Powered China City Weather & Travel Recommender**
> Final Project · Object-Oriented Technology

SinoVista is a professional Flask web application that lets users explore **45+ Chinese cities** across **all major provinces**, view **real-time weather** with **5-day forecasts**, receive **intelligent weather alerts**, and get **AI-generated personalized travel itineraries** based on actual weather conditions.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🌏 **45+ Cities** | All major Chinese cities across 30+ provinces |
| 🌡️ **Real-Time Weather** | Live data from Open-Meteo API (no API key required) |
| 📅 **5-Day Forecasts** | Temperature, precipitation, wind, conditions |
| ⚠️ **Smart Alerts** | Extreme heat, cold, storms, fog, wind, humidity warnings |
| 🤖 **AI Recommendations** | Personalized itineraries based on weather + preferences |
| 💬 **AI Chat Assistant** | Natural-language Q&A about any Chinese city |
| 🎨 **Professional Design** | Elegant Chinese-inspired UI with custom typography |

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Python
You need **Python 3.8 or higher**. Check by running:
```bash
python --version
```

### Step 2: Install Dependencies
Open terminal/command prompt in the `SinoVista` folder and run:
```bash
pip install -r requirements.txt
```

If `pip` doesn't work, try:
```bash
python -m pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

You should see:
```
============================================================
  SinoVista - China Weather & AI Travel Recommender
============================================================
  Total cities loaded: 45
  Provinces covered: 30+
============================================================
  Server starting at: http://localhost:5000
============================================================
```

Open your browser and go to: **http://localhost:5000**

---

## 🤖 (Optional) Enable Real AI Mode

By default, the app uses a **smart template engine** that works **offline** and produces professional-quality recommendations. This works perfectly for demos and grading.

If you want to enable a **real Large Language Model (LLM)** for even more dynamic responses:

1. Open `config.py`
2. Replace `"YOUR_API_KEY_HERE"` with your API key from one of these providers:
   - **DeepSeek** (recommended, cheap, China-friendly): https://platform.deepseek.com
   - **OpenAI**: https://platform.openai.com
   - **Tongyi Qianwen** (Alibaba): https://dashscope.console.aliyun.com
3. Save and restart the app

The app automatically detects the key and switches to LLM mode.

---

## 📂 Project Structure

```
SinoVista/
├── app.py                       # Main Flask application
├── config.py                    # AI API configuration
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── models/                      # OOP Business Logic Layer
│   ├── __init__.py
│   ├── city_manager.py          # City & CityManager classes
│   ├── weather_service.py       # WeatherService class
│   ├── ai_recommender.py        # AIRecommender class
│   └── weather_alert.py         # WeatherAlertSystem class
│
├── data/
│   └── cities.json              # 45 China cities database
│
├── templates/                   # Jinja2 HTML templates
│   ├── base.html                # Base layout with nav + footer
│   ├── index.html               # Homepage
│   ├── cities.html              # All cities listing
│   ├── city_detail.html         # Individual city + AI panel
│   ├── alerts.html              # Weather alerts page
│   ├── about.html               # About the project
│   └── 404.html                 # Error page
│
└── static/
    ├── css/style.css            # Complete styling
    └── js/
        ├── main.js              # Global UI + AI chat
        └── city.js              # AI recommendation form
```

---

## 🏗️ Architecture (Object-Oriented Design)

SinoVista demonstrates four core OOP classes:

### 1. `City` & `CityManager`
- **City** — encapsulates a single city (name, province, coordinates, highlights, cuisine)
- **CityManager** — manages the collection: search, filter, retrieve

### 2. `WeatherService`
- Fetches real-time weather from Open-Meteo API
- **Intelligent fallback**: if API fails, switches to climate-based simulation
- Demonstrates the **Strategy pattern**

### 3. `AIRecommender`
- Generates travel recommendations based on weather + preferences
- **Dual-mode**: LLM API mode OR smart template mode
- Uses **prompt engineering** principles

### 4. `WeatherAlertSystem`
- Rule-based AI for safety warnings
- Three severity levels: info, warning, danger
- Checks temperature, humidity, wind, precipitation, fog

---

## 🎬 How to Demo (For Your Presentation)

1. **Open homepage** → show hero, search box, featured cities
2. **Search "Beijing"** in hero search → autocomplete dropdown
3. **Click Beijing card** → live weather + 5-day forecast + alerts
4. **Click "Generate AI Recommendation"** → fill form → wait → see structured AI output
5. **Open chat widget** (bottom-right) → ask: *"What food should I try in Chengdu?"*
6. **Visit Alerts page** → show warnings across all cities
7. **Visit a cold/hot city** like Harbin or Sanya → show different alert types

---

## 🛠️ Troubleshooting

**Problem: "ModuleNotFoundError: No module named 'flask'"**
→ Run `pip install -r requirements.txt` again.

**Problem: "Port 5000 is already in use"**
→ Edit the last line of `app.py` and change `port=5000` to `port=8000`.

**Problem: Weather shows "Climate Simulation" instead of real data**
→ This is normal if you have no internet. The app still works fully.

**Problem: AI recommendation looks like a template**
→ This is the **smart template mode**. To get real LLM responses, add an API key to `config.py` (see "Enable Real AI Mode" section above).

---

## 📜 Course Information

- **Course:** Object-Oriented Technology
- **Project Type:** Final Course Project
- **Project Topic:** City/Region Data Collector & AI-Powered Recommendation
- **Language:** Python 3
- **Framework:** Flask
- **Demonstrated Concepts:** OOP (Encapsulation, Polymorphism, Strategy Pattern), API Integration, Prompt Engineering, MVC Architecture, Responsive Web Design

---

© 2026 SinoVista — Built for the love of Chinese culture & technology 🇨🇳
