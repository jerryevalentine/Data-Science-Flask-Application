import sqlite3
import pandas as pd
import os
from flask import g

class SQLiteDB:
    
    def __init__(self, db_path):
        """
        Initializes the SQLiteDB class.

        Parameters:
        db_path (str): The file path to the SQLite database.
        """
        self.db_path = db_path

    def connect(self):
        """
        Connects to the SQLite database.

        If a connection doesn't exist in Flask's g object, it establishes a connection.

        Returns:
        sqlite3.Connection: SQLite database connection.
        """
        if 'conn' not in g:
            g.conn = sqlite3.connect(self.db_path)
            g.conn.row_factory = sqlite3.Row  # Enable row factory for dictionary-like rows
        return g.conn
    
    def create_database(self, db_name):
        """
        Creates a new SQLite database file.

        Parameters:
        db_name (str): The name of the new database file to create.

        Returns:
        str: The full path to the created database.
        """
        os.makedirs(self.db_path, exist_ok=True)
        db_full_path = os.path.join(self.db_path, db_name)
        connection = sqlite3.connect(db_full_path)
        connection.close()
        return db_full_path

    def close(self):
        """
        Closes the current SQLite database connection.

        If the connection exists in Flask's g object, it is closed and removed.
        """
        conn = g.pop('conn', None)
        if conn:
            conn.close()

    def update_column_type(self, table_name, column_name, new_type):
        """
        Updates the data type of a specific column in a table.

        Parameters:
        table_name (str): The name of the table.
        column_name (str): The name of the column to change.
        new_type (str): The new data type for the column.
        """
        conn = self.connect()
        temp_table_name = f"{table_name}_temp"
        try:
            columns_query = f'PRAGMA table_info("{table_name}");'
            columns_df = pd.read_sql_query(columns_query, conn)
            
            columns = [
                f"{row['name']} {new_type if row['name'] == column_name else row['type']}"
                for _, row in columns_df.iterrows()
            ]
            columns_str = ', '.join(columns)

            conn.execute(f"CREATE TABLE {temp_table_name} ({columns_str});")
            conn.execute(f"INSERT INTO {temp_table_name} SELECT * FROM {table_name};")
            conn.execute(f"DROP TABLE {table_name};")
            conn.execute(f"ALTER TABLE {temp_table_name} RENAME TO {table_name};")
            conn.commit()
        except sqlite3.OperationalError as e:
            conn.rollback()
            raise Exception(f"Failed to update column type: {e}")

    def get_tables(self):
        """
        Retrieves a list of all tables in the SQLite database.

        Returns:
        list: A list of table names in the database.
        """
        conn = self.connect()
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables_df = pd.read_sql_query(query, conn)
        return tables_df['name'].tolist()

    def fetch_table_columns(self, table_name):
        """
        Retrieves the column names of a specific table.

        Parameters:
        table_name (str): The name of the table to retrieve columns from.

        Returns:
        list: A list of column names from the table.
        """
        conn = self.connect()
        query = f'PRAGMA table_info("{table_name}");'
        df = pd.read_sql_query(query, conn)
        return df['name'].tolist()

    def count_missing_values(self, table_name):
        """
        Counts missing values for each column in a table.

        Parameters:
        table_name (str): The name of the table to analyze for missing values.

        Returns:
        dict: A dictionary of column names with the corresponding count of missing values.
        """
        conn = self.connect()
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, conn)
        return df.isnull().sum().to_dict()

    def delete_missing_values(self, table_name):
        """
        Deletes rows that have missing values in any column in a table.

        Parameters:
        table_name (str): The name of the table from which to delete rows with missing values.

        Returns:
        bool: True if deletion is successful, False otherwise.
        """
        conn = self.connect()
        try:
            query = f"DELETE FROM {table_name} WHERE {' OR '.join([f'{col} IS NULL' for col in self.fetch_table_columns(table_name)])};"
            conn.execute(query)
            conn.commit()
            return True
        except sqlite3.Error as e:
            conn.rollback()
            return False, str(e)

    def fetch_query(self, query):
        """
        Executes a raw SQL query and fetches the results as a pandas DataFrame.

        Parameters:
        query (str): The SQL query to execute.

        Returns:
        pd.DataFrame: A DataFrame containing the query results.
        """
        conn = self.connect()
        return pd.read_sql_query(query, conn)

    def fetch_table(self, table_name):
        """
        Fetches all records from a specific table.

        Parameters:
        table_name (str): Name of the table to fetch records from.

        Returns:
        pd.DataFrame: DataFrame containing all records from the table.
        """
        conn = self.connect()
        query = f"SELECT * FROM {table_name};"
        return pd.read_sql_query(query, conn)

    def insert_dataframe_to_db(self, df, table_name):
        """
        Inserts a pandas DataFrame into the SQLite database.

        Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        table_name (str): The name of the table to insert data into.
        """
        conn = self.connect()
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.commit()

    def clear_table(self, table_name):
        """
        Deletes all records from a table.

        Parameters:
        table_name (str): The name of the table to clear.
        """
        conn = self.connect()
        query = f"DELETE FROM {table_name};"
        conn.execute(query)
        conn.commit()

    def delete_record(self, table_name, condition):
        """
        Deletes a record from the table that matches a specific condition.

        Parameters:
        table_name (str): The name of the table.
        condition (str): The SQL condition to specify which records to delete.
        """
        conn = self.connect()
        query = f"DELETE FROM {table_name} WHERE {condition};"
        conn.execute(query)
        conn.commit()

    def update_record(self, table_name, columns, values, condition):
        """
        Updates a record in the table with new values based on a condition.

        Parameters:
        table_name (str): The name of the table.
        columns (list): A list of column names to update.
        values (list): The new values for the specified columns.
        condition (str): The SQL condition to specify which records to update.
        """
        conn = self.connect()
        set_clause = ', '.join([f"{col} = ?" for col in columns])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition};"
        conn.execute(query, values)
        conn.commit()

    def insert_record(self, table_name, columns, values):
        """
        Inserts a new record into a table.

        Parameters:
        table_name (str): The name of the table.
        columns (list): A list of column names for the new record.
        values (list): The corresponding values to insert into the columns.
        """
        conn = self.connect()
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['?'] * len(values))
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});"
        conn.execute(query, values)
        conn.commit()

    def get_sqlite_metadata(self):
        """
        Retrieves metadata for all tables in the SQLite database.

        Returns:
        pd.DataFrame: A DataFrame containing table, column names, and data types.
        """
        conn = self.connect()
        query_metadata = "SELECT name FROM sqlite_master WHERE type='table';"
        tables_df = pd.read_sql_query(query_metadata, conn)
        metadata = []

        for table in tables_df['name']:
            columns_query = f'PRAGMA table_info("{table}");'
            columns_df = pd.read_sql_query(columns_query, conn)
            for _, row in columns_df.iterrows():
                metadata.append((table, row['name'], row['type']))

        return pd.DataFrame(metadata, columns=['Table Name', 'Column Name', 'Data Type'])
