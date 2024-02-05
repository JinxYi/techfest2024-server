import os

from flask import Flask, request, render_template


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
app.config['DEBUG'] = True
app.config.from_mapping(
    SECRET_KEY='HAHAHI',
    static_folder='static',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

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

@app.route('/summarize', methods=['POST'])
def summarize():
    if request.method == 'POST':
        user_input = request.form.get('notes')
        max_length = int(request.form.get('word_count'))
        summarizer_output = summarizer(user_input, max_length=max_length, min_length=30, do_sample=False)
        return summarizer_output



