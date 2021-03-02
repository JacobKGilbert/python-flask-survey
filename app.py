from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blahblahblah123'

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_route():
  return render_template('home.html')

@app.route('/question/<int:ques_num>')
def questions_route(ques_num):
  if ques_num != len(responses):
    ques_num = len(responses)

    if ques_num > len(satisfaction_survey.questions)-1:
      flash("You have already answered all the questions.")
      return redirect('/thankyou')
      
    flash('Please answer questions in order.')
    return redirect(f'/question/{ques_num}')
    
  next_q = ques_num + 1
  return render_template(
    'question.html', 
    title=satisfaction_survey.title, 
    instruction=satisfaction_survey.instructions, 
    question=satisfaction_survey.questions[ques_num],
    next_q=next_q)

@app.route('/answer<int:next_q>', methods=['POST'])
def answer_route(next_q):
  responses.append(request.form['options'])

  if next_q < len(satisfaction_survey.questions):
    return redirect(f'/question/{next_q}')
  else:
    return redirect('/thankyou')

@app.route('/thankyou')
def thank_route():
  return render_template('thanks.html')
