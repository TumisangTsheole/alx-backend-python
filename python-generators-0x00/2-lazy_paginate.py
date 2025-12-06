#!/usr/bin/python3
"""
Generator functions to simulate lazy loading of paginated data from a database.
"""
import sys
# Assuming seed.py is in the same directory and handles MySQL connection
try:
    seed = __import__('seed')
except ImportError:
    print("Error: 'seed.py' module not found. Ensure it is in the same directory.", file=sys.stderr)
    sys.exit(1)


def paginate_users(page_size, offset):
    """
    Fetches a single page of user data from the database.

    Args:
        page_size (int): The maximum number of rows to return.
        offset (int): The starting point (number of rows to skip).

    Returns:
        list[dict]: A list of user dictionaries for the specified page.
    """
    connection = None
    try:
        # Connect to the ALX_prodev database (function from seed.py)
        connection = seed.connect_to_prodev()
        
        if not connection:
            return []

        # Use dictionary=True for dict results
        cursor = connection.cursor(dictionary=True)
        
        # SQL query using LIMIT and OFFSET for pagination
        query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
        cursor.execute(query)
        
        # Fetch all rows for the current page
        rows = cursor.fetchall()
        
        cursor.close()
        return rows
        
    except Exception as e:
        print(f"Error in paginate_users: {e}", file=sys.stderr)
        return []
        
    finally:
        # Ensure the connection is closed
        if connection and connection.is_connected():
            connection.close()


def lazy_paginate(page_size):
    """
    A generator function that lazily loads pages of user data.
    It stops fetching when an empty page (no more data) is returned.

    Args:
        page_size (int): The number of users per page.

    Yields:
        list[dict]: A single page of user data.
    """
    offset = 0
    
    # Loop 1: Continually request pages until an empty page is returned
    while True:
        # Fetch the next page using the utility function
        page = paginate_users(page_size, offset)
        
        if not page:
            # If the page is empty, it means we've reached the end of the data
            break
            
        # Yield the full page (list of dicts)
        yield page
        
        # Update the offset for the next page request
        offset += page_size


# The script is expected to import lazy_pagination, so alias the function
lazy_pagination = lazy_paginate
