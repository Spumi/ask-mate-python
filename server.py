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

    q = """SELECT * FROM question ORDER BY {order_by} {order_direction}   
    """.format(order_by=order_by, order_direction=order_direction)
    questions = data_handler.execute_query(q)
    return render_template('list.html',
                           sorted_questions=questions,
                           order_by=order_by,
                           order_direction=order_direction)


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
    question_query = f"""SELECT * FROM question
                     WHERE id={question_id};"""

    answers_query = f"""SELECT * FROM answer
                    WHERE question_id={question_id};"""

    question = data_handler.execute_query(question_query)
    related_answers = data_handler.execute_query(answers_query)

    return render_template('display_question.html', question=question.pop(), answers=related_answers)

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
        edited_question_data['submission_time'] = str(int(time.time()))
        question = data_handler.update_questions(question_id, edited_question_data)
        related_answers = data_handler.get_question_related_answers(question_id, data_handler.get_answers())
        return render_template('display_question.html', question=question, answers=related_answers)

    all_questions = data_handler.get_questions()
    question = data_handler.get_question(question_id, all_questions)

    return render_template('edit-question.html', question=question)


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id):
    if request.method == 'POST':
        delete = False
        if request.form.get('delete') == 'Yes':
            delete = True
        question_id = data_handler.delete_record(answer_id, True, delete=delete)
        return redirect('/question/' + question_id)
    else:
        return render_template('asking_if_delete_answer.html', answer_id=answer_id)


@app.route('/search-for-questions', methods=['GET', 'POST'])
def search_for_questions():

    keywords = str(request.args.get('keywords')).replace(',', '').split(' ')

    def check_keywords_in_items(keywords):
        string = f'\'%{keywords[0]}%\''
        for keyword in keywords[1:]:
            string += f' OR message LIKE \'%{keyword}%\''
        return string


    # Get the question ids from the answer database where keywords were found
    answer_related_question_id_query = """SELECT question_id FROM answer WHERE message LIKE {string}
    """.format(string=check_keywords_in_items(keywords))


    def change_list_of_dict_to_tuple():
    # Changes list to tuple. Tuple is needed for SQL VALUE(,,,) format
        answer_related_question_ids = data_handler.execute_query(answer_related_question_id_query)
        answer_id_sql_format = []
        for question_id in answer_related_question_ids:
            answer_id_sql_format.append(question_id.get('question_id'))
        answer_related_question_id_sql_format = tuple(answer_id_sql_format)
        return answer_related_question_id_sql_format

    answer_related_question_id_sql_format = change_list_of_dict_to_tuple()

    def check_question_id_in_answer_ids(answer_related_question_id_sql_format):
        if answer_related_question_id_sql_format != ():
            string_2 = f' OR (question.id IN {answer_related_question_id_sql_format})'
        else:
            string_2 = ''
        return string_2

    print(check_question_id_in_answer_ids(answer_related_question_id_sql_format))


    print(answer_related_question_id_sql_format)

    questions_containing_keywords_query = """SELECT DISTINCT question.* FROM question
                                             JOIN answer ON question.id = answer.question_id
                                             WHERE (question.title LIKE {string_1})
                                             OR (question.message LIKE {string_1}) {string_2}
    """.format(string_1=check_keywords_in_items(keywords),
               string_2=check_question_id_in_answer_ids(answer_related_question_id_sql_format))
    print(questions_containing_keywords_query)
    questions_containing_keywords = data_handler.execute_query(questions_containing_keywords_query)


    # question_query = """SELECT * FROM question
    # """
    # question_database = data_handler.execute_query(question_query)
    # answer_query = """SELECT * FROM answer
    # """
    # answer_database = data_handler.execute_query(answer_query)
    # print(answer_database)
    # questions_containing_keywords = util.search_keywords_in_attribute(keywords,
    #                                                                   answer_related_question_id,
    #                                                                   question_database,
    #                                                                   'title',
    #                                                                   'message')
    # print(questions_containing_keywords)

    return render_template('search_for_keywords_in_questions.html',
                           keywords=keywords, fieldnames=util.QUESTION_DATA_HEADER, questions=questions_containing_keywords)


@app.route("/upload", methods=["POST"])
def upload_image():
    image = request.files["image"]
    image.save(os.path.join(os.getcwd() + "/images/", image.filename))

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)

