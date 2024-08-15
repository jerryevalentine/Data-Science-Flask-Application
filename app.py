from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sys

# Add the libraries directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'libraries'))
"""
def use_api_key():
    OPENAI_API_KEY = config.OPENAI_API_KEY
    # Use the API key in your function
    print(f"Using API Key: {OPENAI_API_KEY}")
use_api_key()
"""
from libraries.chatgpt_utils import get_chatgpt_analysis, get_chatgpt_response
from libraries.db_utils import query_table, get_metadata_tables, get_table_names, get_db_connection
from libraries.dataframe_utils import get_dataframe_statistics

base_dir = os.path.dirname(os.path.abspath(__file__))
database_path = 'resources/spotify.db'

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for session management, such as flash messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display_data', methods=['GET', 'POST'])
def display_data():
    metadata = get_metadata_tables(database_path)
    selected_table = None
    table_data = None
    table_stats = None
    if request.method == 'POST':
        selected_table = request.form.get('table')
        if selected_table:
            table_data = query_table(selected_table, database_path, num_of_rows=10)
            if not table_data.empty:
                table_stats = get_dataframe_statistics(table_data)

    return render_template('display_data.html', metadata=metadata, selected_table=selected_table, table_data=table_data, table_stats=table_stats)

@app.route('/chatgpt_analysis', methods=['GET', 'POST'])
def chatgpt_analysis():
    if request.method == 'POST':
        if 'clear' in request.form:
            return redirect(url_for('chatgpt_analysis'))
        
        model_name = request.form['model_name']
        user_input = request.form['user_input']
        # Fetch necessary data for ChatGPT analysis
        chatgpt_results = get_chatgpt_analysis(OPENAI_API_KEY, model_name, database_path, table_name='neural_network_results', user_input=user_input)
        return render_template('chatgpt_analysis.html', chatgpt_results=chatgpt_results, model_names=get_table_names(database_path, table_name='neural_network_results'))
    
    model_names = get_table_names(database_path, table_name='neural_network_results')
    return render_template('chatgpt_analysis.html', model_names=model_names)

@app.route('/chatgpt_conversation', methods=['GET', 'POST'])
def chatgpt_conversation():
    chatgpt_response = None
    if request.method == 'POST':
        user_input = request.form['user_input']
        chatgpt_response = get_chatgpt_response(OPENAI_API_KEY, user_input)
    
    return render_template('chatgpt_conversation.html', chatgpt_response=chatgpt_response)

@app.route('/data_dictionary')
def data_dictionary():
    conn = get_db_connection(database_path)
    df = query_table('data_dictionary', database_path)
    conn.close()
    data_html = df.to_html(classes='table table-striped', index=False)
    return render_template('data_dictionary.html', table=data_html)

if __name__ == '__main__':
    app.run(debug=True)