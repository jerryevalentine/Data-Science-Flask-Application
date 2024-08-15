from flask import Flask, render_template, request, redirect, url_for, flash
from libraries.SQLite_Database import SQLite_Database

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE_PATH = 'data_science_application.db'
db = SQLite_Database(DATABASE_PATH)

@app.route('/change_data_type', methods=['GET', 'POST'])
def change_data_type():
    tables = db.get_tables()
    data_types = ["INTEGER", "REAL", "TEXT", "BLOB"]

    if request.method == 'POST':
        selected_table = request.form.get('table')
        selected_column = request.form.get('column')
        new_type = request.form.get('data_type')

        if selected_table and selected_column and new_type:
            try:
                db.update_column_type(selected_table, selected_column, new_type)
                flash('Column type updated successfully!', 'success')
                return redirect(url_for('change_data_type'))
            except Exception as e:
                flash(f'Error: {e}', 'danger')
        else:
            flash('Please select a table, column, and data type.', 'warning')
    
    return render_template('change_data_type.html', tables=tables, data_types=data_types)

@app.route('/update_columns', methods=['POST'])
def update_columns():
    table_name = request.form.get('table_name')
    columns = db.fetch_table_columns(table_name)
    return {'columns': columns}

if __name__ == '__main__':
    app.run(debug=True)
