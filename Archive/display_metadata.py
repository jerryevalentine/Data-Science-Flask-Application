from flask import Flask, render_template, request, redirect, url_for
from libraries.SQLite_Database import SQLite_Database

app = Flask(__name__)
db_path = 'database/data_science_application.db'
db = SQLite_Database(db_path)

@app.route('/display_metadata', methods=['GET', 'POST'])
def display_metadata():
    tables = db.get_tables()
    metadata = None
    selected_table = None
    
    if request.method == 'POST':
        selected_table = request.form.get('table_name')
        if selected_table:
            metadata = db.get_table_metadata(selected_table)
    
    return render_template('display_metadata.html', tables=tables, metadata=metadata, selected_table=selected_table)

@app.route('/clear_metadata', methods=['POST'])
def clear_metadata():
    return redirect(url_for('display_metadata'))

if __name__ == '__main__':
    app.run(debug=True)
