import os
from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL  # Added import for MySQL

from transformers import T5ForConditionalGeneration,T5Tokenizer
from textwrap3 import wrap
import torch

from util.flashcard_generator import get_question, get_keywords
from util.summarizer import summarizer

# installing english language pack
import spacy
nlp = spacy.load("en_core_web_sm")
import en_core_web_sm
nlp = en_core_web_sm.load()


template_dir = os.path.abspath('./template')
test_config = None

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
def get_flashcard():
    # Insert flashcard into the database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM flashcards")
    flashcards = cursor.fetchall()
    cursor.close()

    # Convert the result to a list of dictionaries for JSON response
    flashcards_list = [{'id': card[0], 'question': card[1], 'answer': card[2]} for card in flashcards]
    print("flashcards_list", flashcards_list)
    return jsonify({'flashcards': flashcards_list})

# initlilizing summary model
summary_model = T5ForConditionalGeneration.from_pretrained('t5-base')
summary_tokenizer = T5Tokenizer.from_pretrained('t5-base')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
summary_model = summary_model.to(device)

# initializing flashcard model
question_model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_squad_v1')
question_tokenizer = T5Tokenizer.from_pretrained('ramsrigouthamg/t5_squad_v1')
question_model = question_model.to(device)
@app.route('/summarize', methods=['POST'])
def summarize():
    if request.method == 'POST':
        user_input = request.form.get('notes')

        #generating summarized text
        summarized_text = summarizer(user_input,summary_model,summary_tokenizer)
        out = ''
        for wrp in wrap(summarized_text, 150):
            out+=wrp

        #generating flashcards
        imp_keywords = get_keywords(user_input,summarized_text)

        flashcard_data = []
        for answer in imp_keywords:
          ques = get_question(summarized_text,answer,question_model,question_tokenizer)
          flashcard_data.append({"question":ques, "answer":answer.capitalize()})
        
        # Create a summary record
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO summary (summary) VALUES (%s)", (out,))
        mysql.connection.commit()

        # Get the ID of the newly created summary
        cursor.execute("SELECT LAST_INSERT_ID()")
        summarization_id = cursor.fetchone()[0]

        for card in flashcard_data:
           
            # add flashcard to db
            # Create a flashcard record referencing the summary ID
            cursor.execute("INSERT INTO flashcards (question, answer, summarization_id) VALUES (%s, %s, %s)", (card['question'], card['answer'], summarization_id))
            mysql.connection.commit()

        cursor.close()
        return render_template('hackathon.html', out=out)


