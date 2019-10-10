from datetime import datetime

import psycopg2
from psycopg2 import sql

import connection
from util import string_builder, create_check_keywords_in_database_string, escape_single_quotes, hash_password
from flask import request, session


def add_entry(entry, is_answer=False):
    table = "answer"
    if not is_answer:
        table = "question"
    query = """INSERT INTO {table}
    ({columns}) VALUES ({values});
    """.format(columns=string_builder(entry.keys()),
               values=string_builder(entry.values(), False),
               table=table)
    execute_query(query)


def get_question(question_id):
    question_query = f"""SELECT question.*, users.name
                         FROM question
                         JOIN users ON question.user_id=users.id
                         WHERE question.id={int(question_id)};"""
    question_data = execute_query(question_query)
    return question_data


def get_answer(answer_id):
    answer_query = f"""SELECT * FROM answer
                       WHERE id={int(answer_id)}"""
    answer_data = execute_query(answer_query)
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
                message={"'" + record['message'] + "'"},
                image={"'" + record['image'] + "'"}
            WHERE id={id_};
            """

    execute_query(query)


def get_question_id(id):
    question_id_query = f"""SELECT question_id FROM answer
                            WHERE id={id};"""
    question_id = execute_query(question_id_query)[0]['question_id']
    return question_id


def delete_record(id, answer=False, delete=False):
    if answer:
        # question_id_query = f"""SELECT question_id FROM answer
        #                         WHERE id={id};"""
        delete_answer_query = f"""DELETE FROM answer
                                  WHERE id={id};"""
        delete_comment_query = f"""DELETE FROM comment
                                  WHERE answer_id={id};"""
        # question_id = execute_query(question_id_query)[0]['question_id']
        question_id = get_question_id(id)

        if delete:
            execute_query(delete_comment_query)
            execute_query(delete_answer_query)

        return question_id


@connection.connection_handler
def execute_query(cursor, query):
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
    query = """INSERT INTO comment ({columns}) 
    VALUES ({value_list})""".format(columns=string_builder(req.keys(), True),
                                    value_list=string_builder(req.values(), False)
                                    )
    execute_query(query)


def get_comments(comment_tpe, _id):
    comment_tpe += "_id"
    query = """SELECT message, submission_time, edited_count, comment.question_id, comment.answer_id, comment.id, u.name
    FROM comment
    JOIN users u on comment.user_id = u.id
    WHERE {col} = {id} ORDER BY submission_time DESC 
    """.format(col=comment_tpe, id=_id)
    return execute_query(query)


def handle_edit_comment(id, msg):
    query = """UPDATE comment 
    SET message = {msg},
     edited_count = COALESCE (edited_count, 0) +1 
    WHERE id = {id}
    """.format(id=id, msg=("'" + msg["message"].replace("'", "''")) + "'")
    execute_query(query)


def create_questions_containing_keywords_query(keywords):
    questions_containing_keywords_query = """SELECT DISTINCT question.* FROM question
                                             LEFT JOIN answer ON question.id = answer.question_id
                                             WHERE (question.title ILIKE {string_1})
                                             OR (question.message ILIKE {string_2}) 
                                             OR (answer.message ILIKE {string_3})
    """.format(string_1=create_check_keywords_in_database_string(keywords, 'question', 'title'),
               string_2=create_check_keywords_in_database_string(keywords, 'question', 'message'),
               string_3=create_check_keywords_in_database_string(keywords, 'answer', 'message'))
    return questions_containing_keywords_query


def delete_question(question_id):
    q = """DELETE FROM comment WHERE question_id = {question_id} OR answer_id IN (SELECT id FROM answer WHERE answer.question_id = {question_id}) 
    """.format(question_id=question_id)
    execute_query(q)
    q = """DELETE FROM answer WHERE question_id = {question_id}
    """.format(question_id=question_id)
    execute_query(q)
    q = """DELETE FROM question_tag WHERE question_id = {question_id}
    """.format(question_id=question_id)
    execute_query(q)
    q = """DELETE FROM question WHERE id = {question_id}
    """.format(question_id=question_id)
    execute_query(q)


