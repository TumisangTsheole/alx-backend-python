# 🐍 Python Generators and Database Streaming (0x00)

This repository contains Python scripts demonstrating the effective use of **generators** (`yield`) to handle large datasets from a MySQL database in a **memory-efficient** and **lazy-loading** manner.

The primary goal is to stream data, process it in batches, and calculate aggregates without loading the entire result set into Python's memory.

## 📁 Files

| File | Description | Core Generator Concept |
| :--- | :--- | :--- |
| `seed.py` | Sets up the MySQL database (`ALX_prodev`), creates the `user_data` table, and populates it with data from `user_data.csv`. | N/A (Setup) |
| `0-stream_users.py` | Implements `stream_users()`, a generator that fetches and yields **individual rows** one by one from the `user_data` table. | **Row-by-Row Streaming** |
| `1-batch_processing.py` | Implements `stream_users_in_batches()` to fetch data in configurable **chunks**, and `batch_processing()` to filter users based on age, utilizing nested generators. | **Batch Yielding & Processing Pipelines** |
| `2-lazy_paginate.py` | Implements `lazy_paginate()`, a generator that fetches data one **page** at a time (`LIMIT/OFFSET`), only requesting the next page when the current one is consumed. | **Lazy Pagination** |
| `4-stream_ages.py` | Implements `stream_user_ages()` to yield ages one by one, and `calculate_average_age()` to compute the average age **incrementally**, achieving memory-efficient aggregation. | **Memory-Efficient Aggregation** |

## ⚙️ Setup and Dependencies

1.  **Install MySQL Connector:**
    ```bash
    pip install mysql-connector-python
    ```
2.  **Database Configuration:**
    Ensure you update the MySQL credentials (user, password, host) in **ALL** Python files (`seed.py`, `0-stream_users.py`, `1-batch_processing.py`, `2-lazy_paginate.py`, `4-stream_ages.py`) to match your local setup:
    ```python
    MYSQL_PASSWORD = "your_mysql_password" # <--- UPDATE THIS IN ALL SCRIPTS
    ```
3.  **Data File:**
    Ensure the `user_data.csv` file is present in the repository root for `seed.py` to populate the database.

## 🚀 Usage

### 1. Database Initialization

Run `0-main.py` (or execute the `seed.py` functions directly) to set up the database and populate the table:

```bash
./0-main.py
# Output will confirm connection, database creation, table creation, and data insertion.
