"""
SinoVista v3 Configuration
===========================
Made by FAHIM MD FURKAN AHAMED (amfa7im)
Zhengzhou University, China

╔══════════════════════════════════════════════════════════╗
║  HOW TO ACTIVATE REAL AI (DeepSeek):                     ║
║                                                            ║
║  1. Get API key from: https://platform.deepseek.com      ║
║  2. Replace YOUR_API_KEY_HERE below with your real key   ║
║  3. Push to GitHub                                        ║
║  4. Render will auto-redeploy with real AI!              ║
║                                                            ║
║  Without API key, the app uses smart template mode       ║
║  (no errors, fully working).                              ║
╚══════════════════════════════════════════════════════════╝
"""

# =========================================================
# AI / LLM Configuration
# =========================================================
# DeepSeek (recommended for China, no VPN needed)
# Sign up: https://platform.deepseek.com
# Get key: https://platform.deepseek.com/api_keys

AI_API_KEY = "YOUR_API_KEY_HERE"   # ← Replace with your DeepSeek key
AI_PROVIDER = "DeepSeek"
AI_MODEL = "deepseek-chat"
AI_BASE_URL = "https://api.deepseek.com/v1/chat/completions"

# Alternative 1: Tongyi Qianwen (Alibaba - excellent in China)
# AI_API_KEY = "sk-..."
# AI_PROVIDER = "Tongyi"
# AI_MODEL = "qwen-turbo"
# AI_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

# Alternative 2: OpenAI (requires VPN in China)
# AI_API_KEY = "sk-..."
# AI_PROVIDER = "OpenAI"
# AI_MODEL = "gpt-3.5-turbo"
# AI_BASE_URL = "https://api.openai.com/v1/chat/completions"

# Alternative 3: Google Gemini (free, requires VPN to get key)
# AI_API_KEY = "AIza..."
# AI_PROVIDER = "Gemini"
# AI_MODEL = "gemini-pro"
# AI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# =========================================================
# App Settings
# =========================================================
APP_NAME = "SinoVista"
APP_TAGLINE = "A Beautiful View of China"
CREATOR = "amfa7im"
CREATOR_FULL_NAME = "FAHIM MD FURKAN AHAMED"
UNIVERSITY = "Zhengzhou University"
DEBUG = True
