import json
import os
from Pydantic_Models.pydantic_models import UserLoggingData


class UserDB:
    """
    A class that manages user data, providing methods for CRUD operations and verification.
    """
    _data: dict = {}
    _dbpath: str = os.path.join(os.path.dirname(__file__), 'UserData.json')
    print(_dbpath)

    @classmethod
    def instantiate_data(cls) -> bool:
        """
        Load existing user data from the JSON file into the class-level _data attribute.

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
    def _search_by_id(cls, user_id: str):
        """
        Search for a user by their user ID.

        :param user_id: The ID of the user to search for.
        :return: The user data if found, None otherwise.
        """
        return cls._data.get(user_id)

    @classmethod
    def _search_by_name(cls, name: str) -> dict:
        """
        Search for users by name.

        :param name: The name of the user(s) to search for.
        :return: A dictionary of user IDs and corresponding names if found, empty dictionary otherwise.
        """
        found_matches = {user_id: user_info["name"] for user_id, user_info in cls._data.items() if user_info["name"] == name}
        return found_matches

    def verify_user(self, user_data: UserLoggingData) -> bool:
        """
        Verify if the provided user credentials are correct.

        :param user_data: The UserLoggingData object containing user credentials.
        :return: True if the credentials match, False otherwise.
        """
        stored_user = self._search_by_id(user_data.user_id)
        if stored_user and stored_user["password"] == user_data.password:
            return True
        print("Either password or login ID is incorrect")
        return False

    @classmethod
    def add_user(cls, user_data: UserLoggingData) -> bool:
        """
        Add a new user to the database.

        :param user_data: The UserLoggingData object containing user information.
        :return: True if the user is added successfully, False if the user already exists.
        """
        if user_data.user_id not in cls._data:
            cls._data[user_data.user_id] = user_data.model_dump()
            return True
        print(f"User already exists with login ID: {user_data.user_id}")
        return False

    @classmethod
    def update_password(cls, user_data: UserLoggingData) -> bool:
        """
        Update the password for an existing user.

        :param user_data: The UserLoggingData object containing the updated password.
        :return: True if the password is updated successfully, False otherwise.
        """
        stored_user = cls._search_by_id(user_data.user_id)
        if not stored_user:
            print("User does not exist")
            return False
        if stored_user["password"] == user_data.password:
            print("Previous and new password cannot be the same")
            return False
        cls._data[user_data.user_id]["password"] = user_data.password
        return True

    @classmethod
    def delete_user(cls, user_data: UserLoggingData) -> bool:
        """
        Delete a user from the database.

        :param user_data: The UserLoggingData object of the user to delete.
        :return: True if the user is deleted successfully, False if the user does not exist.
        """
        if user_data.user_id not in cls._data:
            print("User does not exist")
            return False
        cls._data.pop(user_data.user_id)
        return True

    @classmethod
    def _get_users(cls) -> None:
        """
        Display all users and their information.
        """
        if not cls._data:
            print("No users found.")
        else:
            for idx, (user_id, info) in enumerate(cls._data.items(), start=1):
                print(f"User {idx}:\nUser ID: {user_id}\nName: {info['name']}")
                print("-" * 40)

    @classmethod
    def save_data(cls) -> bool:
        """
        Save the user data to the JSON file.

        :return: True if data is saved successfully, False otherwise.
        """
        try:
            with open(cls._dbpath, "w") as fp:
                json.dump(cls._data, fp, indent=4)  # Pretty printing for better readability
            return True
        except Exception as e:
            print(f"Unable to save data\nError: {e}")
            return False
