import data_handler


def vote_question(_id, vote):
    questions = data_handler.get_questions()
    question = data_handler.get_question(_id, questions)
    questions.remove(question)
    question["vote_number"] = str(int(question["vote_number"]) + vote)
    questions.append(question)
    data_handler.save_questions(questions)


def vote_answer(_id, vote):
    delta = 1 if vote == "up" else -1
    answers = data_handler.get_answers()
    answer = data_handler.get_answer(_id, answers)
    answers.remove(answer)
    answer["vote_number"] = str(int(answer["vote_number"]) + delta)
    answers.append(answer)
    data_handler.save_answers(answers)
