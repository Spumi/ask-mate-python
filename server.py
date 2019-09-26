import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import ast

import data_handler
import util

app = Flask(__name__)
app.debug = True


@app.route('/')
@app.route('/list')
@app.route('/?order_by=<order_by>&order_direction=<order_direction>', methods=['GET', 'POST'])
def list_questions():
    '''
    Assign values to the parameters of the sorted_questions function. It happens by getting them from the user.
    Sort the questions according to sorted questions's parameters.
    Convert order_direction from boolean to string. It is needed for user interface (html).
    :param questions:list of dictionaries
    :return:
    '''
    if str(request.url_rule) == '/':
        q = """SELECT * FROM question ORDER BY submission_time DESC
               LIMIT 5           
            """
        questions = data_handler.execute_query(q)
        return render_template('list.html',
                               sorted_questions=questions,
                               order_by='submission_time',
                               order_direction="DESC",
                               is_main=True)

    else:
        order_direction = False if request.args.get('order_direction') == 'asc' else True
        order_by = 'submission_time' if request.args.get('order_by') == None else request.args.get('order_by')
        order_direction = 'ASC' if order_direction == False else 'DESC'

        q = """SELECT * FROM question ORDER BY {order_by} {order_direction}   
        """.format(order_by=order_by, order_direction=order_direction)
        questions = data_handler.execute_query(q)
        return render_template('list.html',
                               sorted_questions=questions,
                               order_by=order_by,
                               order_direction=order_direction,
                               is_main=False)


@app.route('/add-question', methods=["GET", "POST"])
def add_question():
    if request.method == 'POST':
        req = request.form.to_dict()
        util.handle_add_question(req)
        return redirect(url_for("list_questions"))

    return render_template("edit-question.html", qid="")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer(question_id):
    if request.method == 'POST':
        req = request.form.to_dict()
        util.handle_add_answer(req)
        return redirect("/question/" + question_id)

    return render_template("add-answer.html", qid=question_id)


@app.route('/question/<question_id>')
def question_display(question_id):
    question = data_handler.get_question(question_id)
    related_answers = data_handler.get_question_related_answers(question_id)
    question_comments = data_handler.get_comments("question", question_id)
    question_related_tags = util.get_question_related_tags(question_id)

    return render_template('display_question.html',
                           question=question.pop(),
                           question_comments=question_comments,
                           answers=related_answers,
                           get_comments=data_handler.get_comments,
                           question_related_tags=question_related_tags)


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

            q = """DELETE FROM comment WHERE question_id = {question_id} OR answer_id = (SELECT id FROM answer WHERE id = {question_id}) 
            """.format(question_id=question_id)
            data_handler.execute_query(q)
            q = """DELETE FROM answer WHERE question_id = {question_id}
            """.format(question_id=question_id)
            data_handler.execute_query(q)
            q = """DELETE FROM question_tag WHERE question_id = {question_id}
            """.format(question_id=question_id)
            data_handler.execute_query(q)
            q = """DELETE FROM question WHERE id = {question_id}
            """.format(question_id=question_id)
            data_handler.execute_query(q)

            # handle_delete_question(question_id)
            return redirect(url_for('list_questions'))

        else:
            return redirect(url_for('question_display', question_id=question_id))

    return render_template('asking_if_delete_entry.html', question_id=question_id)


@app.route('/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):

    if request.method == 'POST':
        edited_question_data = request.form.to_dict()
        edited_question_data['id'] = int(edited_question_data['id'])
        edited_question_data['submission_time'] = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        util.handle_edit_entry(edited_question_data)

        return redirect("/question/" + str(question_id))

    question = data_handler.get_question(question_id)[0]

    return render_template('edit-question.html', question=question)


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id):
    if request.method == 'POST':
        delete = False
        if request.form.get('delete') == 'Yes':
            delete = True
        question_id = data_handler.delete_record(answer_id, True, delete=delete)
        return redirect('/question/' + str(question_id))
    else:
        return render_template('asking_if_delete_answer.html', answer_id=answer_id)


@app.route('/search-for-questions', methods=['GET', 'POST'])
def search_for_questions():
    keywords = str(request.args.get('keywords')).replace(',', '').split(' ')
    questions_containing_keywords_query = """SELECT DISTINCT question.* FROM question
                                             LEFT JOIN answer ON question.id = answer.question_id
                                             WHERE (question.title ILIKE {string_1})
                                             OR (question.message ILIKE {string_2}) 
                                             OR (answer.message ILIKE {string_3})
    """.format(string_1=util.create_check_keywords_in_database_string(keywords, 'question', 'title'),
               string_2=util.create_check_keywords_in_database_string(keywords, 'question', 'message'),
               string_3=util.create_check_keywords_in_database_string(keywords, 'answer', 'message'))
    questions_containing_keywords = data_handler.execute_query(questions_containing_keywords_query)

    return render_template('search_for_keywords_in_questions.html',
                           keywords=keywords, fieldnames=util.QUESTION_DATA_HEADER, questions=questions_containing_keywords)


@app.route("/upload", methods=["POST"])
def upload_image():
    image = request.files["image"]
    image.save(os.path.join(os.getcwd() + "/images/", image.filename))

    return redirect("/")


