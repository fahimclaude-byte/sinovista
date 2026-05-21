"""
Configuration File for SinoVista
=================================
Edit this file to enable real LLM AI features.
If you don't have an API key, the app will use smart template mode (still works great).
"""

# =========================================================
# AI / LLM Configuration
# =========================================================
# To enable real AI (DeepSeek, OpenAI, etc.), replace "YOUR_API_KEY_HERE"
# with your actual API key. Leave it as is to use the offline template mode.

# DeepSeek (cheapest, China-friendly, recommended for students):
AI_API_KEY = "YOUR_API_KEY_HERE"      # Get from https://platform.deepseek.com
AI_PROVIDER = "DeepSeek"
AI_MODEL = "deepseek-chat"
AI_BASE_URL = "https://api.deepseek.com/v1/chat/completions"

# To use OpenAI instead, uncomment these and comment out the DeepSeek block above:
# AI_API_KEY = "sk-..."                # Get from https://platform.openai.com
# AI_PROVIDER = "OpenAI"
# AI_MODEL = "gpt-3.5-turbo"
# AI_BASE_URL = "https://api.openai.com/v1/chat/completions"

# To use Tongyi Qianwen (Alibaba):
# AI_API_KEY = "sk-..."                # Get from https://dashscope.console.aliyun.com
# AI_PROVIDER = "Tongyi"
# AI_MODEL = "qwen-turbo"
# AI_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

# =========================================================
# App Settings
# =========================================================
APP_NAME = "SinoVista"
APP_TAGLINE = "A Beautiful View of China"
DEBUG = True
