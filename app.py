from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey
from surveys import personality_quiz as quiz #learn how to select elements using bs4 come back to this

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def show_survey():
    """Pick a survey."""

    return render_template("survey_start.html", survey=survey, quiz=quiz)

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/finished")

    else:
        return redirect(f"/questions/{len(responses)}")
    


@app.route("/quiz/answer", methods=["POST"])
def handle_question_quiz():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(quiz.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/finished")

    else:
        return redirect(f"/quiz/questions/{len(responses)}")



@app.route("/questions/<int:num>")
def questions(num):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")
    
    if (len(responses)==len(survey.questions)):
        return redirect("/finished")
    
    if (len(responses) != num):
        flash(f"Invalid question iq: {num}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[num]
    return render_template(
        "question.html", question_num = num, question = question)

@app.route("/quiz/questions/<int:num>")
def quiz_questions(num):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")
    
    if (len(responses)==len(quiz.questions)):
        return redirect("/finished")
    
    if (len(responses) != num):
        flash(f"Invalid question iq: {num}.")
        return redirect(f"/quiz/questions/{len(responses)}")
    
    question = quiz.questions[num]
    return render_template(
        "quiz_question.html", question_num = num, question = question)


@app.route("/begin", methods=["POST"])
def begin_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route("/beginquiz", methods=["POST"])
def begin_quiz():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/quiz/questions/0")



@app.route("/finished")
def complete():

    return render_template("finished.html")

