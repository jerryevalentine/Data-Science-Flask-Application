import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from .SQLiteDB import SQLiteDB  # Importing shared functionality

class SQLiteProcessor:
    
    def get_all_tables(self, database_path):
        """
        Fetches all table names from the SQLite database.

        Parameters:
        database_path (str): Path to the SQLite database.

        Returns:
        list: List of all table names in the database.
        """
        db = SQLiteDB(database_path)
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        db.close()
        return tables
    
    def get_missing_values(self, database_path, table_name):
        """
        Retrieves the count of missing values from a specified table.

        Parameters:
        database_path (str): Path to the SQLite database.
        table_name (str): Name of the table to analyze.

        Returns:
        dict: A dictionary where keys are column names and values are the count of missing values.
        """
        db = SQLiteDB(database_path)
        conn = db.connect()
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        missing_values = df.isnull().sum().to_dict()
        db.close()
        return missing_values
    
    def create_dummy_variables(self, database_path, table_name, exclude_columns=[]):
        """
        Creates dummy variables for categorical columns in a specified table, excluding specific columns.

        Parameters:
        database_path (str): Path to the SQLite database.
        table_name (str): Name of the table to process.
        exclude_columns (list): List of columns to exclude from dummy variable creation.

        Returns:
        None
        """
        db = SQLiteDB(database_path)
        conn = db.connect()
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        
        excluded_df = df[exclude_columns]
        columns_to_encode = [col for col in df.columns if col not in exclude_columns]
        df_to_encode = df[columns_to_encode]
        
        df_encoded = pd.get_dummies(df_to_encode)
        df_combined = pd.concat([df_encoded, excluded_df], axis=1)
        
        df_combined.to_sql(table_name, conn, if_exists='replace', index=False)
        db.close()
    
    def handle_missing_values(self, database_path, table_name):
        """
        Removes rows with missing values from a specified table.

        Parameters:
        database_path (str): Path to the SQLite database.
        table_name (str): Name of the table to process.

        Returns:
        None
        """
        db = SQLiteDB(database_path)
        conn = db.connect()
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        
        df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
        df.dropna(inplace=True)
        
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        db.close()
    
    def scale_numeric_columns(self, database_path, table_name, exclude_columns=[]):
        """
        Scales numeric columns in a specified table, excluding specific columns.

        Parameters:
        database_path (str): Path to the SQLite database.
        table_name (str): Name of the table to process.
        exclude_columns (list): List of columns to exclude from scaling.

        Returns:
        None
        """
        db = SQLiteDB(database_path)
        conn = db.connect()
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        cols_to_scale = [col for col in numeric_cols if col not in exclude_columns]
        
        scaler = StandardScaler()
        df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        db.close()

    def convert_integer_to_boolean(self, column_name, cutoff=None, table_name=None, database_path=None):
        """
        Converts an integer column to boolean based on a cutoff or median value.

        Parameters:
        column_name (str): The column name to convert.
        cutoff (float): Optional cutoff value for conversion. If None, median is used.
        table_name (str): Name of the table in the SQLite database.
        database_path (str): Path to the SQLite database.

        Returns:
        str: Message indicating success or failure.
        """
        if table_name is None or database_path is None:
            return "Error: Both table_name and database_path parameters must be provided."
        
        try:
            db = SQLiteDB(database_path)
            conn = db.connect()
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            df.columns = df.columns.str.strip()
            
            if column_name not in df.columns:
                return f"Error: Column '{column_name}' not found in table '{table_name}'."
            
            new_column_name = column_name + '_boolean'
            if cutoff is not None:
                df[new_column_name] = df[column_name].apply(lambda x: 1 if x >= cutoff else 0)
            else:
                median_value = df[column_name].median()
                df[new_column_name] = df[column_name].apply(lambda x: 1 if x >= median_value else 0)
                if len(df) % 2 != 0:
                    median_index = df[column_name].argsort().iloc[len(df) // 2]
                    df.at[median_index, new_column_name] = 0
            
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            db.close()
            return "Success: Column converted and data saved to the database."
        
        except Exception as e:
            return f"Error: {str(e)}"

    def change_column_data_types(self, database_path, table_name, column_data_types):
        """
        Changes data types of specified columns in a SQLite table.

        Parameters:
        database_path (str): Path to the SQLite database.
        table_name (str): Name of the table in which column data types will be altered.
        column_data_types (dict): Dictionary with column names as keys and new data types as values.

        Returns:
        str: Message indicating success or failure.
        """
        try:
            db = SQLiteDB(database_path)
            conn = db.connect()
            cursor = conn.cursor()
            
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            if not columns:
                return f"Error: Table '{table_name}' does not exist."
            
            new_table_name = f"{table_name}_new"
            columns_definitions = []
            for col in columns:
                col_name = col[1].strip()
                new_col_type = column_data_types.get(col_name, col[2])
                columns_definitions.append(f"{col_name} {new_col_type}")
            
            create_table_sql = f"CREATE TABLE {new_table_name} ({', '.join(columns_definitions)})"
            cursor.execute(create_table_sql)
            
            column_names = [col[1].strip() for col in columns]
            column_names_str = ', '.join(column_names)
            copy_data_sql = f"INSERT INTO {new_table_name} ({column_names_str}) SELECT {column_names_str} FROM {table_name}"
            cursor.execute(copy_data_sql)
            
            cursor.execute(f"DROP TABLE {table_name}")
            cursor.execute(f"ALTER TABLE {new_table_name} RENAME TO {table_name}")
            
            conn.commit()
            db.close()
            return "Success: Data types changed and table updated."
        
        except Exception as e:
            return f"Error: {str(e)}"
