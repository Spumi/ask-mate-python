import os
from datetime import datetime
from flask import request
import data_handler


QUESTION_DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_DATA_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def vote_question(_id, vote):
    query = """UPDATE question SET vote_number = question.vote_number +{vote}
    WHERE id = {id}
    """.format(vote=vote,id=_id)
    data_handler.execute_query(query)


def vote_answer(_id, vote):
    delta = 1 if vote == "up" else -1
    query = """UPDATE answer SET vote_number = vote_number +{vote}
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


def generate_question_dict(data):
    question_data = {}
    question_data.update(submission_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    question_data.update(view_number=str(0))
    question_data.update(vote_number=str(0))
    question_data.update(title=data["title"])
    question_data.update(message=data["message"])
    question_data.update(image=data["image"])
    return question_data


def generate_answer_dict(data):
    answer_data = {}
    answer_data.update(submission_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    answer_data.update(vote_number=str(0))
    answer_data.update(question_id=data["question_id"])
    answer_data.update(message=data["message"])
    answer_data.update(image=data["image"])
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


def get_related_question_id(id):
    query = """SELECT answer.question_id FROM  answer JOIN comment ON comment.answer_id = answer.id
               WHERE answer.id = {id}
            """.format(id=id)
    result = data_handler.execute_query(query)
    return result.pop()["question_id"]


def get_question_related_tags(question_id):
    question_related_tags = data_handler.execute_query("""SELECT tag.name FROM question_tag LEFT JOIN tag 
        ON question_tag.tag_id = tag.id WHERE question_tag.question_id = {id}""".format(id=question_id))
    return question_related_tags
