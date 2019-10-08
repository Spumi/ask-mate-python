import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
import data_handler
import util
from data_handler import register

app = Flask(__name__)
app.debug = True
app.secret_key = os.environ.get("SECRET_KEY")

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
    order_direction = False if request.args.get('order_direction') == 'asc' else True
    order_by = 'submission_time' if request.args.get('order_by') == None else request.args.get('order_by')
    order_direction = 'ASC' if order_direction == False else 'DESC'
    if str(request.url_rule) == '/':
        is_main = True
        questions = data_handler.order_questions('submission_time', 'DESC', True)
    else:
        is_main = False
        questions = data_handler.order_questions(order_by, order_direction, False)
    return render_template('list.html',
                           sorted_questions=questions,
                           order_by=order_by,
                           order_direction=order_direction,
                           is_main=is_main)


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
    question_related_tags = data_handler.get_question_related_tags(question_id)

    return render_template('display_question.html',
                           question=question.pop(),
                           question_comments=question_comments,
                           answers=related_answers,
                           get_comments=data_handler.get_comments,
                           question_related_tags=question_related_tags)


@app.route("/question/<question_id>/vote-up")
def vote_up_question(question_id):
    data_handler.vote_question(question_id, 1)

    return redirect("/question/" + question_id)


@app.route("/question/<question_id>/vote-down")
def vote_down_question(question_id):
    data_handler.vote_question(question_id, -1)

    return redirect("/question/" + question_id)


@app.route("/vote-answer", methods=["POST"])
def vote_answer():
    if request.method == 'POST':
        req = request.form.to_dict()
        data_handler.vote_answer(req["id"], req["vote"])
        question_id = req['question_id']
        return redirect("/question/" + question_id)


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == 'POST':
        if request.form.get('delete') == 'Yes':
            data_handler.delete_question(question_id)
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
    questions_containing_keywords_query = data_handler.create_questions_containing_keywords_query(keywords)
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
    ref_question_id = request.args.get("qid")
    if "answer" in str(request.url_rule):
        comment_type = "answer"
    if request.method == 'POST':
        req = request.form.to_dict()
        ref_question_id = req["qid"]
        del req["qid"]
        data_handler.handle_add_comment(req)
        return redirect("/question/" + str(ref_question_id))
    return render_template("add-comment.html", qid=id, type=comment_type, question_id=ref_question_id)


@app.route("/question/<id>/new-tag", methods=["GET", "POST"])
def tag_question(id):
    existing_tags = data_handler.get_existing_tags()
    if request.method == 'POST':
        if request.form.get('selected_tag_name'):
            data_handler.tag_question_when_user_choose_from_existing_tags(id)
        elif request.form.get('add_new_tag'):
            data_handler.tag_question_when_user_enter_new_tag(id)

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
    data_handler.delete_comment(comment_id)
    return redirect("/question/" + str(question_id))


@app.route("/registration", methods=["GET", "POST"])
def user_registration():
    if request.method == "POST":
        credentials = request.form.to_dict()
        if not register(credentials['username'], credentials['password']):
            return 'Fail'
        else:
            return redirect('/')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username","")
        pwd = request.form.get("password","")
        if username != "" and pwd != "":
            auth_query = """SELECT id FROM users
            WHERE users.name = '%s' AND users.password = '%s';
            """ % (username, util.verify_password(pwd, util.hash_password(pwd)))
            result = data_handler.execute_query(auth_query)
            # session["username"] = username
            print(util.hash_password(pwd))
            print(result)
            # return result[0]["id"]
    return render_template("dev/login.html")


if __name__ == '__main__':
    app.run(debug=True)

