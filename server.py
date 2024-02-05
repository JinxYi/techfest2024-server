import os

from flask import Flask, jsonify, request, render_template
import google.generativeai as palm
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



palm.configure(api_key='AIzaSyBcbCy0PNsrzB-txCnN7YU5OnSb_4FbIwA')
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

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')
@app.route('/send_message',methods=['POST'])
def send_message():
    user_input = request.form.get('user_input')

    if user_input == '0':
        return jsonify({'response': 'Goodbye!'})

    completion = palm.generate_text(
        model="models/text-bison-001",
        prompt=user_input,
        temperature=0,
        max_output_tokens=200,
    )

    bot_response = completion.result
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/flashcards',)
def get_flashcard():
    # Insert flashcard into the database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM flashcards")
    flashcards = cursor.fetchall()
    cursor.close()

    # Convert the result to a list of dictionaries for JSON response
    flashcards_list = [{'id': card[0], 'question': card[1], 'answer': card[2]} for card in flashcards]
    return render_template('flashcards.html',flashcards_list=flashcards_list)


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
        return render_template('hackathon.html', summarizer_result=out)


