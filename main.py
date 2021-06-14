import tkinter as tk

from question_manager import QuestionManager

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
FONT_SIZE = 14
SIDE_OF_CARD_SHOWING = 'front'

language = 'French'
word = f"{language.upper()}_WORD"
table = "french_words"
test = True

qm = QuestionManager(table='french_words')

# -------------------- FUNCTIONS -------------------- #


def checked_button(correct):
    qm.record_answer(correct=correct, test=test)
    qm.choose_question()
    canvas.itemconfig(tagOrId=question_text, text=qm.question[word].iloc[0])


# -------------------- UI SETUP -------------------- #
window = tk.Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = tk.Canvas(window, width=800, height=526)

# card front and back
card_front = tk.PhotoImage(file="images/card_front.png")
canvas.create_image(411, 270, image=card_front)

language_text = canvas.create_text(411, 150, text=language, fill="black", font=("Arial", 40, "italic"))
question_text = canvas.create_text(411, 263, text=qm.question[word].iloc[0], fill="black", font=("Arial", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=3)

# card_back = tk.PhotoImage(file="images/card_back.png")
# canvas.create_image(0, 0, image=card_back)
# canvas.grid(row=0, column=0, columnspan=3)

# buttons
wrong_image = tk.PhotoImage(file="images/wrong.png")
wrong_button = tk.Button(image=wrong_image, highlightthickness=0, bd=0, command=lambda: checked_button(False))
wrong_button.grid(row=1, column=0)

show_image = tk.PhotoImage(file="images/eye_2.png")
new_show_image = show_image.zoom(2, 2)
new_show_image = new_show_image.subsample(3, 3)
show_answer_button = tk.Button(image=new_show_image, width=100, height=100, command=lambda: print('Do you see? DO YOU SEE?!'))
show_answer_button.config(bd=0, highlightthickness=0)
show_answer_button.grid(row=1, column=1)

right_image = tk.PhotoImage(file="images/right.png")
right_button = tk.Button(image=right_image, highlightthickness=0, bd=0, command=lambda: checked_button(True))
right_button.grid(row=1, column=2)

#canvas.grid(row=0, column=1)


window.mainloop()