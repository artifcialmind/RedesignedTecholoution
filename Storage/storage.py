import json
from Storage.UserDB.user_storage_handling import UserDB
from Storage.BookDB.book_storage_handling import BookDB
from Pydantic_Models.pydantic_models import Assignment, BookData, UserLoggingData


class ContextManager(UserDB, BookDB):
    _previous_context: dict
    _assignment_path: str = r"C:\Users\91797\OneDrive\Desktop\Redesigned\Storage\AssignmentManager.json"

    def __init__(self):
        UserDB.instantiate_data()
        BookDB.instantiate_data()
        self._load_previous_context()

    def _load_previous_context(self):
        """ Load previous assignments from the JSON file, or initialize an empty dictionary. """
        try:
            with open(self._assignment_path, "r") as fp:
                self._previous_context = json.load(fp)
        except FileNotFoundError:
            self._previous_context = {}
        except json.JSONDecodeError:
            print("Error decoding JSON file. Starting with an empty context.")
            self._previous_context = {}

    def is_book_available(self, isbn: str) -> bool:
        if isbn in self._previous_context.keys() or isbn not in BookDB._data.keys():
            return False
        return True

    def checkout(self, assignment_info: Assignment) -> bool:
        isbn, user_id = assignment_info.isbn, assignment_info.user_id
        if isbn in BookDB._data.keys() and user_id in UserDB._data.keys() and self.is_book_available(isbn):
            self._previous_context[isbn] = user_id
            print(f"Book with ISBN {isbn} assigned to user with ID {user_id}.")
            return True
        else:
            print("Invalid ISBN or login ID.")
            return False

    def checkin(self, assignment_info: Assignment) -> bool:
        isbn, user_id = assignment_info.isbn, assignment_info.user_id
        if isbn in self._previous_context.keys() and self._previous_context[isbn] == user_id:
            del self._previous_context[isbn]
            print(f"Assignment of book with ISBN {isbn} removed.")
            return True
        else:
            print(f"No assignment found for isbn: {isbn} and user id: {user_id}.")
            return False

    def save_data(self) -> bool:
        super().save_data()  # Save user data
        BookDB.save_data()  # Save book data
        try:
            with open(self._assignment_path, "w") as fp:
                json.dump(self._previous_context, fp)
            print("Assignments saved successfully!")
            return True
        except Exception as e:
            print(f"Unable to save assignments\nError: {e}")
            return False

    @staticmethod
    def take_assignment_data() -> Assignment:
        input_assignment_data = Assignment()
        input_assignment_data.isbn = input("Please enter isbn of book: ")
        input_assignment_data.user_id = input("Please enter your user id: ")
        return input_assignment_data

    @staticmethod
    def take_book_data() -> BookData:
        input_book_data = BookData()
        input_book_data.title = input("Please enter book title: ")
        input_book_data.author = input("Please enter book author: ")
        input_book_data.isbn = input("Please enter book isbn: ")
        return input_book_data

    @staticmethod
    def take_user_data() -> UserLoggingData:
        input_user_data = UserLoggingData()
        input_user_data.user_id = input("Please enter user id: ")
        input_user_data.password = input("Please enter user password: ")
        input_user_data.name = input("Please enter your name: ")
        return input_user_data

    def add_book_data(self) -> None:
        data = self.take_book_data()
        BookDB.add_book(data)

    def delete_book_data(self) -> None:
        data = self.take_book_data()
        BookDB.delete_book(data)

    def update_book_data(self) -> None:
        data = self.take_book_data()
        BookDB.update_book(data)

    @staticmethod
    def search_book():
        input_by_user = input("Enter 1 for search by title\nEnter 2 for search by author\nEnter 3 for search by isbn: " )
        if input_by_user == "1":
            return BookDB._search_by_title(input("Enter title of book: "))
        elif input_by_user == "2":
            return BookDB._search_by_author(input("Enter author of book: "))
        elif input_by_user == "3":
            return BookDB._search_by_isbn(input("Enter isbn of book: "))
        else:
            print("Invalid input")
            return {}

    @staticmethod
    def get_books_data() -> None:
        return BookDB._get_books()

    @staticmethod
    def search_user():
        input_by_user = input("Enter 1 for searching by id\nEnter 2 for searching by name:")
        if input_by_user == "1":
            user_id = input("Enter user id: ")
            return UserDB._search_by_id(user_id)
        elif input_by_user == "2":
            username = input("Enter username: ")
            return UserDB._search_by_name(username)
        else:
            print("Invalid input")
            return {}

    @staticmethod
    def get_all_users() -> None:
        return UserDB._get_users()

    def add_user_data(self) -> None:
        data = self.take_user_data()
        UserDB.add_user(data)

    def delete_user_data(self) -> None:
        data = self.take_user_data()
        UserDB.delete_user(data)

    def update_user_data(self) -> None:
        data = self.take_user_data()
        UserDB.update_password(data)

    def track_availability(self) -> bool:
        isbn = input("Enter isbn to check availability: ")
        return self.is_book_available(isbn)

    def checkin_book(self) -> bool:
        assignment_data = self.take_assignment_data()
        return self.checkin(assignment_data)

    def checkout_book(self) -> bool:
        assignment_data = self.take_assignment_data()
        return self.checkout(assignment_data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type:
            print(f"Exception occurred: {exc_val}")
        self.save_data()
        UserDB.save_data()
        BookDB.save_data()
        return True
