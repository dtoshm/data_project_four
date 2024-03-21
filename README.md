# data_project_four
Inventory Management Console Application


Overview

This project is a console application designed to help users easily interact with inventory data using CSV file manipulation and SQLAlchemy ORM methods. The application allows users to read, clean, and import data from CSV files into a SQLite database. It also provides functionalities such as viewing, creating, editing, and deleting records in the database, as well as generating data analysis reports. Additionally, users can create backups of the database in the form of CSV files.


Features

CSV Data Import: Read and import data from CSV files into a database.
Data Cleaning: Clean imported data before adding it to the database.
CRUD Operations: Perform Create, Read, Update, and Delete operations on database records.
Data Analysis: Display analysis reports based on the stored data.
Backup Creation: Create backup CSV files reflecting the current state of the database.


Technologies Used

Python: Core programming language for the application.
CSV: Handling CSV file reading, writing, and data manipulation.
SQLAlchemy: Utilized for ORM (Object-Relational Mapping) to interact with the SQLite database.
Console Interface: Command-line interface for user interaction.


Installation

Clone the repository: git clone "https://github.com/dtoshm/data_project_four"
Navigate to the project directory
Install dependencies: pip install -r requirements.txt
Run the application: python main.py


Usage

Upon running the application, follow the on-screen instructions to perform various actions.
Use menu options to import CSV data, manage inventory records, generate reports, and create backups.


Project Structure

app.py: Entry point of the application.
models.py: Contains database setup and SQLAlchemy ORM models.
requirements.txt: List of Python dependencies.
