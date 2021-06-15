import tkinter as tk

from question_manager import QuestionManager

TEST = False # set to true if you dont want to write to database for testing purposes
DEFAULT_TIME_QUESTION = 5000
DEFAULT_TIME_ANSWER = 3000


class CardManager:

    def __init__(self, window_object, canvas_object, table='french_words'):
        self.window_object = window_object
        self.canvas_object = canvas_object
        self.i = 0
        self.display = {0: ['French', 'FRENCH_WORD'],
                        1: ['English', 'ENGLISH_WORD']}
        self.timeout = True
        self.saw_answer, self.correct, self.button_click, self.canceled = False, False, False, False
        self.qm = QuestionManager(table=table)
        self.create_card()
        self.set_timer()
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

    def set_timer(self):
        self.flip_timer = self.window_object.after(DEFAULT_TIME_QUESTION, func=self.out_of_time)

    def out_of_time(self):
        self.record()
        self.show_answer_and_continue()

    def no_timeout(self):
        self.timeout = False

    def reset_vars(self):
        self.cancel_timer() # canceling and reseting the timer eveytime as a hacky solution to it not working as expected
        self.timeout = True
        self.saw_answer, self.correct, self.button_click = False, False, False
        self.set_timer()

    def button_clicked(self):
        self.button_click = True

    def next_card(self):
        self.get_question()
        self.current_language()

        if self.i % 2 != 0:
            self.flip_card()

        self.change_text()
        self.reset_vars()

    def record(self):
        if not self.button_click:
            self.qm.record_answer(correct=self.correct,saw_answer=self.saw_answer, timeout=self.timeout, test=TEST)

    def cancel_timer(self):
        self.window_object.after_cancel(self.flip_timer)
        self.timeout = False
        self.canceled = True

    def show_answer_and_continue(self):
        self.flip_card()
        self.window_object.after(DEFAULT_TIME_ANSWER, self.next_card)

    def record_and_continue(self, correct):
        self.correct = correct
        self.button_click_record_cancel_timer()

        if not correct and self.language == 'French':
            self.show_answer_and_continue()
        else:
            self.next_card()

    def flip_card(self):
        self.iterate()
        self.get_word()
        self.change_text()
        self.canvas_object.itemconfig(self.card_image, image=self.card)

    def show_answer(self):
        self.saw_answer = True
        self.timeout = False
        self.button_click_record_cancel_timer()
        self.show_answer_and_continue()

    def button_click_record_cancel_timer(self):
        self.cancel_timer()
        self.no_timeout()
        self.record()
        self.button_clicked()

    def change_text(self):
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
