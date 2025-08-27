
import tkinter as tk
from tkinter import messagebox

# --- Safe arithmetic evaluator using AST ---
import ast
import operator as op

# Supported operators
_ops = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
}

def safe_eval(expr: str):
    """
    Safely evaluate a math expression string using AST.
    Supports +, -, *, /, //, %, **, parentheses, unary +/- and decimals.
    """
    def _eval(node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        if isinstance(node, ast.Constant):  # py3.8+ numbers
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid constant")
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type not in _ops:
                raise ValueError("Unsupported operator")
            # guard division by zero
            if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                raise ZeroDivisionError("Division by zero")
            return _ops[op_type](left, right)
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type not in _ops:
                raise ValueError("Unsupported unary operator")
            return _ops[op_type](operand)
        if isinstance(node, ast.Expr):
            return _eval(node.value)
        if isinstance(node, ast.Paren):
            return _eval(node.value)
        raise ValueError("Invalid expression")

    # Cleanup: replace unicode multiplication/division signs and percent shorthand
    expr = expr.replace('×', '*').replace('÷', '/')
    # Convert percentage like "50%" to "(50/100)"
    def _percent_to_div100(s):
        out = []
        i = 0
        while i < len(s):
            if s[i] == '%':
                out.append('/100')
                i += 1
            else:
                out.append(s[i])
                i += 1
        return ''.join(out)
    expr = _percent_to_div100(expr)

    tree = ast.parse(expr, mode='eval')
    return _eval(tree.body)

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Calculator")
        self.geometry("360x480")
        self.resizable(False, False)
        self._create_widgets()
        self._bind_keys()

    def _create_widgets(self):
        self.display_var = tk.StringVar(value="")
        self.display = tk.Entry(self, textvariable=self.display_var, font=("Segoe UI", 24), bd=8, relief="groove", justify="right")
        self.display.pack(fill="x", padx=12, pady=12, ipady=8)

        btns = [
            ("C", self.clear), ("⌫", self.backspace), ("%", lambda: self.insert("%")), ("÷", lambda: self.insert("÷")),
            ("7", lambda: self.insert("7")), ("8", lambda: self.insert("8")), ("9", lambda: self.insert("9")), ("×", lambda: self.insert("×")),
            ("4", lambda: self.insert("4")), ("5", lambda: self.insert("5")), ("6", lambda: self.insert("6")), ("-", lambda: self.insert("-")),
            ("1", lambda: self.insert("1")), ("2", lambda: self.insert("2")), ("3", lambda: self.insert("3")), ("+", lambda: self.insert("+")),
            ("(", lambda: self.insert("(")), ("0", lambda: self.insert("0")), (")", lambda: self.insert(")")), ("=", self.calculate),
        ]

        grid = tk.Frame(self)
        grid.pack(expand=True, fill="both", padx=12, pady=(0,12))

        rows = 5
        cols = 4
        for r in range(rows):
            grid.rowconfigure(r, weight=1)
        for c in range(cols):
            grid.columnconfigure(c, weight=1)

        for i, (text, cmd) in enumerate(btns):
            r = i // cols
            c = i % cols
            b = tk.Button(grid, text=text, command=cmd, font=("Segoe UI", 16), bd=1, relief="raised", padx=12, pady=12)
            b.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)

        # decimal button spans under 0 if you prefer; here we'll accept '.' via keyboard
        # Add a dedicated '.' button for completeness
        dot_btn = tk.Button(grid, text=".", command=lambda: self.insert("."), font=("Segoe UI", 16), bd=1, relief="raised", padx=12, pady=12)
        dot_btn.grid(row=4, column=0, sticky="nsew", padx=6, pady=6)
        # Move "(" from row 4 col 0 to row 4 col 1 and "0" to col 2, ")" to col 3
        # But we already placed them; to keep layout simple, we'll keep above arrangement.

    def _bind_keys(self):
        for ch in "0123456789+-*/().%":
            self.bind(f"<Key-{ch}>", self._on_key)
        # Multiplication/division unicode
        self.bind("<KeyPress>", self._on_any_key)
        self.bind("<Return>", lambda e: self.calculate())
        self.bind("<KP_Enter>", lambda e: self.calculate())
        self.bind("<Escape>", lambda e: self.clear())
        self.bind("<BackSpace>", lambda e: self.backspace())

    def _on_any_key(self, event):
        # map x to multiplication when shift-8 not used
        if event.char == 'x' or event.char == 'X':
            self.insert("×")
        elif event.char == '/':
            self.insert("÷") if self.display_var.get() and self.display_var.get()[-1] != '÷' else self.insert("")
        # Allow regular slash too, but we handle both.

    def _on_key(self, event):
        self.insert(event.char)

    def insert(self, text: str):
        # prevent two operators in a row (basic validation)
        if text in "+-×÷*/%":
            current = self.display_var.get()
            if not current:
                if text in "+×÷*/%":
                    return  # don't start with an operator except unary minus
            if current and current[-1] in "+-×÷*/%.":
                # Replace last operator with the new one (except minus which could be unary)
                if text == "-" and current[-1] != "-":
                    pass
                else:
                    self.display_var.set(current[:-1] + text)
                    return
        self.display.insert("end", text)

    def clear(self):
        self.display_var.set("")

    def backspace(self):
        current = self.display_var.get()
        if current:
            self.display_var.set(current[:-1])

    def calculate(self):
        expr = self.display_var.get().strip()
        if not expr:
            return
        try:
            result = safe_eval(expr)
            # Format result to avoid trailing .0 for integers
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.display_var.set(str(result))
        except ZeroDivisionError:
            messagebox.showerror("Math Error", "Division by zero is not allowed.")
        except Exception:
            messagebox.showerror("Input Error", "Please enter a valid arithmetic expression.")

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
