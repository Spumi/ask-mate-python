import copy
import os
from datetime import datetime
from flask import request
import data_handler


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


def gen_question_id():
    answers = get_questions()
    items = [x['id'] for x in answers]
    return int(max(items)) + 1


def gen_answer_id():
    # depricated - Marked for removal
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
    # questions = data_handler.get_questions()
    handle_upload(req)
    question = generate_question_dict(req)
    # questions.append(question)
    data_handler.add_entry(question)


def handle_edit_entry(req, is_answer=False):
    handle_upload(req)
    data_handler.update_record(req, is_answer)


def get_answer_related_question_ids(keywords, answer_database, attribute):
    """
    Search keywords in database using attribute as a key. If it founds a keyword
    in the attribute, then its related question id is stored.
    :param keywords: list
    :param answer_database: list of dictionaries
    :param attribute: string
    :return: list of item related question ids
    """
    answer_related_question_ids = []
    for answer in answer_database:
        if any(keyword in answer[attribute] for keyword in keywords):
            answer_related_question_ids.append(answer['question_id'])
    return answer_related_question_ids


def create_check_keywords_in_database_string(keywords, database, attribute):
    string = f'\'%{keywords[0]}%\''
    for keyword in keywords[1:]:
        string += f' OR {database}.{attribute} LIKE \'%{keyword}%\''
    return string


def search_keywords_in_attribute(keywords, id_s, database, attribute_1, attribute_2=None):
    """
    Search keywords in table using attribute_1 and/or attribute_2 as key(s).
    Search id in id_s in order to find and append other database related items.
    :param keywords: list
    :param id_s: list
    :param database: list of dictionaries
    :param attribute_1: string
    :param attribute_2: string
    :return: list of items containing keywords
    """
    items_containing_keywords = []
    for item in database:
        if any(keyword in item[attribute_1] for keyword in keywords) or \
                any(keyword in item[attribute_2] for keyword in keywords):
            items_containing_keywords.append(item)
        elif item['id'] in id_s:
            items_containing_keywords.append(item)
    return items_containing_keywords


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
    print(query)
    result = data_handler.execute_query(query)
    print(result)
    return result.pop()["question_id"]
