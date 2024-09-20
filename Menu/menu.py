from Storage.storage import ContextManager


class Menu:
    """
    The Menu class provides the interface for the Library Management System, allowing the user to
    interact with the system by selecting actions such as adding, updating, or deleting books and users.
    It also handles book check-in/check-out operations and tracks availability.
    """

    def __init__(self):
        """
        Initializes the Menu object and sets up a context manager for managing
        the system's data, as well as a dictionary of allowed user inputs and corresponding actions.
        """
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
        """
        Displays the menu options for the Library Management System.
        The menu lists the available actions users can perform, such as managing books and users.
        """
        print("\n--- Library Management System ---")
        print("Please choose an option:")
        for key, action in self.allowed_inputs.items():
            # Display the action in a user-friendly format
            print(f"{key}. {action.replace('_', ' ').capitalize()}")
        print()

    def verify_input(self, input_by_user: str) -> bool:
        """
        Verifies if the user input corresponds to a valid action in the system.

        Args:
            input_by_user (str): The input provided by the user.

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        if input_by_user not in self.allowed_inputs:
            print(f"Invalid input '{input_by_user}'. Please choose a valid option.")
            return False
        return True

    def execute_action(self, input_by_user: str, manager):
        """
        Executes the action based on the user's input by calling the appropriate method
        from the manager object, which interacts with the storage system.

        Args:
            input_by_user (str): The action number chosen by the user.
            manager: The context manager object responsible for handling data operations.
        """
        action = self.allowed_inputs[input_by_user]
        # Perform the appropriate action based on user input
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
            # Display the availability status of a book
            if manager.track_availability():
                print("Available!")
            else:
                print("Not available")
        elif action == "exit":
            print("Exiting the system. Goodbye!")
            exit(0)

    def run(self):
        """
        The main loop of the Library Management System, where the system continuously displays the menu
        and allows the user to choose and execute actions until they choose to exit.
        The context manager is used to ensure proper handling of resources.
        """
        with self.context_manager as manager:
            while True:
                # Display the menu to the user
                self.display_menu()
                # Get user input
                user_input = input("Enter your choice: ").strip()
                # Verify if the input is valid
                if self.verify_input(user_input):
                    # Check if the user chose to exit
                    if user_input == "14":
                        print("Exiting the system. Goodbye!")
                        break
                    # Execute the corresponding action
                    self.execute_action(user_input, manager)
