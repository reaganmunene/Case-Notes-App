import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "notes.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    return "Server is running"

@app.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    result = []
    for note in notes:
        result.append({
            'id': note.id,
            'title': note.title,
            'content': note.content
        })
    return result

@app.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    new_note = Note(title=data['title'], content=data['content'])
    db.session.add(new_note)
    db.session.commit()
    return {
        'id': new_note.id,
        'title': new_note.title,
        'content': new_note.content
    }, 201

@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = Note.query.get_or_404(note_id)
    return {
        'id': note.id,
        'title': note.title,
        'content': note.content
    }

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return {'message': f'Note {note_id} deleted'}, 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print(f"Database initialized at: {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.run(debug=True, port=5000)