import json
from Pydantic_Models.pydantic_models import BookData


class BookDB:
    _data: dict = {}
    _dbpath: str = r"C:\Users\91797\OneDrive\Desktop\Redesigned\Storage\BookDB\BookData.json"

    @classmethod
    def instantiate_data(cls) -> bool:
        try:
            with open(cls._dbpath, "r") as fp:
                content = fp.read()
                if content.strip():  # Check if file content is not empty
                    cls._data = json.loads(content)
                else:
                    cls._data = {}  # Initialize with an empty dictionary if file is empty
            return True
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON data: {e}")
            cls._data = {}  # Initialize data as empty if JSON is invalid
            return False
        except FileNotFoundError:
            print(f"File not found. Creating new data store.")
            cls._data = {}  # Initialize data if file does not exist
            return False
        except Exception as e:
            print(f"Unable to instantiate data\nError: {e}")
            return False

    @classmethod
    def _search_by_isbn(cls, isbn: str):
        return cls._data.get(isbn, None)

    @classmethod
    def _search_by_title(cls, title: str) -> dict:
        return {isbn: book for isbn, book in cls._data.items() if book["title"] == title}

    @classmethod
    def _search_by_author(cls, author: str) -> dict:
        return {isbn: book for isbn, book in cls._data.items() if book["author"] == author}

    @classmethod
    def verify_book(cls, book_data: BookData) -> bool:
        if cls._search_by_isbn(book_data.isbn) is not None:
            return True
        else:
            print("Book not found")
            return False

    @classmethod
    def add_book(cls, book_data: BookData) -> bool:
        if book_data.isbn not in cls._data.keys():
            cls._data[book_data.isbn] = book_data.model_dump()
            return True
        else:
            print(f"Book already exists with ISBN: {book_data.isbn}")
            return False

    @classmethod
    def update_book(cls, book_data: BookData) -> bool:
        if book_data.isbn not in cls._data.keys():
            print("Book does not exist")
            return False
        else:
            cls._data[book_data.isbn] = book_data.model_dump()
            return True

    @classmethod
    def delete_book(cls, book_data: BookData) -> bool:
        if book_data.isbn not in cls._data.keys():
            print("Book does not exist")
            return False
        else:
            cls._data.pop(book_data.isbn)
            return True

    @classmethod
    def save_data(cls) -> bool:
        try:
            with open(cls._dbpath, "w") as fp:
                json.dump(cls._data, fp)
            return True
        except Exception as e:
            print(f"Unable to save data\nError: {e}")
            return False

    @classmethod
    def _get_books(cls) -> None:
        for idx, (isbn_num, info) in enumerate(cls._data.items()):
            print(f"Book {idx + 1}\nISBN: {isbn_num}\nTitle: {info['title']}\nAuthor: {info['author']}")
            print("-"*40)


#
# # Example interaction
# db = BookDB()  # Create an instance of BookDB
# db.instantiate_data()
#
# # Add and verify books interactively
# while True:
#     print("\n1. Add Book\n2. Verify Book\n3. Exit")
#     i = int(input("Choose an option: "))
#
#     if i == 1:
#         title = input("Enter book title: ")
#         author = input("Enter book author: ")
#         isbn = input("Enter book ISBN: ")
#         book = BookData(title=title, author=author, isbn=isbn)
#         db.add_book(book)
#     elif i == 2:
#         isbn = input("Enter book ISBN to verify: ")
#         book = BookData(title="", author="", isbn=isbn)  # Title/author not needed for verification
#         if db.verify_book(book):
#             print("Book verified successfully")
#     elif i == 3:
#         print("Exiting...")
#         break
#     else:
#         print("Invalid option, please try again")