def get_existing_tags():
    existing_tags = [name['name'] for name in
                     [tag for tag in execute_query("""SELECT id, name FROM tag""")]]
    return existing_tags


### REFACTOR IN PROGRESS ###
def tag_question_when_user_choose_from_existing_tags(id):
        selected_tag_name = '\'' + request.form.to_dict('selected_tag_name')['selected_tag_name'] + '\''
        selected_tag_id = execute_query("""SELECT id FROM tag 
        LEFT JOIN question_tag ON tag.id = question_tag.tag_id WHERE tag.name = {selected_tag}"""
                                                     .format(selected_tag=selected_tag_name))[0]['id']
        # Check in question_tag database whether there is a tag to the current question and get the ids...
        quest_tag_id_combination = execute_query("""SELECT question_id, tag_id FROM question_tag 
            WHERE question_id = {q_id} AND tag_id = {t_id}""".format(q_id=id, t_id=selected_tag_id))

        # ... if there is not then add new tag id and related question id to question_tag database
        if quest_tag_id_combination == []:
            execute_query("""INSERT INTO question_tag (question_id, tag_id) 
            VALUES({q_id}, {t_id})""".format(q_id=id, t_id=selected_tag_id))

### REFACTOR IN PROGRESS ###
def tag_question_when_user_enter_new_tag(id):
    new_tag_id = execute_query("""SELECT MAX(id) FROM tag""")[0]['max'] + 1
    new_tag_name = '\'' + request.form.get('add_new_tag') + '\''  # ' is needed for the SQL query

    quest_tag_id_combination = execute_query("""SELECT question_id, tag_id FROM question_tag
         WHERE question_id = {q_id} AND tag_id = (SELECT id FROM tag 
                                                 WHERE name = {t_name})""".format(q_id=id, t_name=new_tag_name))
    if quest_tag_id_combination == []:
        execute_query("""INSERT INTO tag (id, name) VALUES({new_tag_id}, {new_tag_name})"""
                                   .format(new_tag_id=new_tag_id, new_tag_name=new_tag_name))

        execute_query("""INSERT INTO question_tag (question_id, tag_id) 
         VALUES({q_id}, {t_id})""".format(q_id=id, t_id=new_tag_id))


def vote_question(_id, vote):
    query = """UPDATE question SET vote_number = question.vote_number +{vote}
    WHERE id = {id}
    """.format(vote=vote,id=_id)
    execute_query(query)


def vote_answer(_id, vote):
    delta = 1 if vote == "up" else -1
    query = """UPDATE answer SET vote_number = vote_number +{vote}
    WHERE id = {id}
    """.format(vote=delta,id=_id)
    execute_query(query)


def get_related_question_id(id):
    query = """SELECT answer.question_id FROM  answer JOIN comment ON comment.answer_id = answer.id
               WHERE answer.id = {id}
            """.format(id=id)
    result = execute_query(query)
    return result.pop()["question_id"]


def get_question_related_tags(question_id):
    question_related_tags = execute_query("""SELECT tag.name, tag_id, question_tag.question_id FROM question_tag LEFT JOIN tag 
             ON question_tag.tag_id = tag.id WHERE question_tag.question_id = {id}""".format(id=question_id))
    return question_related_tags


def delete_comment(comment_id):
    query = """DELETE FROM comment WHERE id = {comment_id}
    """.format(comment_id=comment_id)
    execute_query(query)


def order_questions(order_by, order_direction, is_main):
    limit = 'LIMIT 5' if is_main == True else ''
    q = """SELECT * FROM question ORDER BY {order_by} {order_direction} {limit}
    """.format(order_by=order_by, order_direction=order_direction, limit=limit)
    questions = execute_query(q)
    return questions


