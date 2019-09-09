import csv
import os

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

