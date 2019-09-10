
from flask import Flask, render_template, request

import data_handler

from datetime import datetime

app = Flask(__name__)

@app.route('/')
def route_home_page():
    return render_template('home_page.html')

@app.route('/list')
def list_questions():
    fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    questions = data_handler.get_questions()
    sorted_questions = data_handler.sorting_data(questions, 'id', True)
    return render_template('list.html', fieldnames=fieldnames, sorted_questions=sorted_questions)


@app.route('/add-question', methods=["GET", "POST"])
def add_question():
    if request.method == 'POST':
        reqv = request.form.to_dict()
        answers = data_handler.get_answers()
        questions = data_handler.get_questions()

        if reqv["question_id"] == '':
            answer = data_handler.generate_question_dict(reqv)
            answers.append(answer)
            data_handler.add_entry(answer,True)

        elif reqv["question_id"] != '':
            question = data_handler.generate_answer_dict(reqv)
            questions.append(question)
            data_handler.add_entry(question)

        app.logger.info(answers)
    return render_template('add-question.html', question_id="")


@app.route("/test")
def test():
    return str(data_handler.get_answers())


@app.route('/question/<question_id>')
def question_display(question_id):
    question_database = data_handler.get_questions()
    answer_database = data_handler.get_answers()
    question = data_handler.get_question(question_id, question_database)
    related_answers = data_handler.get_question_related_answers(question_id, answer_database)
    return render_template('display_question.html', question=question, answers=related_answers)


if __name__ == '__main__':
    app.run(debug=True)
