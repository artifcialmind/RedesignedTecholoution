# Library Management System (Redesigned code)

This repo consists of redesigned code for Library management system which uses pythonic ways to define and structure the system. 

## Features

- **User Management**: Add, verify, update, and delete users easily.
- **Book Management**: Manage books by adding, verifying, updating, and deleting book records.
- **Data Persistence**: User and book data are stored in JSON files, ensuring data is preserved between sessions.
- **Error Handling**: Robust error handling for file operations and JSON decoding.

## Technologies Used

- Python 3.12
- Pydantic for data modeling
- JSON for data storage

## Installation

1. Clone the repository
2. Install pydantic
   ```bash
   pip install pydantic
3. Run main.py
   ```bash
   python main.py
4. Follow the interactive menu to manage users and books.

## File Structure
```bash
project-directory/
│
├── Menu/
│   └── menu.py          # Menu handling for user interactions
│
├── Pydantic_Models/
│   └── pydantic_models.py  # Pydantic models for User and Book data
│
├── Storage/
|   └── BookDB  # User database management
|   |    └── book_storage_handling.py  #  class handling book db
|   |    └── BookData.json     # json storing book data
|   └── UserDB
|   |     └── user_storage_handling.py    # class handling user db
|   |    └── UserData.json      # json storing user data
|   ├── AssignmentManager.json       # json storing book-assignment data
|   └── storage.py             # class handling combination of both UserDB and BookDB as inheritence
|
└── main.py              # Main entry point for the application

