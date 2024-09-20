import json
import os
from Storage.UserDB.user_storage_handling import UserDB
from Storage.BookDB.book_storage_handling import BookDB
from Pydantic_Models.pydantic_models import Assignment, BookData, UserLoggingData


class ContextManager(UserDB, BookDB):
    """
    ContextManager handles book and user management for the library system,
    along with tracking book assignments for check-out and check-in operations.
    Inherits from UserDB and BookDB to provide methods for managing users and books.
    """

    _previous_context: dict  # Stores the previous book assignments (ISBN -> User ID mapping)
    _assignment_path: str = os.path.join(os.path.dirname(__file__), 'AssignmentManager.json')

    def __init__(self):
        """
        Initialize the ContextManager by loading user and book data from storage,
        and then load previous book assignments.
        """
        UserDB.instantiate_data()  # Load users data from the storage
        BookDB.instantiate_data()  # Load books data from the storage
        self._load_previous_context()  # Load any previous book assignment context

    def _load_previous_context(self):
        """
        Load previous assignments from the JSON file. If the file doesn't exist or is
        improperly formatted, an empty dictionary is initialized.
        """
        try:
            with open(self._assignment_path, "r") as fp:
                self._previous_context = json.load(fp)
        except FileNotFoundError:
            print("Assignment file not found, starting with an empty context.")
            self._previous_context = {}
        except json.JSONDecodeError:
            print("Error decoding JSON file. Starting with an empty context.")
            self._previous_context = {}

    def is_book_available(self, isbn: str) -> bool:
        """
        Check if a book is available for checkout based on its ISBN.

        :param isbn: The ISBN of the book to check.
        :return: True if the book is available, False otherwise.
        """
        if isbn in self._previous_context.keys() or isbn not in BookDB._data.keys():
            return False
        return True

    def checkout(self, assignment_info: Assignment) -> bool:
        """
        Assign a book to a user for checkout if the book is available and both
        book and user IDs are valid.

        :param assignment_info: Assignment data containing ISBN and User ID.
        :return: True if the checkout is successful, False otherwise.
        """
        isbn, user_id = assignment_info.isbn, assignment_info.user_id
        if isbn in BookDB._data.keys() and user_id in UserDB._data.keys() and self.is_book_available(isbn):
            self._previous_context[isbn] = user_id
            print(f"Book with ISBN {isbn} assigned to user with ID {user_id}.")
            return True
        else:
            print("Invalid ISBN or login ID, or the book is unavailable.")
            return False

    def checkin(self, assignment_info: Assignment) -> bool:
        """
        Check-in a book and remove the assignment based on the ISBN and User ID.

        :param assignment_info: Assignment data containing ISBN and User ID.
        :return: True if the check-in is successful, False otherwise.
        """
        isbn, user_id = assignment_info.isbn, assignment_info.user_id
        if isbn in self._previous_context.keys() and self._previous_context[isbn] == user_id:
            del self._previous_context[isbn]
            print(f"Assignment of book with ISBN {isbn} removed.")
            return True
        else:
            print(f"No assignment found for ISBN: {isbn} and User ID: {user_id}.")
            return False

    def save_data(self) -> bool:
        """
        Save the current assignment data to the JSON file, along with user and book data.

        :return: True if the data is saved successfully, False otherwise.
        """
        super().save_data()  # Save user data
        BookDB.save_data()  # Save book data
        try:
            with open(self._assignment_path, "w") as fp:
                json.dump(self._previous_context, fp)
            print("Assignments saved successfully!")
            return True
        except Exception as e:
            print(f"Unable to save assignments. Error: {e}")
            return False

    @staticmethod
    def take_assignment_data() -> Assignment:
        """
        Take input from the user for assignment (book check-out/check-in).

        :return: An Assignment object containing user-inputted ISBN and User ID.
        """
        input_assignment_data = Assignment()
        input_assignment_data.isbn = input("Please enter the ISBN of the book: ")
        input_assignment_data.user_id = input("Please enter your user ID: ")
        return input_assignment_data

    @staticmethod
    def take_book_data() -> BookData:
        """
        Take input from the user for book data (add, update, delete).

        :return: A BookData object containing user-inputted book details.
        """
        input_book_data = BookData()
        input_book_data.title = input("Please enter the book title: ")
        input_book_data.author = input("Please enter the book author: ")
        input_book_data.isbn = input("Please enter the book ISBN: ")
        return input_book_data

    @staticmethod
    def take_user_data() -> UserLoggingData:
        """
        Take input from the user for user data (add, update, delete).

        :return: A UserLoggingData object containing user-inputted user details.
        """
        input_user_data = UserLoggingData()
        input_user_data.user_id = input("Please enter the user ID: ")
        input_user_data.password = input("Please enter the user password: ")
        input_user_data.name = input("Please enter your name: ")
        return input_user_data

    def add_book_data(self) -> None:
        """
        Add a new book to the database using user input.
        """
        data = self.take_book_data()
        resp = BookDB.add_book(data)
        if resp:
            print("Added book successfully!")

    def delete_book_data(self) -> None:
        """
        Delete a book from the database using user input.
        """
        data = self.take_book_data()
        resp = BookDB.delete_book(data)
        if resp:
            print("Deleted book successfully!")

    def update_book_data(self) -> None:
        """
        Update book information in the database using user input.
        """
        data = self.take_book_data()
        resp = BookDB.update_book(data)
        if resp:
            print("Updated book successfully!")

    @staticmethod
    def search_book():
        """
        Search for a book in the database by title, author, or ISBN based on user input.

        :return: The search results or an empty dictionary if no results are found.
        """
        input_by_user = input("Enter 1 to search by title\nEnter 2 to search by author\nEnter 3 to search by ISBN: ")
        if input_by_user == "1":
            return BookDB._search_by_title(input("Enter the title of the book: "))
        elif input_by_user == "2":
            return BookDB._search_by_author(input("Enter the author of the book: "))
        elif input_by_user == "3":
            return BookDB._search_by_isbn(input("Enter the ISBN of the book: "))
        else:
            print("Invalid input")
            return {}

    @staticmethod
    def get_books_data() -> None:
        """
        Retrieve all book data from the database.
        """
        return BookDB._get_books()

    @staticmethod
    def search_user():
        """
        Search for a user in the database by user ID or name based on user input.

        :return: The search results or an empty dictionary if no results are found.
        """
        input_by_user = input("Enter 1 to search by ID\nEnter 2 to search by name: ")
        if input_by_user == "1":
            user_id = input("Enter the user ID: ")
            return UserDB._search_by_id(user_id)
        elif input_by_user == "2":
            username = input("Enter the username: ")
            return UserDB._search_by_name(username)
        else:
            print("Invalid input")
            return {}

    @staticmethod
    def get_all_users() -> None:
        """
        Retrieve all user data from the database.
        """
        return UserDB._get_users()

    def add_user_data(self) -> None:
        """
        Add a new user to the database using user input.
        """
        data = self.take_user_data()
        resp = UserDB.add_user(data)
        if resp:
            print("Added user successfully!")

    def delete_user_data(self) -> None:
        """
        Delete a user from the database using user input.
        """
        data = self.take_user_data()
        resp = UserDB.delete_user(data)
        if resp:
            print("Deleted user successfully!")

    def update_user_data(self) -> None:
        """
        Update user password in the database using user input.
        """
        data = self.take_user_data()
        resp = UserDB.update_password(data)
        if resp:
            print("Updated user successfully!")

    def track_availability(self) -> bool:
        """
        Check if a book is available for checkout by its ISBN.

        :return: True if the book is available, False otherwise.
        """
        isbn = input("Enter the ISBN to check availability: ")
        return self.is_book_available(isbn)

    def checkin_book(self) -> bool:
        """
        Perform a book check-in operation by taking user input for the book and user.

        :return: True if the check-in is successful, False otherwise.
        """
        assignment_data = self.take_assignment_data()
        return self.checkin(assignment_data)

    def checkout_book(self) -> bool:
        """
        Perform a book checkout operation by taking user input for the book and user.

        :return: True if the checkout is successful, False otherwise.
        """
        assignment_data = self.take_assignment_data()
        return self.checkout(assignment_data)

    def __enter__(self):
        """
        Enter the runtime context related to this object.
        """
        print("Entering context manager...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context related to this object, ensuring data is saved.
        """
        print("Exiting context manager...")
        self.save_data()
