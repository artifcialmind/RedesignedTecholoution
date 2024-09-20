from Storage.storage import ContextManager


class Menu:
    def __init__(self):
        self.context_manager = ContextManager()
        self.allowed_inputs = {
            "1": "add_book",
            "2": "update_book",
            "3": "delete_book",
            "4": "list_books",
            "5": "search_books",
            "6": "add_user",
            "7": "update_user",
            "8": "delete_user",
            "9": "list_users",
            "10": "search_users",
            "11": "check_out_book",
            "12": "check_in_book",
            "13": "track_availability",
            "14": "exit"
        }

    def display_menu(self):
        print("\n--- Library Management System ---")
        print("Please choose an option:")
        for key, action in self.allowed_inputs.items():
            print(f"{key}. {action.replace('_', ' ').capitalize()}")
        print()

    def verify_input(self, input_by_user: str) -> bool:
        if input_by_user not in self.allowed_inputs:
            print(f"Invalid input '{input_by_user}'. Please choose a valid option.")
            return False
        return True

    def execute_action(self, input_by_user: str, manager):
        action = self.allowed_inputs[input_by_user]
        if action == "add_book":
           manager.add_book_data()
        elif action == "update_book":
            manager.update_book_data()
        elif action == "delete_book":
            manager.delete_book_data()
        elif action == "list_books":
            manager.get_books_data()
        elif action == "search_books":
            print(manager.search_book())
        elif action == "add_user":
            manager.add_user_data()
        elif action == "update_user":
            manager.update_user_data()
        elif action == "delete_user":
            manager.delete_user_data()
        elif action == "list_users":
            manager.get_all_users()
        elif action == "search_users":
            print(manager.search_user())
        elif action == "check_out_book":
            manager.checkout_book()
        elif action == "check_in_book":
            manager.checkin_book()
        elif action == "track_availability":
            if manager.track_availability():
                print("Available!")
            else:
                print("Not available")
        elif action == "exit":
            print("Exiting the system. Goodbye!")
            exit(0)

    def run(self):
        with self.context_manager as manager:
            while True:
                self.display_menu()
                user_input = input("Enter your choice: ").strip()
                if self.verify_input(user_input):
                    if user_input == "14":
                        print("Exiting the system. Goodbye!")
                        break
                    self.execute_action(user_input, manager)


