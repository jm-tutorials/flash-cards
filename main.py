import tkinter as tk

from card_manager import CardManager

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
FONT_SIZE = 14
SIDE_OF_CARD_SHOWING = 'front'

global test
test = True

# -------------------- UI SETUP -------------------- #

window = tk.Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = tk.Canvas(window, width=800, height=526)

# create cards and timer
cm = CardManager(window, canvas)

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=3)

# buttons
wrong_image = tk.PhotoImage(file="images/wrong.png")
wrong_button = tk.Button(image=wrong_image, highlightthickness=0, bd=0, command=lambda: cm.record_and_continue(False))
wrong_button.grid(row=1, column=0)

show_image = tk.PhotoImage(file="images/eye_2.png")
new_show_image = show_image.zoom(2, 2)
new_show_image = new_show_image.subsample(3, 3)
show_answer_button = tk.Button(image=new_show_image, width=100, height=100, command=cm.show_answer)
show_answer_button.config(bd=0, highlightthickness=0)
show_answer_button.grid(row=1, column=1)

right_image = tk.PhotoImage(file="images/right.png")
right_button = tk.Button(image=right_image, highlightthickness=0, bd=0, command=lambda: cm.record_and_continue(True))
right_button.grid(row=1, column=2)

window.mainloop()