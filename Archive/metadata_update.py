from flask import Flask, render_template, request, g
from libraries.SQLite_Database import SQLite_Database

app = Flask(__name__)
db_path = 'database/data_science_application.db'
db = SQLite_Database(db_path)

@app.teardown_appcontext
def close_db(error):
    db.close()

@app.route('/metadata_update', methods=['GET', 'POST'])
def metadata_update():
    tables = db.get_tables()
    selected_table = None
    metadata = None

    if request.method == 'POST':
        selected_table = request.form.get('table_name')
        if selected_table:
            metadata = db.fetch_table(selected_table)

    return render_template(
        'metadata_update.html',
        tables=tables,
        selected_table=selected_table,
        metadata=metadata
    )


if __name__ == '__main__':
    app.run(debug=True)
