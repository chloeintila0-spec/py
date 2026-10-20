
import tkinter as tk
import random

# Window
root = tk.Tk()
root.title("Little Minesweeper ♡")
root.configure(bg="#FAF2F9")
root.resizable(False, False)

# Settings
ROWS = 10
COLS = 10
MINES = 12

# Pastel colors
BG = "#FAF2F9"
PINK = "#EAB6D2"
LAVENDER = "#E6D9F2"
HOVER = "#D8C5E8"
WHITE = "#FFFAFD"
TEXT = "#66516F"
RED = "#D95D82"

NUMBER_COLORS = [
    "", "#6485D8", "#4B9B78", "#DF657E",
    "#9369C5", "#B46F60", "#54A6AC",
    "#66516F", "#9990A5"
]

board = []
buttons = []
opened = set()
flags = set()
mines = set()
game_over = False
first_click = True


def neighbors(r, c):
    return [
        (nr, nc)
        for nr in range(r - 1, r + 2)
        for nc in range(c - 1, c + 2)
        if (nr, nc) != (r, c)
        and 0 <= nr < ROWS
        and 0 <= nc < COLS
    ]


def new_game():
    global board, buttons, opened, flags
    global mines, game_over, first_click

    opened = set()
    flags = set()
    mines = set()
    game_over = False
    first_click = True

    board = [[0] * COLS for _ in range(ROWS)]

    for r in range(ROWS):
        for c in range(COLS):
            buttons[r][c].config(
                text="",
                state="normal",
                bg=LAVENDER,
                fg=TEXT,
                relief="flat",
                font=("Arial", 14, "bold")
            )

    status.config(text="find the safe tiles ♡", fg=TEXT)
    update_counter()


def update_counter():
    remaining = MINES - len(flags)
    counter.config(text=f"💣  {remaining} mines left")


def place_mines(safe_r, safe_c):
    global mines

    available = [
        (r, c)
        for r in range(ROWS)
        for c in range(COLS)
        if (r, c) != (safe_r, safe_c)
    ]

    mines = set(random.sample(available, MINES))

    for r, c in mines:
        board[r][c] = -1

    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != -1:
                board[r][c] = sum(
                    (nr, nc) in mines
                    for nr, nc in neighbors(r, c)
                )


def reveal(r, c):
    global first_click, game_over

    if game_over or (r, c) in opened or (r, c) in flags:
        return

    # First click is always safe
    if first_click:
        place_mines(r, c)
        first_click = False

    if board[r][c] == -1:
        game_over = True
        status.config(text="oops! you found a mine! now ur mine❤︎", fg=RED)

        # Show all mines
        for mr, mc in mines:
            buttons[mr][mc].config(
                text="✹",
                bg="#F4B8C9",
                fg=RED
            )

        return

    # Reveal connected empty tiles
    stack = [(r, c)]

    while stack:
        cr, cc = stack.pop()

        if (cr, cc) in opened or (cr, cc) in flags:
            continue

        opened.add((cr, cc))
        value = board[cr][cc]

        if value == 0:
            buttons[cr][cc].config(
                text="",
                bg=WHITE,
                relief="flat",
                disabledforeground=TEXT,
                state="disabled"
            )
        else:
            buttons[cr][cc].config(
                text=str(value),
                bg=WHITE,
                fg=NUMBER_COLORS[value],
                disabledforeground=NUMBER_COLORS[value],
                state="disabled"
            )

        if value == 0:
            for nr, nc in neighbors(cr, cc):
                if (nr, nc) not in opened and (nr, nc) not in mines:
                    stack.append((nr, nc))

    # Check victory
    if len(opened) == ROWS * COLS - MINES:
        game_over = True
        status.config(text="you finally won! my heart... ♡", fg="#4B9B78")


def toggle_flag(r, c):
    if game_over or (r, c) in opened:
        return

    if (r, c) in flags:
        flags.remove((r, c))
        buttons[r][c].config(text="", bg=LAVENDER)
    else:
        if len(flags) >= MINES:
            status.config(text="no flags left ♡", fg=RED)
            return

        flags.add((r, c))
        buttons[r][c].config(
            text="⚑",
            bg=PINK,
            fg=RED
        )

    update_counter()


# Header
title = tk.Label(
    root,
    text="little minesweeper ♡",
    font=("Arial", 22, "bold"),
    bg=BG,
    fg=TEXT
)
title.pack(pady=(16, 4))

counter = tk.Label(
    root,
    text="",
    font=("Arial", 11),
    bg=BG,
    fg=TEXT
)
counter.pack(pady=3)

status = tk.Label(
    root,
    text="find the safe tiles ♡",
    font=("Arial", 11),
    bg=BG,
    fg=TEXT
)
status.pack(pady=5)

# Game board
frame = tk.Frame(root, bg=BG)
frame.pack(padx=12, pady=10)

for r in range(ROWS):
    row_buttons = []

    for c in range(COLS):
        btn = tk.Button(
            frame,
            text="",
            width=2,
            height=1,
            font=("Arial", 14, "bold"),
            bg=LAVENDER,
            fg=TEXT,
            activebackground=HOVER,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda r=r, c=c: reveal(r, c)
        )

        btn.grid(
            row=r,
            column=c,
            padx=2,
            pady=2,
            ipadx=3,
            ipady=3
        )

        btn.bind(
            "<Button-3>",
            lambda event, r=r, c=c: toggle_flag(r, c)
        )

        row_buttons.append(btn)

    buttons.append(row_buttons)

# Restart button
restart_button = tk.Button(
    root,
    text="  ↻  play again  ",
    font=("Arial", 11, "bold"),
    bg=PINK,
    fg=TEXT,
    activebackground=HOVER,
    relief="flat",
    cursor="hand2",
    command=new_game
)
restart_button.pack(pady=(4, 16))

new_game()

root.mainloop()
