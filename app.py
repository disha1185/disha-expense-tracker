from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)
DATABASE = "/app/data/expenses.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                expense_date TEXT NOT NULL
            )
        """)

@app.route("/")
def index():
    with get_db() as conn:
        expenses = conn.execute(
            "SELECT * FROM expenses ORDER BY expense_date DESC, id DESC"
        ).fetchall()

        total = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses"
        ).fetchone()[0]

    return render_template("index.html", expenses=expenses, total=total)

@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form.get("title", "").strip()
    amount = request.form.get("amount", "").strip()
    category = request.form.get("category", "").strip()
    expense_date = request.form.get("expense_date", "").strip()

    if not title or not category or not amount or not expense_date:
        return "Please fill in all fields.", 400

    try:
        amount = float(amount)
        if amount <= 0:
            return "Amount must be greater than zero.", 400
    except ValueError:
        return "Enter a valid amount.", 400

    with get_db() as conn:
        conn.execute(
            """INSERT INTO expenses (title, amount, category, expense_date)
               VALUES (?, ?, ?, ?)""",
            (title, amount, category, expense_date)
        )

    return redirect(url_for("index"))

@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    with get_db() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    return redirect(url_for("index"))

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
