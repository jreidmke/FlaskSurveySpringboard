from flask import Flask, request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "James"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

SELECTED_SURVEY = 'selected'
RESPONSES = 'responses'

@app.route('/')
def show_selection():
    return render_template('selection.html', surveys = surveys)

@app.route('/selected', methods=["GET", "POST"])
def store_survey():
    session[SELECTED_SURVEY] = request.form.get('selected')
    return redirect('/survey')

@app.route('/survey')
def show_survey():
    return render_template('survey.html', survey = surveys[session[SELECTED_SURVEY]])

@app.route('/responses', methods=['GET', "POST"])
def setup_responses():
    session[RESPONSES] = []
    return redirect('/question/0')

@app.route('/answer', methods=["GET", "POST"])
def answer_question():
    responses = session[RESPONSES]

    if request.form.get('comment') != None:
        responses.append([request.form.get('answer'), request.form.get('comment')])
    else:
        responses.append(request.form.get('answer'))

    session[RESPONSES] = responses

    if request.form.get('answer') == None or not len(responses) == len(surveys[session[SELECTED_SURVEY]].questions):
        return redirect(f"/question/{len(responses)}")
    else:
        return redirect(f"/thanks")

@app.route('/question/<int:idx>')
def show_question(idx):
    return render_template('question.html', survey = surveys[session[SELECTED_SURVEY]], idx = len(session[RESPONSES]))

@app.route('/thanks')
def show_thank_you():
    return render_template('thanks.html')

@app.route('/complete', methods=['POST', 'GET'])
def clear_session():
    session[SELECTED_SURVEY] = ""
    session[RESPONSES] = []
    return redirect('/')