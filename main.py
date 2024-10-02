from tkinter import *
from tkinter import messagebox
import pandas
import random

# --------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
WHITE = "#ffffff"
BLACK = "#000000"
GREEN = "#B0DEC5"
DARK_GREEN = "#8FC3AF"
LANGUAGE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")

# -------------------- CREATING WORDS DATAFRAME ----------------------- #
words = pandas.read_csv("data/french_words.csv")

# --------------------- CREATING ALL-WORDS LIST ----------------------- #
allWords = []
for (index, row) in words.iterrows():
    allWords.append(index)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("FlashCards")
window.config(padx=20, pady=20, background=GREEN)

# Card
frontCard_img = PhotoImage(file="images/card_front.png")
backCard_img = PhotoImage(file="images/card_back.png")

Card_Canvas = Canvas(width=800, height=526, bg=GREEN, highlightthickness=0)
Card_img = PhotoImage(file="images/card_front.png")
canvas_image = Card_Canvas.create_image(400, 263, image=frontCard_img)
Card_Canvas.grid(column=0, row=0, columnspan=2, padx=(50, 50), pady=(50, 10))


# ----------------------- CARDS FUNCTIONS START ----------------------- #
def flip_to_back():
    word_label.config(text=words["English"][random_number], fg=WHITE, bg=DARK_GREEN)
    language_label.config(text="English", fg=WHITE, bg=DARK_GREEN)
    Card_Canvas.itemconfig(canvas_image, image=backCard_img)


def flip_to_front():
    global random_number

    try:
        random_number = random.choice(allWords)
        word_label.config(text=words["French"][random_number], fg=BLACK, bg=WHITE)
        language_label.config(text="French", fg=BLACK, bg=WHITE)
        Card_Canvas.itemconfig(canvas_image, image=frontCard_img)
        window.after(3000, flip_to_back)
    except KeyError:
        messagebox.showinfo(title="Attention", message=f"There are no more new words to learn")


def learned_word():
    global words
    words = words.drop([random_number], axis=0)
    allWords.remove(random_number)

    words_to_learn_dict = words.to_dict()
    words_to_learn_data_frame = pandas.DataFrame(words_to_learn_dict)
    f = open("words_to_learn.csv", "w+")
    f.close()
    words_to_learn_data_frame.to_csv("words_to_learn.csv", index=False)
    flip_to_front()

# ------------------------ CARDS FUNCTIONS END ------------------------ #

# Language label
language_label = Label(font=LANGUAGE_FONT)
language_label.grid(column=0, row=0, columnspan=2)
language_label.place(x=450, y=200, anchor=CENTER)

# Word label
word_label = Label(font=WORD_FONT)
word_label.grid(column=0, row=0, columnspan=2)
word_label.place(x=450, y=313, anchor=CENTER)

# Button - Wrong
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, bg=WHITE, highlightthickness=0, borderwidth=0, command=flip_to_front)
wrong_button.grid(column=0, row=1)

# Button - Right
right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, bg=WHITE, highlightthickness=0, borderwidth=0, command=learned_word)
right_button.grid(column=1, row=1)

# ---------------------------- START CODE ----------------------------- #
flip_to_front()

window.mainloop()
