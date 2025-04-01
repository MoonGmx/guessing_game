from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "database/contacts.db"

# Function to connect to the database
def connect_db():
    return sqlite3.connect(DATABASE)

# Initialize database and create table
with connect_db() as conn:
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts 
                      (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT)''')
    conn.commit()

# Home Page - Show Contacts & Search
@app.route('/')
def home():
    query = request.args.get('q', '')  # Get search query if exists
    conn = connect_db()
    cursor = conn.cursor()
    
    if query:
        cursor.execute("SELECT * FROM contacts WHERE name LIKE ?", ('%' + query + '%',))
    else:
        cursor.execute("SELECT * FROM contacts")
    
    contacts = cursor.fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts, query=query)

# Add Contact
@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
    conn.commit()
    conn.close()
    
    return redirect(url_for('home'))

# Delete Contact
@app.route('/delete/<int:id>')
def delete_contact(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
