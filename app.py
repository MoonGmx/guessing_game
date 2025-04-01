from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Contact Model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)

# Home Page - List Contacts
@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

# Add Contact
@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    new_contact = Contact(name=name, phone=phone, email=email)
    db.session.add(new_contact)
    db.session.commit()
    return redirect(url_for('index'))

# Delete Contact
@app.route('/delete/<int:id>')
def delete_contact(id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('index'))

# Search Contact
@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    contacts = Contact.query.filter(Contact.name.ilike(f"%{query}%")).all()
    return jsonify([{'id': c.id, 'name': c.name, 'phone': c.phone, 'email': c.email} for c in contacts])

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
