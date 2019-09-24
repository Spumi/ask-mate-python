import os
from datetime import datetime

from psycopg2 import sql

import connection
from util import string_builder

ANSWER_DATA_FILE_PATH = os.getcwd() + "/data/answer.csv"
QUESTION_DATA_FILE_PATH = os.getcwd() + "/data/question.csv"


def get_answers():
    database = connection.csv_to_dict(ANSWER_DATA_FILE_PATH)
    return database


def get_questions():
    database = connection.csv_to_dict(QUESTION_DATA_FILE_PATH)
    return database


def save_questions(data):
    database = connection.dict_to_csv(QUESTION_DATA_FILE_PATH, data)
    return database


def save_answers(data):
    database = connection.dict_to_csv(ANSWER_DATA_FILE_PATH, data, True)
    return database


def add_entry(entry, is_answer=False):
    table = "answer"
    if not is_answer:
        table = "question"

    query = """INSERT INTO {table}
    ({columns}) VALUES ({values});
    """.format(columns=string_builder(entry.keys()),
               values=string_builder(entry.values(), False),
               table=table)
    print(query)
    execute_query(query)

def get_question(question_id, question_database):
    for question_data in question_database:
        if question_data['id'] == question_id:
            return question_data


def get_answer(answer_id, answer_database):
    for answer_data in answer_database:
        if answer_data['id'] == answer_id:
            return answer_data


def get_question_related_answers(question_id, answer_database):
    answers_of_question = []
    for answer_data in answer_database:
        if answer_data['question_id'] == question_id:
            answers_of_question.append(answer_data)
    return answers_of_question


def update_questions(question_id, updated_data):
    all_questions = get_questions()
    question = get_question(question_id, all_questions)
    question_index = all_questions.index(question)

    for key, value in updated_data.items():
        question[key] = value
    all_questions[question_index] = question
    save_questions(all_questions)
    return question


def delete_record(id, answer=False, delete=False):
    if answer:
        question_id_query = f"""SELECT question_id FROM answer
                                WHERE id={id};"""
        delete_answer_query = f"""DELETE FROM answer
                                  WHERE id={id};"""
        delete_comment_query = f"""DELETE FROM comment
                                  WHERE answer_id={id};"""
        question_id = execute_query(question_id_query)[0]['question_id']

        if delete:
            execute_query(delete_comment_query)
            execute_query(delete_answer_query)

        return question_id


@connection.connection_handler
def execute_query(cursor, query):
    # print(query.startswith("INSERT"))
    if query.startswith("SELECT"):
        cursor.execute(
            sql.SQL(query)
        )
        result = cursor.fetchall()

    else:
        result = cursor.execute(query)
    return result


def handle_add_comment(req):
    req.update(submission_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    query ="""INSERT INTO comment ({columns}) 
    VALUES ({value_list})""".format(columns=string_builder(req.keys(), True),
                                    value_list=string_builder(req.values(), False)
                                    )
    execute_query(query)
