import os

from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL  # Added import for MySQL

from transformers import pipeline
template_dir = os.path.abspath('./template')
test_config = None

MAX_LENGTH = 130

## set up summarizer model
# using pipeline API for summarization task
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


## server code
test_config = None
# create and configure the app
app = Flask(__name__, instance_relative_config=True, template_folder=template_dir)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root1234'
app.config['MYSQL_DB'] = 'flashcard_db'

app.config['DEBUG'] = True
app.config.from_mapping(
    SECRET_KEY='HAHAHI',
    static_folder='static',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

mysql = MySQL(app)

@app.route('/')
def hack():
    return render_template('hackathon.html')

if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.route('/flashcards',)
def add_flashcard():
    # Insert flashcard into the database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM flashcards")
    flashcards = cursor.fetchall()
    cursor.close()

    # Convert the result to a list of dictionaries for JSON response
    flashcards_list = [{'id': card[0], 'question': card[1], 'answer': card[2]} for card in flashcards]
    print("flashcards_list", flashcards_list)
    return jsonify({'flashcards': flashcards_list})

@app.route('/summarize', methods=['POST'])
def summarize():
    if request.method == 'POST':
        user_input = request.form.get('notes')
        max_length = int(request.form.get('word_count'))
        summarizer_output = summarizer(user_input, max_length=max_length, min_length=30, do_sample=False)
        out = summarizer_output[0]['summary_text']

        # add flashcard to db
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO flashcards (question, answer) VALUES (%s, %s)", (None, out))
        mysql.connection.commit()
        cursor.close()
        return render_template('hackathon.html', out)


