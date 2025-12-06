#!/usr/bin/python3
"""
Generator functions to stream user ages and calculate the average age
in a memory-efficient manner.
"""
import mysql.connector
import sys

# Assuming seed.py is in the same directory and handles MySQL connection
try:
    seed = __import__('seed')
except ImportError:
    print("Error: 'seed.py' module not found. Ensure it is in the same directory.", file=sys.stderr)
    sys.exit(1)

# --- Configuration (Must match the settings in seed.py) ---
# NOTE: Using placeholder values, replace with your actual password
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_mysql_password" 
MYSQL_HOST = "localhost"
DATABASE_NAME = "ALX_prodev"
# ---------------------------------------------------------

def stream_user_ages():
    """
    Connects to the ALX_prodev database and streams the 'age' field
    from the user_data table one by one.

    Yields:
        float: The age of a single user.
    """
    connection = None
    try:
        # Connect to the ALX_prodev database
        connection = seed.connect_to_prodev()
        
        if not connection:
            return

        # Use buffered=False for streaming, dictionary=False (default) for tuples
        cursor = connection.cursor(buffered=False)
        
        # Select only the age column
        select_query = "SELECT age FROM user_data"
        cursor.execute(select_query)

        # Loop 1: Iterates over the cursor, fetching one row/age per iteration
        for row in cursor:
            # row is a tuple (age,), extract the first element and convert to float
            try:
                age = float(row[0])
                yield age
            except (ValueError, IndexError):
                # Skip invalid or missing age data
                continue
            
    except mysql.connector.Error as err:
        print(f"Database error in stream_user_ages: {err}", file=sys.stderr)
        
    except Exception as e:
        print(f"An unexpected error occurred in stream_user_ages: {e}", file=sys.stderr)
        
    finally:
        # Ensure the connection and cursor are closed
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def calculate_average_age():
    """
    Calculates the average age of all users using the streaming generator.
    This process is memory-efficient as it aggregates data on the fly.

    Returns:
        float: The calculated average age, or None if no data is streamed.
    """
    total_age = 0.0
    count = 0
    
    # Loop 2: Iterate over the ages yielded by the generator
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return None  # Return None if no ages were found
    
    # Compute and return the average
    return total_age / count

if __name__ == '__main__':
    # Compute the average age
    average_age = calculate_average_age()
    
    if average_age is not None:
        # Print the result formatted to two decimal places
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("Average age could not be calculated (No data or connection error).")
