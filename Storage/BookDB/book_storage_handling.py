import json
from Pydantic_Models.pydantic_models import BookData


class BookDB:
    """
    A class that manages book data, providing methods for CRUD operations and verification.
    """
    _data: dict = {}
    _dbpath: str = r"C:\Users\91797\OneDrive\Desktop\Redesigned\Storage\BookDB\BookData.json"

    @classmethod
    def instantiate_data(cls) -> bool:
        """
        Load existing book data from the JSON file into the class-level _data attribute.

        :return: True if data is successfully loaded, False otherwise.
        """
        try:
            with open(cls._dbpath, "r") as fp:
                content = fp.read()
                if content.strip():  # Check if the file content is not empty
                    cls._data = json.loads(content)
                else:
                    cls._data = {}  # Initialize with an empty dictionary if file is empty
            return True
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON data: {e}")
            cls._data = {}  # Initialize data as empty if JSON is invalid
            return False
        except FileNotFoundError:
            print("File not found. Creating new data store.")
            cls._data = {}  # Initialize data if file does not exist
            return False
        except Exception as e:
            print(f"Unable to instantiate data\nError: {e}")
            return False

    @classmethod
    def _search_by_isbn(cls, isbn: str):
        """
        Search for a book by its ISBN.

        :param isbn: The ISBN of the book to search for.
        :return: The book data if found, None otherwise.
        """
        return cls._data.get(isbn)

    @classmethod
    def _search_by_title(cls, title: str) -> dict:
        """
        Search for books by title.

        :param title: The title of the book(s) to search for.
        :return: A dictionary of ISBNs and corresponding book data if found, empty dictionary otherwise.
        """
        return {isbn: book for isbn, book in cls._data.items() if book["title"] == title}

    @classmethod
    def _search_by_author(cls, author: str) -> dict:
        """
        Search for books by author.

        :param author: The author of the book(s) to search for.
        :return: A dictionary of ISBNs and corresponding book data if found, empty dictionary otherwise.
        """
        return {isbn: book for isbn, book in cls._data.items() if book["author"] == author}

    @classmethod
    def verify_book(cls, book_data: BookData) -> bool:
        """
        Verify if the provided book exists in the database.

        :param book_data: The BookData object containing the book information.
        :return: True if the book exists, False otherwise.
        """
        if cls._search_by_isbn(book_data.isbn) is not None:
            return True
        print("Book not found")
        return False

    @classmethod
    def add_book(cls, book_data: BookData) -> bool:
        """
        Add a new book to the database.

        :param book_data: The BookData object containing book information.
        :return: True if the book is added successfully, False if the book already exists.
        """
        if book_data.isbn not in cls._data:
            cls._data[book_data.isbn] = book_data.model_dump()
            return True
        print(f"Book already exists with ISBN: {book_data.isbn}")
        return False

    @classmethod
    def update_book(cls, book_data: BookData) -> bool:
        """
        Update an existing book's data.

        :param book_data: The BookData object containing updated book information.
        :return: True if the book is updated successfully, False if the book does not exist.
        """
        if book_data.isbn not in cls._data:
            print("Book does not exist")
            return False
        cls._data[book_data.isbn] = book_data.model_dump()
        return True

    @classmethod
    def delete_book(cls, book_data: BookData) -> bool:
        """
        Delete a book from the database.

        :param book_data: The BookData object of the book to delete.
        :return: True if the book is deleted successfully, False if the book does not exist.
        """
        if book_data.isbn not in cls._data:
            print("Book does not exist")
            return False
        cls._data.pop(book_data.isbn)
        return True

    @classmethod
    def save_data(cls) -> bool:
        """
        Save the book data to the JSON file.

        :return: True if data is saved successfully, False otherwise.
        """
        try:
            with open(cls._dbpath, "w") as fp:
                json.dump(cls._data, fp, indent=4)  # Pretty printing for better readability
            return True
        except Exception as e:
            print(f"Unable to save data\nError: {e}")
            return False

    @classmethod
    def _get_books(cls) -> None:
        """
        Display all books and their information.
        """
        if not cls._data:
            print("No books found.")
        else:
            for idx, (isbn_num, info) in enumerate(cls._data.items(), start=1):
                print(f"Book {idx}\nISBN: {isbn_num}\nTitle: {info['title']}\nAuthor: {info['author']}")
                print("-" * 40)


# Example interaction
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
