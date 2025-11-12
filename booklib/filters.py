from typing import List, Callable, Any
from .models import Book


def search(books: List[Book], **criteria) -> List[Book]:
    """
    Фильтрует книги по произвольным полям.
    Поддерживаемые ключи: title, author, year, genre, quote (поиск по цитате).

    Пример:
        search(books, author="Оруэлл", year=1949)
    """
    if not criteria:
        return books.copy()

    def match(book: Book) -> bool:
        for key, value in criteria.items():
            if key == "title" and value.lower() not in book.title.lower():
                return False
            elif key == "author" and value.lower() not in book.author.lower():
                return False
            elif key == "year" and book.year != value:
                return False
            elif key == "genre" and book.genre and value.lower() not in book.genre.lower():
                return False
            elif key == "quote" and not any(value.lower() in q.lower() for q in book.quotes):
                return False
        return True

    return [b for b in books if match(b)]


def sort_books(
    books: List[Book],
    key: str = "id",
    reverse: bool = False
) -> List[Book]:
    """
    Сортирует список книг.
    Поддерживаемые ключи: id, title, author, year, genre.
    """
    key_func: Callable[[Book], Any]

    if key == "id":
        key_func = lambda b: b.id
    elif key == "title":
        key_func = lambda b: b.title.lower()
    elif key == "author":
        key_func = lambda b: b.author.lower()
    elif key == "year":
        key_func = lambda b: b.year
    elif key == "genre":
        key_func = lambda b: (b.genre or "").lower()
    else:
        raise ValueError(f"Неизвестный ключ сортировки: {key}")

    return sorted(books, key=key_func, reverse=reverse)