import copy
import os
import time
from datetime import datetime
from flask import request
import data_handler
from data_handler import get_questions, get_answers


QUESTION_DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_DATA_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def vote_question(_id, vote):
    # questions = data_handler.get_questions()
    # question = data_handler.get_question(_id, questions)
    # questions.remove(question)
    # question["vote_number"] = str(int(question["vote_number"]) + vote)
    # questions.append(question)
    # data_handler.save_questions(questions)
    # data_handler.save_questions(questions)
    query ="""UPDATE question SET vote_number = question.vote_number +{vote}
    WHERE id = {id}
    """.format(vote=vote,id=_id)
    data_handler.execute_query(query)


def vote_answer(_id, vote):
    delta = 1 if vote == "up" else -1
    # answers = data_handler.get_answers()
    # answer = data_handler.get_answer(_id, answers)
    # answers.remove(answer)
    # answer["vote_number"] = str(int(answer["vote_number"]) + delta)
    # answers.append(answer)
    # data_handler.save_answers(answers)
    query ="""UPDATE answer SET vote_number = vote_number +{vote}
    WHERE id = {id}
    """.format(vote=delta,id=_id)
    data_handler.execute_query(query)


def handle_upload(req):
    image = request.files["image"]
    if image.filename != "":
        req["image"] = "images/" + image.filename
        image.save(os.path.join(os.getcwd() + "/static/images/", image.filename))
    else:
        req["image"] = ""

def sorting_data(data, attribute, order_flag):
    '''
    Sorts data by attribute in order order_flag.
    :param data: list of dictionaries
    :param attribute: By which the data is sorted- This is the key of dictionaries.
    :param order_flag: Boolean. The order is ascending (False) or descending (True).
    :return: The sorted data. List of dictionaries.
    '''
    try:
        sorted_data = sorted(data, key=lambda x: int(x[attribute]) if x[attribute].isdigit() else x[attribute], reverse=order_flag)
    except AttributeError:
        sorted_data = sorted(data, key=lambda x: x[attribute], reverse=order_flag)
    return sorted_data


def convert_to_readable_date(timestamp):
    '''
    Converts unix timestamp into 2019-09-12 12:54:49 date-time format.
    :param timestamp: string
    :return: string
    '''
    readable_time = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    return readable_time


def gen_question_id():
    answers = get_questions()
    items = [x['id'] for x in answers]
    return int(max(items)) + 1


def gen_answer_id():
    answers = get_answers()
    if len(answers) == 0:
        return 0
    items = [x['id'] for x in answers]
    return int(max(items)) + 1


def generate_question_dict(data):
    question_data = {}

    # question_data.update(id="")
    question_data.update(submission_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    question_data.update(view_number=str(0))
    question_data.update(vote_number=str(0))
    question_data.update(title=data["title"])
    question_data.update(message=data["message"])
    question_data.update(image=data["image"])
    return question_data


def generate_answer_dict(data):
    answer_data = {}

    # answer_data.update(id=str(gen_answer_id()))
    # answer_data.update(submission_time=str(int(time.time())))
    answer_data.update(submission_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    answer_data.update(vote_number=str(0))
    answer_data.update(question_id=data["question_id"])
    answer_data.update(message=data["message"])
    answer_data.update(image=data["image"])
    return answer_data


def handle_delete_question(question_id):
    question_database = data_handler.get_questions()
    answer_database = data_handler.get_answers()
    copied_answer_database = copy.deepcopy(answer_database)
    for answer in copied_answer_database:
        if answer['question_id'] == question_id:
            answer_database.remove(answer)
    for question in question_database:
        if question['id'] == question_id:
            question_database.remove(question)
    data_handler.save_questions(question_database)
    data_handler.save_answers(answer_database)


def handle_add_answer(reqv):
    handle_upload(reqv)
    answer = generate_answer_dict(reqv)
    answers = data_handler.get_answers()
    answers.append(answer)
    data_handler.add_entry(answer, True)


def handle_add_question(req):
    questions = data_handler.get_questions()
    handle_upload(req)
    question = generate_question_dict(req)
    questions.append(question)
    data_handler.add_entry(question)
