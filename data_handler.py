import csv
import os
import time

# ANSWER_DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'data/answer.csv'
import connection

ANSWER_DATA_FILE_PATH = os.getcwd() + "/../data/answer.csv"
QUESTION_DATA_FILE_PATH = os.getcwd() + "/../data/question.csv"


def get_answer():
    database = connection.csv_to_dict(QUESTION_DATA_FILE_PATH)
    return database


def get_answer():
    database = connection.csv_to_dict(QUESTION_DATA_FILE_PATH)
    return database


def generate_id(stories):
    ordered_stories = sorted(stories, key=lambda x: ANSWER_DATA_HEADER[0])
    return str(int(ordered_stories[-1][ANSWER_DATA_HEADER[0]]) + 1)


def gen_id():
    return 0


def generate_question_dict(data):
    question_data = {}

    question_data.update(id=gen_id())
    question_data.update(submission_time=str(time.time()))
    question_data.update(view_number=0)
    question_data.update(vote_number=0)
    question_data.update(title=data["title"])
    question_data.update(message=data["message"])
    question_data.update(image=data["image"])
    return question_data


def generate_answer_dict(data):
    answer_data = {}

    answer_data.update(id=gen_id())
    answer_data.update(submission_time=str(time.time()))
    answer_data.update(vote_number=0)
    answer_data.update(question_id=data["question_id"])
    answer_data.update(message=data["message"])
    answer_data.update(image=data["image"])
    return answer_data
