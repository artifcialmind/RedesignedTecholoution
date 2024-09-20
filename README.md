# Library Management System (Redesigned code)

This repo consists of redesigned code for Library management system which uses pythonic ways to define and structure the system. 

## Features

- **User Management**: Add, verify, update, search, list and delete users easily.
- **Book Management**: Manage books by adding, verifying, updating, searching, listing, and deleting book records.
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
│   └── pydantic_models.py  # Pydantic models for User, Book and Assignment data
│
├── Storage/
|   └── BookDB  # User database management
|   |    └── book_storage_handling.py  #  class handling book db
|   |    └── BookData.json     # json storing book data
|   └── UserDB/
|   |     └── user_storage_handling.py    # class handling user db
|   |    └── UserData.json      # json storing user data
|   ├── AssignmentManager.json       # json storing book-assignment data
|   └── storage.py             # class handling combination of both UserDB and BookDB as inheritence
|
└── main.py              # Main entry point for the application
```
### The picture above describes the file structure and architecture. The choice has been made on following parameters:
1) Modularity: The storage has been explicitly set to User and Book including the json and corresponding codes which helps in increasing the modularity and decreasing effort of debugging.
2) Pydantic model usage: Under the Pydantic_Models we can pydantic_models.py that serves as a common classes that has been used by various other classes. This ensures data integrity throughout the pipeline.
3) Storage.py: This is under the directory Storage and provides multiple inheritence from UserDB and BookDB and serves as a common way point to serve all the storage needs.
4) JSON storage: For easy visualisation and fast retrival times when converted into dictionary, reducing searching times.
5) Menu: Under the Menu directory more functionalities can be added over time. At the moment it consists of a single class serving the menu navigation needs.

Overall this architecture has been made by thought of modularity, efficiency, durablity and scalablity in mind.


## Testing and Validation
### 1) BookDB Features:

![image](https://github.com/user-attachments/assets/21ef3053-5119-4853-b389-41d32165a72a)

![image](https://github.com/user-attachments/assets/9171b9c9-8c4b-4fda-baf8-0fdf0e62139c)

![image](https://github.com/user-attachments/assets/d0bb1111-9ca7-4782-b9da-e8b757e39596)

### 2) UserDB Features:

![image](https://github.com/user-attachments/assets/3e4dbcfc-da85-4dbb-b020-c06ecd53f187)

   
![image](https://github.com/user-attachments/assets/d699eaa2-9fdb-4379-839f-1b875cb4bb0e)

### 3) Check in and out testing:

![image](https://github.com/user-attachments/assets/482e9ed2-df5c-4101-804f-66ebfdad6c78)

![image](https://github.com/user-attachments/assets/6b9ece7f-7d9b-4e1a-ba52-a29a7c5794cc)

![image](https://github.com/user-attachments/assets/e31420b0-597f-4ac1-9b86-ae415800868b)

![image](https://github.com/user-attachments/assets/4b1dad65-267a-4321-82fb-0ff320e2562f)

### 4) Persistant Storage testing:

UserDB:

![image](https://github.com/user-attachments/assets/c3d521f8-bedd-4a23-aa24-953cb3b45c4e)

BookDB:

![image](https://github.com/user-attachments/assets/9b28b908-ccf8-4a13-8fd0-ca0555d8ac06)












