import os
from datetime import datetime

import bcrypt as bcrypt
from flask import request, session
import data_handler


QUESTION_DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_DATA_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def handle_upload(req):
    image = request.files["image"]
    if image.filename != "":
        req["image"] = "images/" + image.filename
        image.save(os.path.join(os.getcwd() + "/static/images/", image.filename))
    else:
        req["image"] = ""


def generate_question_dict(data):
    question_data = {}
    question_data.update(submission_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    question_data.update(view_number=str(0))
    question_data.update(vote_number=str(0))
    question_data.update(title=data["title"])
    question_data.update(message=data["message"])
    question_data.update(image=data["image"])
    question_data.update(user_id=data["user_id"])
    return question_data


def generate_answer_dict(data):
    answer_data = {}
    answer_data.update(submission_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    answer_data.update(vote_number=str(0))
    answer_data.update(question_id=data["question_id"])
    answer_data.update(message=data["message"])
    answer_data.update(image=data["image"])
    answer_data.update(user_id=str(session["id"]))
    return answer_data


def handle_add_answer(reqv):
    handle_upload(reqv)
    answer = generate_answer_dict(reqv)
    data_handler.add_entry(answer, True)


def handle_add_question(req):
    handle_upload(req)
    question = generate_question_dict(req)
    data_handler.add_entry(question)


def handle_edit_entry(req, is_answer=False):
    handle_upload(req)
    data_handler.update_record(req, is_answer)


def create_check_keywords_in_database_string(keywords, database, attribute):
    string = f'\'%{keywords[0]}%\''
    for keyword in keywords[1:]:
        string += f' OR {database}.{attribute} LIKE \'%{keyword}%\''
    return string


def string_builder(lst, is_key=True):
    result = ""
    for element in lst:
        escaped_element = element.replace("'", "''")
        if is_key:
            result += "" + escaped_element + ", "
        else:
            result += "\'" + escaped_element + "\', "
    return result[:-2]


def escape_single_quotes(dictionary):
    for key, value in dictionary.items():
        if type(value) == str and "'" in value:
            dictionary[key] = value.replace("'", "''")
    return dictionary


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)
