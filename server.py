
from flask import Flask, render_template, request, redirect, url_for

import data_handler

from datetime import datetime

app = Flask(__name__)

@app.route('/')
@app.route('/list', methods=['GET', 'POST'])
# @app.route('/?order_by=vote_number&order_direction=desc', methods=['GET', 'POST'])
def list_questions():
    fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    questions = data_handler.get_questions()
    sorted_questions = data_handler.sorting_data(questions, 'submission_time', True)
    if request.method == 'POST':
        order_by = request.form.get('order_by')
        order_direction = False if request.form.get('order_direction') == 'asc' else True
        # app.logger.info(order_by)
        # app.logger.info(order_direction)
        sorted_questions = data_handler.sorting_data(questions, order_by, order_direction)
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
