# tools/fakers.py
import time

def get_random_email() -> str:
    """Генерирует уникальный email с использованием timestamp"""
    return f"test.{time.time()}@example.com"
