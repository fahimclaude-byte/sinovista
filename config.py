"""
SinoVista v2 Configuration
===========================
Made by amfa7im

To enable real AI (DeepSeek/OpenAI/Tongyi), replace YOUR_API_KEY_HERE below.
Leave as is to use smart template mode (works offline, no cost).
"""

# =========================================================
# AI / LLM Configuration
# =========================================================
# Recommended for China: DeepSeek (works without VPN, cheap)
# Get key from: https://platform.deepseek.com

AI_API_KEY = "YOUR_API_KEY_HERE"
AI_PROVIDER = "DeepSeek"
AI_MODEL = "deepseek-chat"
AI_BASE_URL = "https://api.deepseek.com/v1/chat/completions"

# Alternative: Tongyi Qianwen (Alibaba - works perfectly in China)
# AI_API_KEY = "sk-..."
# AI_PROVIDER = "Tongyi"
# AI_MODEL = "qwen-turbo"
# AI_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

# Alternative: OpenAI (requires VPN in China)
# AI_API_KEY = "sk-..."
# AI_PROVIDER = "OpenAI"
# AI_MODEL = "gpt-3.5-turbo"
# AI_BASE_URL = "https://api.openai.com/v1/chat/completions"

# =========================================================
# App Settings
# =========================================================
APP_NAME = "SinoVista"
APP_TAGLINE = "A Beautiful View of China"
CREATOR = "amfa7im"
DEBUG = True
