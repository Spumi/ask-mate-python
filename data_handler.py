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

    # entry = escape_single_quotes(entry)
    query = """INSERT INTO {table}
    ({columns}) VALUES ({values});
    """.format(columns=string_builder(entry.keys()),
               values=string_builder(entry.values(), False),
               table=table)
    execute_query(query)


def get_question(question_id):
    question_query = f"""SELECT * FROM question
                         WHERE id={int(question_id)};"""
    question_data = execute_query(question_query)
    return question_data


def get_answer(answer_id, answer_database):
    for answer_data in answer_database:
        if answer_data['id'] == answer_id:
            return answer_data


def get_question_related_answers(question_id):
    answers_query = f"""SELECT * FROM answer
                        WHERE question_id={int(question_id)}
                        ORDER BY submission_time DESC;"""
    answers_of_question = execute_query(answers_query)
    return answers_of_question


def update_record(record, is_answer=False):
    table = "answer"
    record = escape_single_quotes(record)
    id_ = record['id']
    if not is_answer:
        table = "question"
        query = f"""UPDATE {table}
                    SET submission_time={"'" + record['submission_time'] + "'"},
                        title={"'" + record['title'] + "'"},
                        message={"'" + record['message'] + "'"},
                        image={"'" + record['image'] + "'"}
                    WHERE id={id_};
                    """
    else:
        query = f"""UPDATE {table}
            SET submission_time={"'" + record['submission_time'] + "'"},
                message={"'" + record['title'] + "'"},
                image={"'" + record['image'] + "'"}
            WHERE id={id_};
            """

    execute_query(query)


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


def escape_single_quotes(dictionary):
    for key, value in dictionary.items():
        if type(value) == str and "'" in value:
            dictionary[key] = value.replace("'", "''")
    return dictionary


def get_comments(comment_tpe, _id):
    comment_tpe += "_id"
    query = """SELECT message, submission_time, edited_count, comment.id  FROM comment
    WHERE {col} = {id} 
    """.format(col=comment_tpe, id=_id)
    #qid aid
    return execute_query(query)