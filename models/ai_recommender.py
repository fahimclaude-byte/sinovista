"""
AI Recommender Module
=====================
Generates AI-powered travel recommendations based on weather, city,
and user preferences.

This module supports TWO modes:
1. **LLM Mode (recommended for demos)**: Uses an LLM API (DeepSeek, OpenAI,
   Tongyi/Qwen, etc.) if an API key is set in config.py.
2. **Smart Template Mode (default)**: Uses sophisticated rule-based logic
   with prompt engineering principles so it works offline and without
   API costs. Output is genuinely useful and reads like AI-generated text.

To activate LLM mode, edit config.py and set AI_API_KEY + AI_PROVIDER.
"""

import random
from typing import Dict, List, Optional

try:
    from config import AI_API_KEY, AI_PROVIDER, AI_MODEL, AI_BASE_URL
    LLM_AVAILABLE = bool(AI_API_KEY and AI_API_KEY != "YOUR_API_KEY_HERE")
except ImportError:
    LLM_AVAILABLE = False
    AI_API_KEY = AI_PROVIDER = AI_MODEL = AI_BASE_URL = None


class AIRecommender:
    """
    Generates intelligent travel recommendations.
    Demonstrates: Strategy pattern, prompt engineering, polymorphism.
    """

    def __init__(self):
        self.llm_available = LLM_AVAILABLE
        if self.llm_available:
            print(f"[AIRecommender] Using LLM provider: {AI_PROVIDER}")
        else:
            print("[AIRecommender] Using smart template engine (no API key configured)")

    # ============ PUBLIC METHODS ============

    def generate_recommendation(self, city: Dict, weather: Dict, forecast: List[Dict],
                                preference: str = 'general', budget: str = 'medium',
                                duration: str = '3 days') -> str:
        """Main entry point: generate a personalized travel recommendation."""
        if self.llm_available:
            try:
                return self._llm_recommendation(city, weather, forecast,
                                                preference, budget, duration)
            except Exception as e:
                print(f"[AIRecommender] LLM call failed: {e}, falling back.")

        return self._template_recommendation(city, weather, forecast,
                                             preference, budget, duration)

    def chat(self, message: str, city: Optional[Dict] = None,
             weather: Optional[Dict] = None) -> str:
        """Chatbot for travel questions."""
        if self.llm_available:
            try:
                return self._llm_chat(message, city, weather)
            except Exception as e:
                print(f"[AIRecommender] LLM chat failed: {e}")

        return self._template_chat(message, city, weather)

    # ============ LLM IMPLEMENTATION ============

    def _llm_recommendation(self, city, weather, forecast, preference, budget, duration):
        """Generate via LLM API using carefully engineered prompts."""
        import requests

        # ----- Prompt Engineering -----
        # Role: travel expert. Context: current conditions. Format: structured.
        system_prompt = (
            "You are SinoVista AI, an expert China travel advisor with deep knowledge "
            "of Chinese cities, culture, cuisine, and weather. Provide warm, personalized, "
            "and practical travel recommendations. Always format responses with clear "
            "headings using markdown (## for sections). Be specific and actionable."
        )

        forecast_summary = "\n".join([
            f"  • {f['short_date']}: {f['condition']}, {f['temp_min']}°C–{f['temp_max']}°C"
            for f in forecast[:5]
        ])

        user_prompt = f"""I'm planning a {duration} trip to {city['name']} ({city['name_cn']}) in {city['province']}.

**Current Weather:** {weather['condition']}, {weather['temperature']}°C (feels like {weather['feels_like']}°C), humidity {weather['humidity']}%

**5-Day Forecast:**
{forecast_summary}

**My preferences:** {preference}
**Budget:** {budget}

Please provide a personalized recommendation covering:
## Trip Overview
A brief 2-sentence intro tailored to the weather conditions.

## Day-by-Day Suggested Itinerary
Specific activities for each day based on the actual weather forecast.

## What to Pack
Weather-specific clothing and items.

## Must-Try Local Food
3-4 dishes specific to {city['name']}.

## Insider Tip
One unique tip locals would give.

Keep the total response under 500 words and friendly in tone."""

        headers = {
            "Authorization": f"Bearer {AI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": AI_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        response = requests.post(AI_BASE_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']

    def _llm_chat(self, message, city, weather):
        """LLM-powered chat."""
        import requests

        context = ""
        if city:
            context += f"\nUser is interested in: {city['name']} ({city['name_cn']}), {city['province']}."
        if weather:
            context += f"\nCurrent weather there: {weather['condition']}, {weather['temperature']}°C."

        system_prompt = (
            "You are SinoVista AI, a friendly China travel assistant. "
            f"Answer questions about Chinese cities, weather, food, and travel. "
            f"Keep responses concise (under 150 words) and helpful.{context}"
        )

        headers = {"Authorization": f"Bearer {AI_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": AI_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "temperature": 0.8,
            "max_tokens": 300
        }
        response = requests.post(AI_BASE_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

    # ============ SMART TEMPLATE IMPLEMENTATION ============

    def _template_recommendation(self, city, weather, forecast, preference, budget, duration):
        """Generate recommendation using prompt-engineering-inspired templates."""

        temp = weather['temperature']
        condition = weather['condition'].lower()
        weather_code = weather.get('weather_code', 0)

        # ---- Analyze weather pattern over forecast ----
        rainy_days = sum(1 for f in forecast if f['weather_code'] >= 51 and f['weather_code'] < 90)
        sunny_days = sum(1 for f in forecast if f['weather_code'] <= 2)
        avg_high = sum(f['temp_max'] for f in forecast) / len(forecast)
        avg_low = sum(f['temp_min'] for f in forecast) / len(forecast)

        # ---- Build trip overview ----
        overview = self._build_overview(city, weather, avg_high, avg_low, rainy_days, sunny_days)

        # ---- Build itinerary ----
        itinerary = self._build_itinerary(city, forecast, preference, duration)

        # ---- What to pack ----
        packing = self._build_packing_list(temp, avg_low, avg_high, rainy_days, weather_code)

        # ---- Food recommendations ----
        food = self._build_food_section(city, weather, preference)

        # ---- Insider tip ----
        tip = self._build_insider_tip(city, weather, preference)

        # ---- Budget note ----
        budget_note = self._build_budget_note(budget, city, duration)

        # Assemble final recommendation
        recommendation = f"""## ✨ Trip Overview
{overview}

## 🗓️ Suggested Itinerary
{itinerary}

## 🎒 What to Pack
{packing}

## 🍜 Must-Try Local Food
{food}

## 💡 Insider Tip
{tip}

## 💰 Budget Estimate
{budget_note}

---
*Generated by SinoVista AI Travel Advisor based on real-time weather analysis.*"""

        return recommendation

    def _build_overview(self, city, weather, avg_high, avg_low, rainy_days, sunny_days):
        """Build personalized trip overview."""
        condition_word = weather['condition'].lower()

        if 'rain' in condition_word or 'drizzle' in condition_word:
            mood = "rainy and refreshing"
        elif 'snow' in condition_word:
            mood = "snowy and magical"
        elif 'clear' in condition_word or 'sun' in condition_word:
            mood = "bright and sunny"
        elif 'cloud' in condition_word:
            mood = "cool and comfortable"
        elif 'fog' in condition_word:
            mood = "misty and atmospheric"
        else:
            mood = "pleasant"

        weekly_summary = ""
        if sunny_days >= 3:
            weekly_summary = " The week ahead looks mostly sunny — perfect for outdoor sightseeing!"
        elif rainy_days >= 3:
            weekly_summary = " Expect quite a bit of rain this week, so indoor cultural sites will be your best friends."
        else:
            weekly_summary = " The weather will be mixed, giving you a balanced mix of indoor and outdoor activities."

        return (f"{city['name']} ({city['name_cn']}) is currently {mood} at {weather['temperature']}°C. "
                f"{city['description']}{weekly_summary} Average temperatures will range from "
                f"{round(avg_low)}°C to {round(avg_high)}°C.")

    def _build_itinerary(self, city, forecast, preference, duration):
        """Build day-by-day itinerary based on actual forecast."""
        # Determine number of days
        if '1' in duration:
            n_days = 1
        elif '2' in duration:
            n_days = 2
        elif '5' in duration or 'week' in duration.lower():
            n_days = min(5, len(forecast))
        elif '7' in duration:
            n_days = min(7, len(forecast))
        else:
            n_days = min(3, len(forecast))

        highlights = city['highlights']
        itinerary_lines = []

        outdoor_activities = highlights[:]
        indoor_alternatives = self._get_indoor_alternatives(city)

        used_outdoor = set()
        used_indoor = set()

        for i in range(n_days):
            if i < len(forecast):
                day = forecast[i]
                is_rainy = day['weather_code'] >= 51 and day['weather_code'] < 90
                is_cold = day['temp_max'] < 5
                is_hot = day['temp_max'] > 32

                day_label = f"**Day {i+1} ({day['short_date']}, {day['condition']}, {day['temp_min']}°C–{day['temp_max']}°C):**"

                if is_rainy:
                    available = [a for a in indoor_alternatives if a not in used_indoor]
                    activity = available[0] if available else "Explore covered markets and museums"
                    used_indoor.add(activity)
                    reason = "with rain expected, focus on indoor experiences"
                elif is_cold:
                    available = [a for a in indoor_alternatives if a not in used_indoor]
                    activity = available[0] if available else "Tea house culture and shopping streets"
                    used_indoor.add(activity)
                    reason = "given the cold weather, mix warmth and culture"
                elif is_hot:
                    available = [a for a in outdoor_activities if a not in used_outdoor]
                    activity = available[0] if available else "Morning exploration, afternoon rest"
                    used_outdoor.add(activity)
                    reason = "start early to avoid afternoon heat"
                else:
                    available = [a for a in outdoor_activities if a not in used_outdoor]
                    activity = available[0] if available else random.choice(highlights)
                    used_outdoor.add(activity)
                    reason = "perfect weather for outdoor sightseeing"

                itinerary_lines.append(f"{day_label}\n   Visit **{activity}** — {reason}.")

        return "\n\n".join(itinerary_lines)

    def _get_indoor_alternatives(self, city):
        """Generate indoor activity suggestions for rainy days."""
        generic_indoor = [
            f"{city['name']} Provincial Museum",
            f"local tea houses in {city['name']}",
            "covered shopping streets and underground malls",
            f"traditional restaurants serving {city['cuisine'][0] if city['cuisine'] else 'local cuisine'}",
            "art galleries and cultural centers",
            "indoor markets and food halls"
        ]
        return generic_indoor

    def _build_packing_list(self, temp, avg_low, avg_high, rainy_days, weather_code):
        """Build weather-appropriate packing list."""
        items = []

        # Temperature-based clothing
        if avg_low < 0:
            items.append("🧥 Heavy winter coat, thermal underwear, gloves, scarf, warm hat")
            items.append("👢 Waterproof winter boots with good grip (snow possible)")
        elif avg_low < 10:
            items.append("🧥 Warm jacket or layered clothing, light gloves")
            items.append("👟 Closed comfortable walking shoes")
        elif avg_low < 18:
            items.append("👕 Light jacket or sweater for mornings/evenings")
            items.append("👟 Comfortable walking shoes")
        elif avg_high < 28:
            items.append("👕 Light breathable clothing, optional light cardigan")
            items.append("👟 Breathable walking shoes")
        else:
            items.append("👕 Lightweight breathable summer clothes, hat, sunglasses")
            items.append("🩴 Comfortable sandals + walking shoes")
            items.append("☀️ Sunscreen SPF 30+, water bottle")

        # Rain prep
        if rainy_days >= 1:
            items.append("☂️ Umbrella or waterproof rain jacket")
        if rainy_days >= 3:
            items.append("👢 Waterproof shoes — significant rain expected")

        # Universal items
        items.append("🔌 Universal power adapter (China uses Type A/I plugs)")
        items.append("📱 Power bank — Chinese cities involve lots of walking")
        items.append("💳 Mobile payment apps (WeChat Pay / Alipay) — cash is rare")

        return "\n".join(f"- {item}" for item in items)

    def _build_food_section(self, city, weather, preference):
        """Build food recommendations."""
        cuisine = city['cuisine']
        temp = weather['temperature']

        food_lines = []
        is_cold = temp < 10
        is_hot = temp > 28

        for i, dish in enumerate(cuisine[:4]):
            comment = ""
            if is_cold and i == 0:
                comment = " — *perfect for warming up in this cool weather*"
            elif is_hot and i == 0:
                comment = " — *a refreshing local favorite*"
            elif i == 0:
                comment = " — *the most iconic local dish*"

            food_lines.append(f"- **{dish}**{comment}")

        # Add eating tip
        if preference == 'food' or preference == 'cuisine':
            food_lines.append("\n*🍴 Food lover tip: Visit local night markets in the evening "
                              "for authentic street food at half the restaurant price.*")
        elif is_cold:
            food_lines.append("\n*☕ Tip: Many traditional teahouses serve hot tea with "
                              "small snacks — perfect for warming up between sightseeing.*")

        return "\n".join(food_lines)

    def _build_insider_tip(self, city, weather, preference):
        """Generate a unique insider tip."""
        tips_pool = [
            f"Most tourists visit {city['highlights'][0] if city['highlights'] else city['name']} between 10am–3pm. "
            f"Arrive at opening time (usually 8am) to enjoy it nearly empty and get the best photos.",

            f"Download the **DiDi** app (Chinese Uber) before arrival — taxis don't always speak English, "
            f"but DiDi has English mode and handles payment automatically.",

            f"{city['name']}'s subway/metro is incredibly cheap (2–5 RMB) and bypasses traffic. "
            f"Get a transport card on day one.",

            f"The **best season** to visit {city['name']} is {city['best_season']} — "
            f"keep this in mind if you're flexible with future trips.",

            f"Use **Baidu Maps** or **Amap (Gaode)** instead of Google Maps — Google services are blocked in mainland China. "
            f"Download offline maps before traveling.",

            f"Skip official translation apps and use **Pleco** (free Chinese dictionary) or **Google Translate's camera feature** "
            f"with offline Chinese package downloaded beforehand.",
        ]

        return random.choice(tips_pool)

    def _build_budget_note(self, budget, city, duration):
        """Build budget estimate."""
        # Rough daily estimates in RMB
        if budget == 'low' or budget == 'budget':
            daily = "200–400 RMB"
            note = "hostels, street food, public transport, free attractions"
        elif budget == 'high' or budget == 'luxury':
            daily = "1500–3000+ RMB"
            note = "4–5 star hotels, fine dining, private transport, premium experiences"
        else:  # medium
            daily = "500–1000 RMB"
            note = "3–4 star hotels, mix of local & international food, taxis + metro"

        if '1' in duration:
            n = 1
        elif '5' in duration:
            n = 5
        elif '7' in duration:
            n = 7
        else:
            n = 3

        return f"Expect around **{daily} per person/day** for {n} day(s) — covering {note}."

    def _template_chat(self, message, city, weather):
        """Simple keyword-based chatbot fallback."""
        msg = message.lower()

        if any(w in msg for w in ['hi', 'hello', 'hey', 'greet']):
            return ("Hello! 👋 I'm SinoVista AI, your China travel guide. "
                    "Ask me about weather, food, attractions, or travel tips for any Chinese city!")

        if 'weather' in msg and city and weather:
            return (f"Right now in {city['name']}, it's **{weather['condition']}** at "
                    f"**{weather['temperature']}°C** (feels like {weather['feels_like']}°C). "
                    f"Humidity is {weather['humidity']}%. {self._weather_advice(weather)}")

        if any(w in msg for w in ['food', 'eat', 'cuisine', 'restaurant']) and city:
            cuisine_list = ', '.join(city['cuisine'][:4])
            return (f"In {city['name']}, you must try: **{cuisine_list}**. "
                    f"For the most authentic experience, head to local markets in the evening!")

        if any(w in msg for w in ['attraction', 'visit', 'see', 'sight', 'place']) and city:
            highlights = ', '.join(city['highlights'][:4])
            return (f"Top attractions in {city['name']}: **{highlights}**. "
                    f"Start with the first one — it's usually the most iconic!")

        if 'pack' in msg or 'wear' in msg or 'clothes' in msg:
            if weather:
                return self._weather_advice(weather)
            return "Tell me which city you're visiting and I'll give you specific packing advice!"

        if 'best' in msg and ('time' in msg or 'season' in msg) and city:
            return (f"The best time to visit {city['name']} is **{city['best_season']}**. "
                    f"The weather and crowd levels are ideal then.")

        if 'language' in msg or 'speak' in msg:
            return ("Mandarin is the main language. English is limited outside major hotels. "
                    "Download **Pleco** or **Google Translate (offline Chinese pack)** before your trip!")

        if 'pay' in msg or 'money' in msg or 'cash' in msg:
            return ("China is almost cashless! Set up **WeChat Pay** or **Alipay** before arrival. "
                    "Both now accept foreign credit cards. Carry a little cash as backup.")

        if 'vpn' in msg or 'google' in msg or 'internet' in msg:
            return ("Google, Facebook, Instagram, and YouTube are blocked in mainland China. "
                    "Install a reputable VPN before arrival, or use Chinese alternatives "
                    "(WeChat, Baidu, Bilibili).")

        # Default
        if city:
            return (f"I'm happy to help with {city['name']}! Try asking about: "
                    f"weather, food, attractions, packing, or local tips.")
        else:
            return ("I can help with travel info for any Chinese city. "
                    "Try asking: 'What's the weather in Beijing?' or 'What food should I try in Chengdu?'")

    def _weather_advice(self, weather):
        """Generate weather-based advice."""
        temp = weather['temperature']
        cond = weather['condition'].lower()

        if temp < 0:
            return "It's freezing — bundle up with a heavy coat, gloves, and warm boots!"
        elif temp < 10:
            return "Cold weather — wear a warm jacket and layers."
        elif temp < 20:
            return "Cool and pleasant — a light jacket or sweater is enough."
        elif temp < 28:
            return "Comfortable weather — light clothing works perfectly."
        else:
            advice = "Hot weather — wear light breathable clothes, sunscreen, and stay hydrated."
            if 'rain' in cond:
                advice += " And bring an umbrella!"
            return advice
