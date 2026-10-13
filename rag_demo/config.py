import os

# 大模型 DeepSeek 配置
API_KEY = ("")
BASE_URL = ("https://api.deepseek.com")
CHAT_MODEL = ("deepseek-flash")

# 向量模型硅基流动配置
API_KEY_SILICON = ("")
BASE_KEY_SILICON = ("https://api.siliconflow.cn/v1")
EMBED_MODEL = ("BAAI/bge-m3")

# 向量数据库配置
DB_PATH = ( "./chroma_db")
CHUNK_SIZE = 500
CHUNK_OVERRLAP = 50