#!/usr/bin/python3
"""
MySQL database setup script for ALX_prodev.
Provides functions to connect to the server, create the database,
create the user_data table, and insert data from a CSV file.
"""
import mysql.connector
import csv
import uuid
import sys

# Replace with your actual MySQL credentials
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_mysql_password"
MYSQL_HOST = "localhost"
DATABASE_NAME = "ALX_prodev"

def connect_db():
    """
    Connects to the MySQL database server.

    Returns:
        mysql.connector.connection.MySQLConnection: The connection object,
                                                    or None if connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}", file=sys.stderr)
        return None

def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.

    Args:
        connection (mysql.connector.connection.MySQLConnection):
            The active connection to the MySQL server.
    """
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"Database {DATABASE_NAME} created or already exists.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}", file=sys.stderr)

def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.

    Returns:
        mysql.connector.connection.MySQLConnection: The connection object to ALX_prodev,
                                                    or None if connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=DATABASE_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to {DATABASE_NAME}: {err}", file=sys.stderr)
        return None

def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields.

    Args:
        connection (mysql.connector.connection.MySQLConnection):
            The active connection to the ALX_prodev database.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5, 2) NOT NULL
    )
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}", file=sys.stderr)

def insert_data(connection, filename):
    """
    Inserts data from a CSV file into the user_data table if the database is empty.

    Args:
        connection (mysql.connector.connection.MySQLConnection):
            The active connection to the ALX_prodev database.
        filename (str): The path to the CSV file containing the sample data.
    """
    try:
        cursor = connection.cursor()

        # Check if the table is empty
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]

        if count > 0:
            print("Database already populated. Skipping data insertion.")
            cursor.close()
            return

        print("Inserting data from CSV...")
        insert_query = """
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        """
        data_to_insert = []

        with open(filename, mode='r', encoding='utf-8') as csvfile:
            # Assumes the CSV has header: name,email,age
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Generate a UUID for the primary key
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                # Ensure age is a number before insertion
                try:
                    age = float(row['age'])
                except ValueError:
                    print(f"Skipping row due to invalid age: {row}", file=sys.stderr)
                    continue

                data_to_insert.append((user_id, name, email, age))

        # Execute the bulk insertion
        cursor.executemany(insert_query, data_to_insert)
        connection.commit()
        print(f"Successfully inserted {cursor.rowcount} rows into user_data.")
        cursor.close()

    except FileNotFoundError:
        print(f"Error: CSV file '{filename}' not found.", file=sys.stderr)
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == '__main__':
    # Example usage (for local testing of seed.py)
    # This block is not strictly required by the 0-main.py but is helpful
    # for ensuring the seeding works independently.

    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()

        connection_prodev = connect_to_prodev()
        if connection_prodev:
            create_table(connection_prodev)
            # You must have user_data.csv in the same directory for this to work
            insert_data(connection_prodev, 'user_data.csv')
            connection_prodev.close()
