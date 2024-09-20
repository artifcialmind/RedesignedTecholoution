import json
from Pydantic_Models.pydantic_models import UserLoggingData


class UserDB:
    _data: dict = {}
    _dbpath: str = r"C:\Users\91797\OneDrive\Desktop\Redesigned\Storage\UserDB\UserData.json"

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
    def _search_by_id(self, user_id: str):
        if user_id in self._data.keys() and self._data[user_id]:
            return self._data[user_id]
        else:
            return None

    @classmethod
    def _search_by_name(self, name: str) -> dict:
        found_matches = {}
        for collection in self._data.keys():
            if self._data[collection] == name:
                found_matches[collection] = name
        return found_matches

    def verify_user(self, user_data: UserLoggingData) -> bool:
        if (self._search_by_id(user_data.user_id) is not None and
                self._data[user_data.user_id] == user_data.password):
            return True
        else:
            print("Either password or login id is incorrect")
            return False

    @classmethod
    def add_user(cls, user_data: UserLoggingData) -> bool:
        if user_data.user_id not in cls._data.keys():
            cls._data[user_data.user_id] = user_data.model_dump()
            return True
        else:
            print(f"User already exists with login id: {user_data.user_id}")
            return False

    @classmethod
    def update_password(cls, user_data: UserLoggingData):
        if user_data.user_id not in cls._data.keys():
            print("User does not exist")
            return False
        elif user_data.password == cls._data[user_data.user_id]:
            print("Previous and new password cannot be the same")
            return False
        else:
            cls._data[user_data.user_id]["password"] = user_data.password
            return True

    @classmethod
    def delete_user(cls, user_data: UserLoggingData):
        if user_data.user_id not in cls._data.keys():
            print("User does not exist")
            return False
        else:
            cls._data.pop(user_data.user_id)
            return True

    @classmethod
    def _get_users(cls) -> None:
        for idx, (user_id, info) in enumerate(cls._data.items()):
            print(f"User ID: {user_id}\nName: {info["name"]}")
            print("-" * 40)

    @classmethod
    def save_data(cls) -> bool:
        try:
            with open(cls._dbpath, "w") as fp:
                json.dump(cls._data, fp)
                fp.close()
            return True
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON data: {e}")
            return False
        except FileNotFoundError:
            print(f"File not found. Creating new data store.")
            return False
        except Exception as e:
            print(f"Unable to save data\nError: {e}")
            return False


# Instantiate data on program start
# db = UserDB()  # Create an instance of UserDB
#
# # Add and verify users interactively
# while True:
#     print("\n1. Add User\n2. Verify User\n3. Exit")
#     i = int(input("Choose an option: "))
#
#     if i == 1:
#         user_id = input("Enter login ID: ")
#         password = input("Enter password: ")
#         user = UserLoggingData(user_id=user_id, password=password)
#         db.add_user(user)
#     elif i == 2:
#         user_id = input("Enter login ID: ")
#         password = input("Enter password: ")
#         user = UserLoggingData(user_id=user_id, password=password)
#         if db.verify_user(user):
#             print("User verified successfully")
#         else:
#             print("Failed to verify user")
#     elif i == 3:
#         print("Exiting...")
#         break
#     else:
#         print("Invalid option, please try again")