def register(username, password):
    sql_expression = """ INSERT INTO users (name, password)
                         VALUES ('%s', '%s')                   
                     """ % (username.lower(), hash_password(password))
    try:
        execute_query(sql_expression)
    except psycopg2.IntegrityError:
        return False
    else:
        return True


def get_user_by_entry_id(id, table='question'):
    sql_expression = """SELECT user_id
                        FROM %(table)s
                        WHERE id = %(id)s;""" % {'id': id, 'table': table}

    user_id = execute_query(sql_expression)[0]['user_id']
    return user_id


def get_all_entries_by_user_id(user_id):
    sql_questions = """SELECT users.id AS user_id,
                              users.name AS user_name, 
                              question.id AS question_id,
                              question.title,
                              question.message,
                              question.submission_time,
                              question.view_number,
                              question.vote_number
                       FROM users
                       JOIN question
                        ON users.id = question.user_id
                       WHERE users.id = %(user_id)s
                       ORDER BY question.submission_time DESC;
                    """ % {'user_id': user_id}

    sql_answers = """SELECT answer.user_id AS user_id,
                            (SELECT name FROM users WHERE id=%(user_id)s) AS user_name,
                            question.id AS question_id,
                            question.title AS question_title,
                            answer.message AS answer,
                            answer.submission_time,
                            answer.vote_number,
                            CASE WHEN answer.accepted IS TRUE THEN 'accepted' ELSE '' END AS status
                     FROM answer
                     JOIN question
                      ON answer.question_id = question.id
                     WHERE answer.user_id = %(user_id)s
                     ORDER BY answer.submission_time DESC;
                  """ % {'user_id': user_id}

    sql_comments = """SELECT comment.user_id AS user_id,
                             (SELECT name FROM users WHERE id=%(user_id)s) AS user_name,
                             question.id AS question_id,
                             question.title AS question_title,
                             comment.message AS comment,
                             comment.submission_time,
                             CASE WHEN comment.question_id IS NULL THEN 'answer' ELSE 'question' END AS comment_for
                      FROM comment
                      LEFT JOIN answer
                      ON comment.answer_id = answer.id
                      LEFT JOIN question
                      ON comment.question_id = question.id OR answer.question_id = question.id
                      WHERE comment.user_id = %(user_id)s
                      ORDER BY comment.submission_time DESC;
                  """ % {'user_id': user_id}

    user_entries = {'questions': execute_query(sql_questions),
                    'answers': execute_query(sql_answers),
                    'comments': execute_query(sql_comments)}

    return user_entries


def is_comment_owned_by_user(user_id, comment_id):
    uid = get_user_by_entry_id(comment_id, 'comment')
    return uid == user_id


def get_users():
    query = """SELECT * FROM users"""
    users = execute_query(query)
    return users


def get_answer_id(question_id):
    answer_id_query = f"""SELECT id FROM answer
                            WHERE question_id={question_id};"""
    answer_id = execute_query(answer_id_query)[0]['id']
    return answer_id


def get_accepted_attribute(question_id):
    query = """SELECT id, accepted FROM answer 
        WHERE question_id=%(question_id)s""" % {'question_id': question_id}
    accepted_attribute = execute_query(query)
    return accepted_attribute


def update_answer_accepted(answer_id_and_accepted_pairs, answer_id):
    query = """UPDATE answer SET accepted=%(accepted)s WHERE id=%(id)s""" % {
        'accepted': answer_id_and_accepted_pairs[answer_id], 'id': answer_id}
    execute_query(query)


def is_comment_owned_by_user(user_id, comment_id):
    uid = get_user_by_entry_id(comment_id, 'comment')
    return uid == user_id


def get_tags():
    q = """SELECT tag.name, COUNT(*) AS count FROM tag
    right join question_tag qt on tag.id = qt.tag_id
    GROUP BY tag.name
    """
    return execute_query(q)