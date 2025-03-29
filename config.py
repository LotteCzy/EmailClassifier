import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_CONFIG = {
    "api_key": os.getenv("DEEPSEEK_API_KEY"),
    "base_url": "https://api.deepseek.com/v1",  # 根据实际API地址调整
    "model": "deepseek-chat",                  # 使用的最新模型
    "timeout": 30
}