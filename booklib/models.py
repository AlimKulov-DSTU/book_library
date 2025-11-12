from typing import List, Optional


class Book:
    """Класс, представляющий книгу в библиотеке."""
    
    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        year: int,
        genre: Optional[str] = None,
        quotes: Optional[List[str]] = None
    ):
        self.id = book_id
        self.title = title.strip()
        self.author = author.strip()
        self.year = year
        self.genre = genre.strip() if genre else None
        self.quotes = quotes[:] if quotes else []

        self._validate()

    def _validate(self):
        """Валидация полей."""
        if not self.title:
            raise ValueError("Название книги не может быть пустым.")
        if not self.author:
            raise ValueError("Автор не может быть пустым.")
        if not isinstance(self.year, int) or self.year < 0:
            raise ValueError("Год должен быть положительным целым числом.")

    def to_dict(self) -> dict:
        """Преобразование в словарь для JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre,
            "quotes": self.quotes.copy()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """Создание объекта из словаря."""
        return cls(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            genre=data.get("genre"),
            quotes=data.get("quotes", [])
        )

    def __str__(self) -> str:
        genre_str = f", {self.genre}" if self.genre else ""
        quotes_count = len(self.quotes)
        return f"[{self.id}] {self.title} — {self.author} ({self.year}){genre_str} | Цитат: {quotes_count}"