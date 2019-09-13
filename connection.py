import csv

def csv_to_dict(file_path):
    with open(file_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        database = [dict(row) for row in reader]
    return database


def dict_to_csv(file_path, data, is_answers=False):
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, ANSWER_DATA_HEADER if is_answers else QUESTION_DATA_HEADER)
        writer.writeheader()
        writer.writerows(data)


def append_to_csv(file_path, data):
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([data.values()])
