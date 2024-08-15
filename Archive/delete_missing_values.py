from flask import Flask, render_template, request, flash
from libraries.SQLiteDatabasePreProcessor import SQLiteDatabasePreProcessor

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Necessary for flashing messages

# Define the database path
database_path = 'database/data_science_application.db'

@app.route('/delete_missing_values', methods=['GET', 'POST'])
def delete_missing_values():
    preprocessor = SQLiteDatabasePreProcessor()
    tables = preprocessor.get_all_tables(database_path)

    if request.method == 'POST':
        selected_table = request.form.get('selected_table')
        
        if request.form.get('action') == 'Show Missing Values':
            missing_values = preprocessor.get_missing_values(database_path, selected_table)
            return render_template('delete_missing_values.html', tables=tables, selected_table=selected_table, missing_values=missing_values)
        
        elif request.form.get('action') == 'Delete Missing Values':
            try:
                preprocessor.handle_missing_values(database_path, selected_table)
                flash(f"All missing values in table '{selected_table}' have been successfully deleted.", 'success')
            except Exception as e:
                flash(f"Error: {str(e)}", 'danger')

    return render_template('delete_missing_values.html', tables=tables)

if __name__ == '__main__':
    app.run(debug=True)
