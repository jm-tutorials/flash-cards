import pandas as pd
import sqlite3
from contextlib import closing


class QuestionManager:

    def __init__(self, table, limit=1000):
        self.db = 'data/flashcards.db'
        self.table = table
        self.limit = limit
        self.get_questions()
        self.answered_questions = None

    def connect(self):
        self.conn = sqlite3.connect(self.db)

    def close(self):
        self.conn.close()

    def get_questions(self):
        self.connect()
        query = f"select * from {self.table} limit {self.limit};"
        self.unanswered_questions = pd.read_sql_query(query, self.conn)
        self.close()
        self.choose_question()

    def choose_question(self):
        self.question = self.unanswered_questions.sample()
        print(self.question)
        return self.question.to_dict(orient="records")

    def execute_query(self, query):
        with closing(self.conn.cursor()) as cur:
            try:
                cur.execute(query)
            except Exception as e:
                print("Error:", e)
            else:
                self.conn.commit()
                print("Query executed successfully")

    def move_correct_answers(self):
        if self.answered_questions is not None:
            self.answered_questions = pd.concat([self.answered_questions, self.question])
        else:
            self.answered_questions = self.question

        self.unanswered_questions.drop(self.question.index, inplace=True)

    def record_answer(self, correct, test=False):

        if correct:
            self.move_correct_answers()

        if test:
            if correct:
                print("You're right, Dummy!")
            elif not correct:
                print("Wrong Dummy!")
            return

        query = "insert into table user_attempts (topic, question_id, correct)" \
                f"values{self.table, self.question.id, correct};"
        self.execute_query(query)
