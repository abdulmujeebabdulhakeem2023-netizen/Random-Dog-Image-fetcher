import math
from tkinter import *

# Window
root = Tk()
root.title("Scientific Calculator by Brainiac")
root.geometry("480x700")
root.configure(bg="black")
root.resizable(False, False)

# State
memory = 0
use_degrees = True  # Toggle between degrees and radians

# Display
display = Entry(
    root,
    font=("Helvetica", 30),
    bg="#1c1c1e",
    fg="white",
    bd=0,
    justify=RIGHT,
    insertbackground="white"
)
display.pack(fill=BOTH, ipadx=8, ipady=22, padx=10, pady=(15, 5))

# Secondary label (shows expression or mode)
info_var = StringVar(value="DEG")
info_label = Label(root, textvariable=info_var, font=("Helvetica", 11),
                   bg="black", fg="#888888", anchor=E)
info_label.pack(fill=X, padx=14)

# ── Helpers ────────────────────────────────────────────────
def get_display():
    return display.get()

def set_display(val):
    display.delete(0, END)
    display.insert(END, val)

def append(val):
    set_display(get_display() + str(val))

# ── Core actions ───────────────────────────────────────────
def clear():
    set_display("")

def backspace():
    set_display(get_display()[:-1])

def toggle_sign():
    val = get_display()
    if not val:
        return
    try:
        num = float(val)
        set_display(-num if num != 0 else val)
    except:
        pass

def percent():
    val = get_display()
    if not val:
        return
    try:
        set_display(float(val) / 100)
    except:
        set_display("Error")

def calculate():
    expr = get_display()
    if not expr:
        return
    # Replace display symbols with Python equivalents
    expr = expr.replace("×", "*").replace("÷", "/").replace("^", "**")
    try:
        result = eval(expr, {"__builtins__": {}}, safe_env())
        # Clean up float display
        if isinstance(result, float) and result == int(result):
            result = int(result)
        set_display(result)
    except:
        set_display("Error")

def safe_env():
    """Math namespace for eval."""
    return {
        "sin": lambda x: math.sin(math.radians(x) if use_degrees else x),
        "cos": lambda x: math.cos(math.radians(x) if use_degrees else x),
        "tan": lambda x: math.tan(math.radians(x) if use_degrees else x),
        "asin": lambda x: math.degrees(math.asin(x)) if use_degrees else math.asin(x),
        "acos": lambda x: math.degrees(math.acos(x)) if use_degrees else math.acos(x),
        "atan": lambda x: math.degrees(math.atan(x)) if use_degrees else math.atan(x),
        "log": math.log10,
        "ln": math.log,
        "sqrt": math.sqrt,
        "abs": abs,
        "floor": math.floor,
        "ceil": math.ceil,
        "factorial": math.factorial,
        "pi": math.pi,
        "e": math.e,
        "pow": math.pow,
    }

# ── Scientific actions ─────────────────────────────────────
def apply_func(func_name):
    val = get_display()
    if not val:
        append(func_name + "(")
        return
    try:
        num = float(val)
        env = safe_env()
        result = env[func_name](num)
        if isinstance(result, float) and result == int(result):
            result = int(result)
        set_display(round(result, 10))
    except:
        set_display("Error")

def square():
    val = get_display()
    if not val:
        return
    try:
        result = float(val) ** 2
        set_display(int(result) if result == int(result) else result)
    except:
        set_display("Error")

def reciprocal():
    val = get_display()
    if not val:
        return
    try:
        result = 1 / float(val)
        set_display(round(result, 10))
    except:
        set_display("Error")

def insert_constant(c):
    append(c)

def open_paren():
    append("(")

def close_paren():
    append(")")

def power():
    append("^")

# ── Degree / Radian toggle ─────────────────────────────────
def toggle_deg_rad():
    global use_degrees
    use_degrees = not use_degrees
    info_var.set("DEG" if use_degrees else "RAD")

# ── Memory ────────────────────────────────────────────────
def mem_clear():
    global memory
    memory = 0

def mem_recall():
    append(memory)

def mem_add():
    global memory
    try:
        memory += float(get_display())
    except:
        pass

def mem_sub():
    global memory
    try:
        memory -= float(get_display())
    except:
        pass

# ── Color palette ──────────────────────────────────────────
C_BG      = "black"
C_DARK    = "#1c1c1e"      # number keys
C_MID     = "#333333"      # function keys (C, +/-, %)
C_LIGHT   = "#636366"      # memory / top row
C_ORANGE  = "#FF9F0A"      # operators + =
C_BLUE    = "#0A84FF"      # scientific functions
C_TEXT    = "white"
C_DARK_TXT = "black"

# ── Button definitions ─────────────────────────────────────
# Each entry: (label, bg, fg, command)
def btn(label, bg, fg, cmd):
    return (label, bg, fg, cmd)

