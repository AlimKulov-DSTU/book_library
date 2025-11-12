import os
from typing import List, Optional, Tuple
from .models import Book
from .filters import search, sort_books


def _next_id(books: List[Book]) -> int:
    """Возвращает следующий свободный id."""
    return max((b.id for b in books), default=0) + 1


def add_book(
    title: str,
    author: str,
    year: int,
    genre: Optional[str] = None,
    books: List[Book] = None
) -> Tuple[List[Book], str]:
    """
    Добавляет новую книгу.
    """
    if books is None:
        books = []

    book_id = _next_id(books)
    new_book = Book(
        book_id=book_id,
        title=title,
        author=author,
        year=year,
        genre=genre
    )
    books.append(new_book)
    return books, f"Книга добавлена [ID={book_id}]: {new_book.title}"


def remove_book(book_id: int, books: List[Book]) -> Tuple[List[Book], str]:
    """
    Удаляет книгу по id.
    """
    for i, b in enumerate(books):
        if b.id == book_id:
            removed = books.pop(i)
            return books, f"Книга удалена [ID={book_id}]: {removed.title}"
    return books, f"Книга с ID={book_id} не найдена."


def edit_book(
    book_id: int,
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None,
    genre: Optional[str] = None,
    books: List[Book] = None
) -> Tuple[List[Book], str]:
    """
    Изменяет поля книги. Поля, переданные как None, не меняются.
    """
    if books is None:
        books = []

    for b in books:
        if b.id == book_id:
            if title is not None:
                b.title = title.strip()
            if author is not None:
                b.author = author.strip()
            if year is not None:
                b.year = year
            if genre is not None:
                b.genre = genre.strip() if genre else None

            # валидация после изменения
            b._validate()
            return books, f"Книга обновлена [ID={book_id}]: {b.title}"
    return books, f"Книга с ID={book_id} не найдена."


def search_books(
    books: List[Book],
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None,
    genre: Optional[str] = None,
    quote: Optional[str] = None
) -> Tuple[List[Book], str]:
    """
    Поиск по произвольным полям.
    """
    criteria = {}
    if title:
        criteria["title"] = title
    if author:
        criteria["author"] = author
    if year is not None:
        criteria["year"] = year
    if genre:
        criteria["genre"] = genre
    if quote:
        criteria["quote"] = quote

    result = search(books, **criteria)
    if result:
        return result, f"Найдено книг: {len(result)}"
    return result, "Ничего не найдено."


def list_books(
    books: List[Book],
    sort: Optional[str] = None,
    reverse: bool = False
) -> Tuple[List[Book], str]:
    """
    Выводит весь список (с опциональной сортировкой).
    """
    if sort:
        try:
            books = sort_books(books, key=sort, reverse=reverse)
        except ValueError as e:
            return books, str(e)

    count = len(books)
    return books, f"Всего книг в библиотеке: {count}"


def add_quote(
    book_id: int,
    text: str,
    books: List[Book]
) -> Tuple[List[Book], str]:
    """
    Добавляет цитату к книге.
    """
    for b in books:
        if b.id == book_id:
            b.quotes.append(text.strip())
            return books, f"Цитата добавлена к книге [ID={book_id}]."
    return books, f"Книга с ID={book_id} не найдена."


def remove_quote(
    book_id: int,
    quote_idx: int,
    books: List[Book]
) -> Tuple[List[Book], str]:
    """
    Удаляет цитату по её индексу внутри книги.
    """
    for b in books:
        if b.id == book_id:
            if 0 <= quote_idx < len(b.quotes):
                removed = b.quotes.pop(quote_idx)
                return books, f"Цитата удалена: \"{removed}\""
            return books, f"Цитата с индексом {quote_idx} не найдена."
    return books, f"Книга с ID={book_id} не найдена."