
# Tkinter Calculator (Assignment: Module 10 & 11)

A clean, robust calculator built with Python's `tkinter`. It supports:

- Addition, subtraction, multiplication (×), division (÷)
- Parentheses `(` `)`
- Percent `%` (treated as `/100`)
- Decimal numbers
- Backspace `⌫` and Clear `C`
- Keyboard shortcuts: numbers and operators, `Enter` to evaluate, `Esc` to clear, `Backspace` to delete

## How to Run

1. Ensure you have **Python 3.8+** installed.
2. `tkinter` ships with most standard Python installations:
   - On Windows/macOS: usually preinstalled.
   - On Linux: you may need to install it via your package manager, e.g. Ubuntu/Debian: `sudo apt-get install python3-tk`.
3. Open a terminal in the project folder and run:

   ```bash
   python ./src/calculator.py
   ```

## Validations & Error Handling

- Prevents starting with an operator (except unary minus).
- Replaces repeated operators to avoid `++`, `**` by mistake (except unary minus).
- Blocks division/modulo/floor-division by zero with a friendly error dialog.
- Uses a **safe AST-based evaluator** instead of `eval`.

## Files

```text
CalculatorTkinter/
├─ src/
│  └─ calculator.py
└─ README.md
```

## Zipping & Submitting (as per instructions)

1. Right-click the **CalculatorTkinter** folder.
2. Click **Send to → Compressed (zipped) folder** (Windows) or **Compress "CalculatorTkinter"** (macOS).
3. Upload the resulting ZIP to Google Drive.
4. In Drive, right-click the uploaded file → **Share** → change to **Anyone with the link** and copy the link.
5. Submit that accessible link.

If you face any issues, you can also refer to the provided video guide.
