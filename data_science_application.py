# business_glossary.py
from flask import Flask, render_template, request, redirect, url_for, flash
from libraries.SQLite_Database import SQLite_Database
from libraries.SQLiteDatabasePreProcessor import SQLiteDatabasePreProcessor
import io
import pandas as pd

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Necessary for flashing messages

db_path = 'database/data_science_application.db'
database = SQLite_Database(db_path)
table_name = 'business_metadata'

@app.teardown_appcontext
def close_connection(exception):
    database.close()

@app.route('/')
def index():
    return render_template('data_science_application_index.html')

@app.route('/business_glossary')
def business_glossary():
    # Fetch the current data from the business_metadata table
    df = database.fetch_table(table_name)
    return render_template('business_glossary.html', table_data=df.to_dict(orient='records'))

@app.route('/insert', methods=['POST'])
def insert():
    # Extract data from form fields
    columns = ['business_glossary_term_id', 'business_glossary_term', 'business_glossary_definition']
    values = [request.form.get(col) for col in columns]
    # Insert record into database
    database.insert_record(table_name, columns, values)
    return redirect(url_for('business_glossary'))

@app.route('/update', methods=['POST'])
def update():
    # Extract data from form fields
    set_columns = ['business_glossary_term', 'business_glossary_definition']
    set_values = [request.form.get(col) for col in set_columns]
    where_clause = f"business_glossary_term_id = {request.form.get('business_glossary_term_id')}"
    # Update record in database
    database.update_record(table_name, set_columns, set_values, where_clause)
    return redirect(url_for('business_glossary'))

@app.route('/delete', methods=['POST'])
def delete():
    # Extract the term_id from the form
    term_id = request.form.get('business_glossary_term_id')
    where_clause = f"business_glossary_term_id = {term_id}"
    # Delete record from database
    database.delete_record(table_name, where_clause)
    return redirect(url_for('business_glossary'))

@app.route('/clear', methods=['POST'])
def clear():
    # Clear all records from the business_metadata table
    database.clear_table(table_name)
    return redirect(url_for('business_glossary'))

@app.route('/delete_missing_values', methods=['GET', 'POST'])
def delete_missing_values():
    preprocessor = SQLiteDatabasePreProcessor()
    tables = preprocessor.get_all_tables(db_path)

    if request.method == 'POST':
        selected_table = request.form.get('selected_table')
        
        if request.form.get('action') == 'Show Missing Values':
            missing_values = preprocessor.get_missing_values(db_path, selected_table)
            return render_template('delete_missing_values.html', tables=tables, selected_table=selected_table, missing_values=missing_values)
        
        elif request.form.get('action') == 'Delete Missing Values':
            try:
                preprocessor.handle_missing_values(db_path, selected_table)
                flash(f"All missing values in table '{selected_table}' have been successfully deleted.", 'success')
            except Exception as e:
                flash(f"Error: {str(e)}", 'danger')

    return render_template('delete_missing_values.html', tables=tables)


@app.route('/file_upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        table_name = request.form['table_name']
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and file.filename.endswith('.csv'):
            try:
                file_stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                df = pd.read_csv(file_stream)
                database.insert_dataframe_to_db(df, table_name)
                flash('File successfully uploaded and inserted into the database!')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'An error occurred: {str(e)}')
                return redirect(request.url)
        else:
            flash('Only CSV files are allowed')
            return redirect(request.url)
    
    return render_template('file_upload.html')

    
if __name__ == '__main__':
    app.run(debug=True)
