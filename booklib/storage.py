import json
import os
from typing import List
from .models import Book


DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "library.json")


def ensure_data_file() -> None:
    """Создаёт папку data/ и пустой library.json, если их нет."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def load_library() -> List[Book]:
    """
    Загружает библиотеку из JSON.
    Возвращает список объектов Book.
    """
    ensure_data_file()
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка в формате JSON: {e}. Удалите или исправьте файл {DATA_FILE}.")
    except Exception as e:
        raise RuntimeError(f"Не удалось прочитать файл: {e}")

    if not isinstance(raw_data, list):
        raise ValueError("JSON должен содержать список книг.")

    books = []
    for item in raw_data:
        try:
            book = Book.from_dict(item)
            books.append(book)
        except (KeyError, ValueError) as e:
            print(f"Предупреждение: пропущена некорректная книга: {e}")
    
    return books


def save_library(books: List[Book]) -> None:
    """
    Сохраняет список книг в JSON.
    """
    ensure_data_file()
    
    try:
        data_to_save = [book.to_dict() for book in books]
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2, sort_keys=True)
    except PermissionError:
        raise RuntimeError(f"Нет прав на запись в файл: {DATA_FILE}")
    except OSError as e:
        raise RuntimeError(f"Ошибка записи файла: {e}")