rows = [
    # Row 0 – Memory
    [
        btn("MC",  C_LIGHT, C_TEXT,  mem_clear),
        btn("MR",  C_LIGHT, C_TEXT,  mem_recall),
        btn("M+",  C_LIGHT, C_TEXT,  mem_add),
        btn("M−",  C_LIGHT, C_TEXT,  mem_sub),
        btn("DEG", C_BLUE,  C_TEXT,  toggle_deg_rad),
    ],
    # Row 1 – Scientific
    [
        btn("sin",  C_BLUE, C_TEXT, lambda: apply_func("sin")),
        btn("cos",  C_BLUE, C_TEXT, lambda: apply_func("cos")),
        btn("tan",  C_BLUE, C_TEXT, lambda: apply_func("tan")),
        btn("log",  C_BLUE, C_TEXT, lambda: apply_func("log")),
        btn("ln",   C_BLUE, C_TEXT, lambda: apply_func("ln")),
    ],
    # Row 2 – Scientific
    [
        btn("√",   C_BLUE,  C_TEXT,  lambda: apply_func("sqrt")),
        btn("x²",  C_BLUE,  C_TEXT,  square),
        btn("xʸ",  C_BLUE,  C_TEXT,  power),
        btn("1/x", C_BLUE,  C_TEXT,  reciprocal),
        btn("|x|", C_BLUE,  C_TEXT,  lambda: apply_func("abs")),
    ],
    # Row 3 – Scientific + operators
    [
        btn("π",   C_MID,   C_TEXT,  lambda: insert_constant("pi")),
        btn("e",   C_MID,   C_TEXT,  lambda: insert_constant("e")),
        btn("(",   C_MID,   C_TEXT,  open_paren),
        btn(")",   C_MID,   C_TEXT,  close_paren),
        btn("÷",   C_ORANGE, C_TEXT, lambda: append("÷")),
    ],
    # Row 4
    [
        btn("C",   C_MID,   C_TEXT,  clear),
        btn("+/-", C_MID,   C_TEXT,  toggle_sign),
        btn("%",   C_MID,   C_TEXT,  percent),
        btn("⌫",   C_MID,   C_TEXT,  backspace),
        btn("×",   C_ORANGE, C_TEXT, lambda: append("×")),
    ],
    # Row 5
    [
        btn("7",   C_DARK,  C_TEXT, lambda: append("7")),
        btn("8",   C_DARK,  C_TEXT, lambda: append("8")),
        btn("9",   C_DARK,  C_TEXT, lambda: append("9")),
        btn("-",   C_ORANGE, C_TEXT, lambda: append("-")),
    ],
    # Row 6
    [
        btn("4",   C_DARK,  C_TEXT, lambda: append("4")),
        btn("5",   C_DARK,  C_TEXT, lambda: append("5")),
        btn("6",   C_DARK,  C_TEXT, lambda: append("6")),
        btn("+",   C_ORANGE, C_TEXT, lambda: append("+")),
    ],
    # Row 7
    [
        btn("1",   C_DARK,  C_TEXT, lambda: append("1")),
        btn("2",   C_DARK,  C_TEXT, lambda: append("2")),
        btn("3",   C_DARK,  C_TEXT, lambda: append("3")),
        btn("=",   C_ORANGE, C_TEXT, calculate),
    ],
    # Row 8 – wide zero
    [
        btn("0",   C_DARK,  C_TEXT, lambda: append("0")),
        btn(".",   C_DARK,  C_TEXT, lambda: append(".")),
    ],
]

# ── Render buttons ─────────────────────────────────────────
frame = Frame(root, bg=C_BG)
frame.pack(fill=BOTH, expand=True, padx=6, pady=6)

for r_idx, row in enumerate(rows):
    row_frame = Frame(frame, bg=C_BG)
    row_frame.pack(fill=BOTH, expand=True)

    # Last row: 0 is wide
    if r_idx == len(rows) - 1:
        lbl, bg, fg, cmd = row[0]
        b = Button(row_frame, text=lbl, font=("Helvetica", 18, "bold"),
                   bg=bg, fg=fg, bd=0, relief=FLAT,
                   activebackground=bg, activeforeground=fg,
                   command=cmd)
        b.pack(side=LEFT, expand=True, fill=BOTH, padx=3, pady=3)
        b.configure(width=12)

        lbl, bg, fg, cmd = row[1]
        b = Button(row_frame, text=lbl, font=("Helvetica", 18, "bold"),
                   bg=bg, fg=fg, bd=0, relief=FLAT,
                   activebackground=bg, activeforeground=fg,
                   command=cmd)
        b.pack(side=LEFT, expand=True, fill=BOTH, padx=3, pady=3)

        # = spans the right side (from row 7, column 4)
        # already rendered in row 7, so nothing extra here

    else:
        for (lbl, bg, fg, cmd) in row:
            b = Button(row_frame, text=lbl, font=("Helvetica", 16, "bold"),
                       bg=bg, fg=fg, bd=0, relief=FLAT,
                       activebackground=bg, activeforeground=fg,
                       command=cmd)
            b.pack(side=LEFT, expand=True, fill=BOTH, padx=3, pady=3)

# Keep DEG label in sync with the toggle button text
def sync_deg_btn():
    # find and update the DEG/RAD button text dynamically via info_var
    pass  # info_var already updates the label; button label update below

# Patch toggle to also update button label
original_toggle = toggle_deg_rad
def toggle_deg_rad_patched():
    global use_degrees
    use_degrees = not use_degrees
    info_var.set("DEG" if use_degrees else "RAD")
    # Update the DEG/RAD button text
    for widget in root.winfo_children():
        _update_deg_btn(widget)

def _update_deg_btn(widget):
    if isinstance(widget, Frame):
        for child in widget.winfo_children():
            _update_deg_btn(child)
    elif isinstance(widget, Button) and widget["text"] in ("DEG", "RAD"):
        widget.config(text="DEG" if use_degrees else "RAD")

# Re-bind the DEG button with the patched version
def rebind():
    for widget in root.winfo_children():
        _rebind_deg(widget)

def _rebind_deg(widget):
    if isinstance(widget, Frame):
        for child in widget.winfo_children():
            _rebind_deg(child)
    elif isinstance(widget, Button) and widget["text"] in ("DEG", "RAD"):
        widget.config(command=toggle_deg_rad_patched)

root.after(100, rebind)

root.mainloop()