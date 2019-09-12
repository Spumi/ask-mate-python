import os
import time

from flask import Flask, render_template, request, redirect, url_for

import data_handler
import util
from util import handle_delete_question, handle_add_answer, handle_add_question

app = Flask(__name__)
app.debug = True

@app.route('/')
@app.route('/list')
@app.route('/?order_by=<order_by>&order_direction=<order_direction>', methods=['GET', 'POST'])
def list_questions():
    questions = data_handler.get_questions()

    order_by = 'submission_time' if request.args.get('order_by') == None else request.args.get('order_by')
    order_direction = False if request.args.get('order_direction') == 'asc' else True
    sorted_questions = util.sorting_data(questions, order_by, order_direction)
    order_direction = 'asc' if order_direction == False else 'desc'

    return render_template('list.html',
                           sorted_questions=sorted_questions,
                           order_by=order_by,
                           order_direction=order_direction,
                           convert_to_readable_date=util.convert_to_readable_date)


@app.route('/add-question', methods=["GET", "POST"])
def add_question():
    if request.method == 'POST':
        req = request.form.to_dict()
        handle_add_question(req)
        return redirect(url_for("list_questions"))

    return render_template("edit-question.html", qid="")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer(question_id):
    if request.method == 'POST':
        req = request.form.to_dict()
        handle_add_answer(req)
        return redirect("/question/" + question_id)

    return render_template("add-answer.html", qid=question_id)


@app.route('/question/<question_id>')
def question_display(question_id):
    question_database = data_handler.get_questions()
    answer_database = data_handler.get_answers()
    question = data_handler.get_question(question_id, question_database)

    related_answers = data_handler.get_question_related_answers(question_id, answer_database)
    return render_template('display_question.html', question=question, answers=util.sorting_data(related_answers, 'submission_time', True), convert_to_readable_date=util.convert_to_readable_date)

@app.route("/question/<question_id>/vote-up")
def vote_up_question(question_id):
    util.vote_question(question_id, 1)

    return redirect("/question/" + question_id)


@app.route("/question/<question_id>/vote-down")
def vote_down_question(question_id):
    util.vote_question(question_id, -1)

    return redirect("/question/" + question_id)


@app.route("/vote-answer", methods=["POST"])
def vote_answer():
    if request.method == 'POST':
        req = request.form.to_dict()
        util.vote_answer(req["id"], req["vote"])
        question_id = req['question_id']
        return redirect("/question/" + question_id)

@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == 'POST':
        if request.form.get('delete') == 'Yes':
            handle_delete_question(question_id)
            return redirect(url_for('list_questions'))

        else:
            return redirect(url_for('question_display', question_id=question_id))

    return render_template('asking_if_delete_entry.html', question_id=question_id)


@app.route('/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):

    if request.method == 'POST':
        edited_question_data = request.form.to_dict()
        edited_question_data['submission_time'] = str(int(time.time()))
        question = data_handler.update_questions(question_id, edited_question_data)
        related_answers = data_handler.get_question_related_answers(question_id, data_handler.get_answers())
        return render_template('display_question.html', question=question, answers=related_answers, convert_to_readable_date=util.convert_to_readable_date)

    all_questions = data_handler.get_questions()
    question = data_handler.get_question(question_id, all_questions)

    return render_template('edit-question.html', question=question)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    question_id = data_handler.delete_record(answer_id, True)
    return redirect('/question/' + question_id)


@app.route('/search-for-questions', methods=['GET', 'POST'])
def search_for_questions():
    fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    question_database = data_handler.get_questions()
    keywords = str(request.args.get('keywords')).replace(',', '').split(' ')
    questions_containing_keywords = []
    for question in question_database:
        if any(keyword in question['title'] for keyword in keywords) or any(keyword in question['message'] for keyword in keywords):
            questions_containing_keywords.append(question)

    return render_template('search_for_keywords_in_questions.html',
                           keywords=keywords, fieldnames=fieldnames, questions=questions_containing_keywords,
                           convert_to_readable_date=util.convert_to_readable_date)


@app.route("/upload", methods=["POST"])
def upload_image():
    image = request.files["image"]
    image.save(os.path.join(os.getcwd() + "/images/", image.filename))

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)

