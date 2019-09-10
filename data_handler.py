import csv
import os
import time

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'data.csv'
DATA_HEADER = ['id', 'title', 'user_story', 'acceptance_criteria', 'business_value', 'estimation', 'status']
STATUSES = ['planning', 'todo', 'in progress', 'review', 'done']


def get_all_user_story():
    with open(DATA_FILE_PATH, 'r', newline='') as f:
        reader = csv.DictReader(f)
        database = [dict(row) for row in reader]
    return database


def write_all_user_story(stories):
    with open(DATA_FILE_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, DATA_HEADER)
        writer.writeheader()
        writer.writerows(stories)


def add_story(stories, inputs):
    stories.append(inputs)
    return stories


def update_story(stories, inputs):
    for i, story in enumerate(stories):
        if story[DATA_HEADER[0]] == inputs['id']:
            stories[i] = inputs
    return stories


def generate_id(stories):
    ordered_stories = sorted(stories, key=lambda x: DATA_HEADER[0])
    return str(int(ordered_stories[-1][DATA_HEADER[0]]) + 1)


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


def get_question(question_id, question_database):
    for question_data in question_database:
        if question_data['id'] == question_id:
            return question_data


def get_answers(question_id, answer_database):
    answers_of_question = []
    for answer_data in answer_database:
        if answer_data['question_id'] == question_id:
            answers_of_question.append(answer_data)
    return answers_of_question
