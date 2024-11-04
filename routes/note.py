from flask import Blueprint, jsonify,request
from models.note import Note  # Asegúrate de que la ruta sea correcta
from utils.db import db
from datetime import datetime

notes = Blueprint("notes", __name__)

# Leer todas las notas
@notes.route('/notes', methods=['GET'])
def get_notes():
    all_notes = Note.query.all()
    return jsonify([{'id': n.id, 'content': n.content, 'task_id': n.task_id} for n in all_notes]), 200

# Crear una nueva nota
@notes.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()  # Obtener datos del cuerpo de la solicitud
    if not data or 'content' not in data or 'task_id' not in data:
        return jsonify({'error': 'Bad Request', 'message': 'Content and task_id are required'}), 400

    new_note = Note(content=data['content'], task_id=data['task_id'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'id': new_note.id, 'content': new_note.content, 'task_id': new_note.task_id}), 201

# Actualizar una nota existente
@notes.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get(note_id)
    if note is None:
        return jsonify({'error': 'Not Found', 'message': 'Note not found'}), 404

    data = request.get_json()
    if 'content' in data:
        note.content = data['content']
    if 'task_id' in data:
        note.task_id = data['task_id']
    
    db.session.commit()
    return jsonify({'id': note.id, 'content': note.content, 'task_id': note.task_id}), 200

# Eliminar una nota
@notes.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note is None:
        return jsonify({'error': 'Not Found', 'message': 'Note not found'}), 404

    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted successfully'}), 204

