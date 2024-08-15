from flask import Flask, request, render_template, redirect, url_for, flash
from libraries.SQLite_Database import SQLite_Database
import io
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Path to your SQLite database
db_path = 'database/data_science_application.db'

# Initialize the SQLite_Database class
database = SQLite_Database(db_path)

@app.route('/')
def index():
    return render_template('data_science_application_basemodels.html')

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
