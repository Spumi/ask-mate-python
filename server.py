
from flask import Flask, render_template, request, redirect, url_for

import connection
import data_handler

from datetime import datetime
import time

app = Flask(__name__)


@app.route('/')
@app.route('/list')
@app.route('/?order_by=<order_by>&order_direction=<order_direction>', methods=['GET', 'POST'])
def list_questions():
    fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    questions = data_handler.get_questions()
    try:
        order_by = request.args.get('order_by')
        order_direction = False if request.args.get('order_direction') == 'asc' else True
        sorted_questions = data_handler.sorting_data(questions, order_by, order_direction)
        order_direction = 'asc' if order_direction == False else 'desc'
    except:
        order_by = 'submission_time'
        order_direction = 'desc'
        sorted_questions = data_handler.sorting_data(questions, 'submission_time', True)
    return render_template('list.html',
                           fieldnames=fieldnames,
                           sorted_questions=sorted_questions,
                           order_by=order_by,
                           order_direction=order_direction)



@app.route('/add-question', methods=["GET", "POST"])
def add_question():
    if request.method == 'POST':
        reqv = request.form.to_dict()
        questions = data_handler.get_questions()

        question = data_handler.generate_question_dict(reqv)
        questions.append(question)
        data_handler.add_entry(question)
        return redirect(url_for("list_questions"))

    return render_template("add-question.html", qid="")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer(question_id):
    if request.method == 'POST':
        reqv = request.form.to_dict()
        app.logger.info(request.form.to_dict())
        answer = data_handler.generate_answer_dict(reqv)
        answers = data_handler.get_answers()

        answers.append(answer)
        data_handler.add_entry(answer, True)
        return redirect("/question/" + question_id)

    return render_template("add-answer.html", qid=question_id)


@app.route('/question/<question_id>')
def question_display(question_id):
    question_database = data_handler.get_questions()
    answer_database = data_handler.get_answers()
    question = data_handler.get_question(question_id, question_database)
    related_answers = data_handler.get_question_related_answers(question_id, answer_database)
    return render_template('display_question.html', question=question, answers=related_answers)

@app.route("/question/<question_id>/vote-up")
def vote_up(question_id):
    questions = data_handler.get_questions()
    question = data_handler.get_question(question_id, questions)
    questions.remove(question)
    question["vote_number"] = str(int(question["vote_number"]) + 1)
    questions.append(question)
    data_handler.save_questions(questions)

    return redirect("/list")

@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    question_database = data_handler.get_questions()
    answer_database = data_handler.get_answers()
    for question in question_database:
        if question['id'] == question_id:
            question_database.remove(question)
    for answer in answer_database:
        if answer['question_id'] == question_id:
            answer_database.remove(answer)
    data_handler.modify_question_database(question_database, True)
    return redirect(url_for('list_questions'))

@app.route('/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):

    if request.method == 'POST':
        edited_question_data = request.form.to_dict()
        edited_question_data['submission_time'] = str(int(time.time()))
        question = data_handler.update_questions(question_id, edited_question_data)
        related_answers = data_handler.get_question_related_answers(question_id, data_handler.get_answers())
        return render_template('display_question.html', question=question, answers=related_answers)

    all_questions = data_handler.get_questions()
    question = data_handler.get_question(question_id, all_questions)

    return render_template('edit-question.html', question=question)


if __name__ == '__main__':
    app.run(debug=True)

