#!/usr/bin/python3
"""
Generator function to stream rows one by one from the user_data table.
"""
import mysql.connector
import sys

# --- Configuration (Must match the settings in seed.py) ---
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_mysql_password"  # Replace with your actual password
MYSQL_HOST = "localhost"
DATABASE_NAME = "ALX_prodev"
# ---------------------------------------------------------

def stream_users():
    """
    Connects to the ALX_prodev database and uses a generator to stream
    rows from the user_data table one by one.

    Yields:
        dict: A dictionary representing a single user row.
    """
    connection = None
    try:
        # Establish connection to the database
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=DATABASE_NAME
        )
        
        # Use cursor with buffered=False to stream results
        # dictionary=True makes the results a dict (key=column name)
        cursor = connection.cursor(dictionary=True, buffered=False)
        
        select_query = "SELECT user_id, name, email, age FROM user_data"
        cursor.execute(select_query)

        # The cursor object is an iterable that fetches rows one-by-one
        # when buffered=False is used. This allows us to use a single loop
        # to yield each row as it's fetched from the database.
        for row in cursor:
            yield row
            
    except mysql.connector.Error as err:
        print(f"Database error: {err}", file=sys.stderr)
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        
    finally:
        # Ensure the connection and cursor are closed
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    # This block can be used for local testing
    from itertools import islice
    print("Streaming first 3 users:")
    for user in islice(stream_users(), 3):
        print(user)
