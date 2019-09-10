import csv
import os
import time

# ANSWER_DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'data/answer.csv'
import connection

ANSWER_DATA_FILE_PATH = os.getcwd() + "/data/answer.csv"
QUESTION_DATA_FILE_PATH = os.getcwd() + "/data/question.csv"


def get_answers():
    database = connection.csv_to_dict(ANSWER_DATA_FILE_PATH)
    return database


def get_questions():
    database = connection.csv_to_dict(QUESTION_DATA_FILE_PATH)
    return database

def add_entry(entry, is_answer=False):
    connection.append_to_csv(QUESTION_DATA_FILE_PATH if is_answer else ANSWER_DATA_FILE_PATH, entry)


def generate_id(stories):
    ordered_stories = sorted(stories, key=lambda x: ANSWER_DATA_HEADER[0])
    return str(int(ordered_stories[-1][ANSWER_DATA_HEADER[0]]) + 1)


def gen_id():
    return 0


def generate_question_dict(data):
    question_data = {}

    question_data.update(id=str(gen_id()))
    question_data.update(submission_time=str(time.time()))
    question_data.update(view_number=str(0))
    question_data.update(vote_number=str(0))
    question_data.update(title=data["title"])
    question_data.update(message=data["message"])
    question_data.update(image=data["image"])
    return question_data


def generate_answer_dict(data):
    answer_data = {}

    answer_data.update(id=str(gen_id()))
    answer_data.update(submission_time=str(time.time()))
    answer_data.update(vote_number=str(0))
    answer_data.update(question_id=data["question_id"])
    answer_data.update(message=data["message"])
    answer_data.update(image=data["image"])
    return answer_data


def sorting_data(data, attribute, order_flag):
    '''
    :param data: list of dictionaries
    :param attribute: By which the data is sorted-
    :param order_flag: The order is ascending (False) or descending (True).
    :return: The sorted data.
    '''
    try:
        sorted_data = sorted(data, key=lambda x: int(x[attribute]) if x[attribute].isdigit() else x[attribute], reverse=order_flag)
    except AttributeError:
        sorted_data = sorted(data, key=lambda x: x[attribute], reverse=order_flag)
    return sorted_data