@app.route("/question/<id>/new-comment", methods=["GET", "POST"])
@app.route("/answer/<id>/new-comment", methods=["GET", "POST"])
def comment_question(id):
    comment_type = "question"
    question_id = id
    if "answer" in str(request.url_rule):
        comment_type = "answer"
        question_id = util.get_related_question_id(id)
        print(question_id)
    if request.method == 'POST':
        req = request.form.to_dict()
        data_handler.handle_add_comment(req)
        # return redirect(url_for("question_display", question_id=question_id))
        return redirect("/question/" + str(question_id))
    return render_template("add-comment.html", qid=id, type=comment_type)


@app.route("/question/<id>/new-tag", methods=["GET", "POST"])
def tag_question(id):
    existing_tags = data_handler.execute_query("""SELECT id, name FROM tag""")
    if request.method == 'POST':
        # If the user chooses a tag from the existing tags
        if request.form.get('selected_tag'):
            selected_tag = ast.literal_eval(request.form.to_dict('selected_tag')['selected_tag']) # data of selected tag
            selected_tag_id = selected_tag['id']

            print(type(request.form.to_dict('selected_tag')))
            form = 'select existing tag'
            # Check in question_tag database whether there is a tag to the current question and get the ids...
            get_quest_tag_id_combination = data_handler.execute_query("""SELECT question_id, tag_id FROM question_tag 
                WHERE question_id = {q_id} AND tag_id = {t_id}""".format(q_id=id, t_id=selected_tag_id))

            # ... if there is not then add new tag id and related question id to question_tag database
            if get_quest_tag_id_combination == []:
                data_handler.execute_query("""INSERT INTO question_tag (question_id, tag_id) 
                VALUES({q_id}, {t_id})""".format(q_id=id, t_id=selected_tag_id))

        # When the user enter a tag
        elif request.form.get('add_new_tag'):
            new_tag_id = data_handler.execute_query("""SELECT MAX(id) FROM tag""")[0]['max'] + 1
            new_tag_name = '\'' + request.form.get('add_new_tag') + '\'' # ' is needed for the SQL query

            ### almost same as above
            get_quest_tag_id_combination = data_handler.execute_query("""SELECT question_id, tag_id FROM question_tag
                WHERE question_id = {q_id} AND tag_id = (SELECT id FROM tag 
                                                        WHERE name = {t_name})""".format(q_id=id, t_name=new_tag_name))
            if get_quest_tag_id_combination == []:
                data_handler.execute_query("""INSERT INTO tag (id, name) VALUES({new_tag_id}, {new_tag_name})"""
                                           .format(new_tag_id=new_tag_id, new_tag_name=new_tag_name))

                data_handler.execute_query("""INSERT INTO question_tag (question_id, tag_id) 
                VALUES({q_id}, {t_id})""".format(q_id=id, t_id=new_tag_id))

## REFACTOR
# def get_quest_tag_id_combination(form, selected_tag_id):
#     if form == 'select existing tag':
#         selected_tag_id =
#
#     else:
#     quest_tag_id_combination = data_handler.execute_query("""SELECT question_id, tag_id FROM question_tag
#         WHERE question_id = {q_id} AND tag_id =
#     if get_quest_tag_id_combination == []:
#         data_handler.execute_query("""INSERT INTO tag (id, name) VALUES({new_tag_id}, {new_tag_name})"""
#                                    .format(new_tag_id=new_tag_id, new_tag_name=new_tag_name))
#
#     return quest_tag_id_combination


        return redirect("/question/" + id)

    return render_template("tag-question.html", qid=id, existing_tags=existing_tags)


@app.route('/answer/<answer_id>/edit', methods=["GET", "POST"])
def edit_answer(answer_id):

    if request.method == 'POST':
        edited_answer_data = request.form.to_dict()
        edited_answer_data['id'] = int(edited_answer_data['id'])
        edited_answer_data['submission_time'] = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        util.handle_edit_entry(edited_answer_data, is_answer=True)
        question_id = edited_answer_data['question_id']

        return redirect("/question/" + str(question_id))

    answer = data_handler.get_answer(answer_id)[0]
    question_id = answer['question_id']

    return render_template('add-answer.html', qid=question_id, answer=answer, answer_id=answer_id)


@app.route("/comments/<id>/edit", methods=["GET", "POST"])
def edit_comment(id):
    comment_type = "question"
    ref_question_id = request.args.get('qid')
    message =request.args.get("message")
    if "answer" in str(request.url_rule):
        comment_type = "answer"
#        question_id = util.get_related_question_id(id)
    if request.method == 'POST':
        req = request.form.to_dict()
        question_id = req["qid"]
        del req["qid"]
        data_handler.handle_edit_comment(id,req)
        return redirect("/question/" + str(question_id))

    return render_template("add-comment.html", qid=id, type=comment_type, message=message, question_id = ref_question_id)


@app.route("/comments/<comment_id>/delete", methods=["GET"])
def delete_comment(comment_id):
    question_id = request.args.get("qid")
    query = """DELETE FROM comment WHERE id = {comment_id}
    """.format(comment_id=comment_id)
    data_handler.execute_query(query)
    return redirect("/question/" + str(question_id))


if __name__ == '__main__':
    app.run(debug=True)

