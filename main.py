import argparse
import sys
from typing import List

from booklib.storage import load_library, save_library
from booklib.commands import (
    add_book, remove_book, edit_book,
    search_books, list_books,
    add_quote, remove_quote
)
from booklib.models import Book

from tabulate import tabulate


def print_books(books: List[Book]) -> None:
    """Красивый вывод списка книг в таблице."""
    if not books:
        print("Список пуст.")
        return

    table = [
        [
            b.id,
            b.title,
            b.author,
            b.year,
            b.genre or "—",
            len(b.quotes)
        ]
        for b in books
    ]
    headers = ["ID", "Название", "Автор", "Год", "Жанр", "Цитат"]
    print(tabulate(table, headers=headers, tablefmt="grid"))


def print_quotes(books: List[Book], book_id: int) -> None:
    """Выводит цитаты конкретной книги."""
    for b in books:
        if b.id == book_id:
            if not b.quotes:
                print("Цитат нет.")
            else:
                print(f"Цитаты из «{b.title}»:")
                for i, q in enumerate(b.quotes):
                    print(f"  [{i}] {q}")
            return
    print(f"Книга с ID={book_id} не найдена.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Домашняя книжная библиотека",
        prog="python main.py"
    )
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    #add
    p_add = subparsers.add_parser("add", help="Добавить книгу")
    p_add.add_argument("--title", required=True, help="Название книги")
    p_add.add_argument("--author", required=True, help="Автор")
    p_add.add_argument("--year", type=int, required=True, help="Год издания")
    p_add.add_argument("--genre", help="Жанр (необязательно)")

    #remove
    p_remove = subparsers.add_parser("remove", help="Удалить книгу")
    p_remove.add_argument("id", type=int, help="ID книги")

    #edit
    p_edit = subparsers.add_parser("edit", help="Изменить книгу")
    p_edit.add_argument("id", type=int, help="ID книги")
    p_edit.add_argument("--title", help="Новое название")
    p_edit.add_argument("--author", help="Новый автор")
    p_edit.add_argument("--year", type=int, help="Новый год")
    p_edit.add_argument("--genre", help="Новый жанр")

    #search
    p_search = subparsers.add_parser("search", help="Поиск книг")
    p_search.add_argument("--title", help="Поиск по названию")
    p_search.add_argument("--author", help="Поиск по автору")
    p_search.add_argument("--year", type=int, help="Точный год")
    p_search.add_argument("--genre", help="Поиск по жанру")
    p_search.add_argument("--quote", help="Поиск по цитате")

    #list
    p_list = subparsers.add_parser("list", help="Показать все книги")
    p_list.add_argument("--sort", choices=["id", "title", "author", "year", "genre"],
                        help="Поле для сортировки")
    p_list.add_argument("--reverse", action="store_true", help="Обратный порядок")

    #quote
    p_quote = subparsers.add_parser("quote", help="Работа с цитатами")
    quote_sub = p_quote.add_subparsers(dest="quote_cmd", help="Действие с цитатой")

    #quote add
    q_add = quote_sub.add_parser("add", help="Добавить цитату")
    q_add.add_argument("book_id", type=int, help="ID книги")
    q_add.add_argument("text", help="Текст цитаты")

    #quote remove
    q_remove = quote_sub.add_parser("remove", help="Удалить цитату")
    q_remove.add_argument("book_id", type=int, help="ID книги")
    q_remove.add_argument("index", type=int, help="Индекс цитаты (0, 1, 2...)")

    #quote list
    q_list = quote_sub.add_parser("list", help="Показать цитаты книги")
    q_list.add_argument("book_id", type=int, help="ID книги")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        books = load_library()
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        sys.exit(1)

    try:
        if args.command == "add":
            books, msg = add_book(
                title=args.title,
                author=args.author,
                year=args.year,
                genre=args.genre,
                books=books
            )
            save = True

        elif args.command == "remove":
            books, msg = remove_book(args.id, books)
            save = True

        elif args.command == "edit":
            books, msg = edit_book(
                book_id=args.id,
                title=args.title,
                author=args.author,
                year=args.year,
                genre=args.genre,
                books=books
            )
            save = True

        elif args.command == "search":
            result, msg = search_books(
                books,
                title=args.title,
                author=args.author,
                year=args.year,
                genre=args.genre,
                quote=args.quote
            )
            print(msg)
            print_books(result)
            save = False

        elif args.command == "list":
            result, msg = list_books(books, sort=args.sort, reverse=args.reverse)
            print(msg)
            print_books(result)
            save = False

        elif args.command == "quote":
            if args.quote_cmd == "add":
                books, msg = add_quote(args.book_id, args.text, books)
                save = True
            elif args.quote_cmd == "remove":
                books, msg = remove_quote(args.book_id, args.index, books)
                save = True
            elif args.quote_cmd == "list":
                print_quotes(books, args.book_id)
                save = False
            else:
                p_quote.print_help()
                sys.exit(1)

        else:
            parser.print_help()
            sys.exit(1)

        if 'msg' in locals():
            print(msg)

        if save:
            try:
                save_library(books)
            except Exception as e:
                print(f"Ошибка сохранения: {e}")
                sys.exit(1)

    except (ValueError, IndexError) as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()