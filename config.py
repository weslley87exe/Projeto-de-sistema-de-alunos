# config.py
from dotenv import load_dotenv
import os

# Carrega as variáveis do .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
