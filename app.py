from flask import Flask, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('counters.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS counters
                 (name TEXT PRIMARY KEY, value INTEGER)''')
    # Initialize counters if they don't exist
    c.execute('INSERT OR IGNORE INTO counters VALUES (?, ?)', ('doors', 0))
    c.execute('INSERT OR IGNORE INTO counters VALUES (?, ?)', ('wheels', 0))
    conn.commit()
    conn.close()

def get_counters():
    conn = sqlite3.connect('counters.db')
    c = conn.cursor()
    c.execute('SELECT name, value FROM counters')
    result = dict(c.fetchall())
    conn.close()
    return result

def increment_counter(counter_type):
    conn = sqlite3.connect('counters.db')
    c = conn.cursor()
    c.execute('UPDATE counters SET value = value + 1 WHERE name = ?', (counter_type,))
    conn.commit()
    conn.close()

# Initialize database
init_db()

@app.route('/')
def index():
    counters = get_counters()
    return render_template('index.html', counters=counters, abs=abs)

@app.route('/increment/<counter_type>')
def increment(counter_type):
    if counter_type in ['doors', 'wheels']:
        increment_counter(counter_type)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)