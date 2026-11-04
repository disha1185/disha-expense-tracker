# Disha Expense Tracker

A web-based expense management application built using Python, Flask, SQLite, HTML and CSS.

## Features
- Add expenses
- Categorize expenses
- View expense history
- Delete expenses
- Calculate total expenses
- Persistent SQLite database storage

## Technology Stack
- Python
- Flask
- SQLite
- HTML and CSS
- Docker
- Gunicorn

## Run with Docker

docker build -t disha-expense-tracker:v2 .

docker run -d \
  --name disha-expense-container \
  -p 5000:5000 \
  -v ~/disha-expense-data:/app/data \
  disha-expense-tracker:v2

## Access

http://localhost:5000
