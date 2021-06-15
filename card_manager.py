import tkinter as tk
import time

from question_manager import QuestionManager

test = False


class CardManager:

    def __init__(self, canvas_object, table='french_words'):
        self.canvas_object = canvas_object
        self.i = 0
        self.display = {0: ['French', 'FRENCH_WORD'],
                        1: ['English', 'ENGLISH_WORD']}
        self.qm = QuestionManager(table=table)
        self.create_card()
        self.next_card()

    def create_card(self):
        # card front and back
        self.card_front = tk.PhotoImage(file="images/card_front.png")
        self.card_back = tk.PhotoImage(file="images/card_back.png")

        self.display[0].append(self.card_front)
        self.display[1].append(self.card_back)

        self.current_language()
        self.card_image = self.canvas_object.create_image(411, 270, image=self.card)

        # text
        self.language_text = self.canvas_object.create_text(411, 150, text="", fill="black", font=("Arial", 40, "italic"))
        self.question_text = self.canvas_object.create_text(411, 263, text="", fill="black", font=("Arial", 60, "bold"))

    def next_card(self):
        self.get_question()
        self.current_language()

        if self.i % 2 != 0:
            self.flip_card()
        self.change_text()

    def record_and_continue(self, correct):
        self.qm.record_answer(correct=correct, test=test)

        if not correct and self.language == 'French':
            self.flip_card()
            # time.sleep(5)

        self.next_card()

    def flip_card(self):
        self.iterate()
        self.get_word()
        self.change_text()
        self.canvas_object.itemconfig(self.card_image, image=self.card)

    def change_text(self):
        # self.current_language()
        self.canvas_object.itemconfig(self.language_text, text=self.language)
        self.canvas_object.itemconfig(self.question_text, text=self.word)

    def iterate(self):
        self.i += 1

    def current_language(self):
        self.language, self.column, self.card = self.display[self.i % 2]

    def get_question(self):
        self.question = self.qm.choose_question()
        self.get_word()

    def get_word(self):
        self.current_language()
        self.word = self.question[0][self.column]
