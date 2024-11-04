from flask import  jsonify ,Blueprint, render_template, request, redirect, url_for, flash
from models.task import Task
from models.note import Note
from utils.db import db
from datetime import datetime 
task = Blueprint("tasks", __name__)


@task.route('/tasks', methods=['GET'])
def index():
  
    if Task.query.count() == 0:
        new_task = Task(title='Meeting', description='Discuss project updates', due_date=datetime.utcnow(), is_completed=False, contact_id=2)
        db.session.add(new_task)
        db.session.commit()
    all_tasks = Task.query.all()
    return jsonify([{'id': t.id, 'title': t.title, 'description': t.description, 'due_date': t.due_date.isoformat(), 'is_completed': t.is_completed, 'contact_id': t.contact_id} for t in all_tasks]), 200

@task.route('/contact/<int:contact_id>/tasks_and_notes', methods=['GET'])
def tasks_and_notes_by_contact(contact_id):
    # Obtener todas las tareas para el contacto específico
    tasks = Task.query.filter_by(contact_id=contact_id).all()
    # Obtener todas las notas para el contacto específico
    notes = Note.query.filter_by(task_id=contact_id).all()  # Asegúrate de que estás usando la relación correcta

    # Preparar la respuesta
    response = {
        'tasks': [{'id': t.id, 'title': t.title, 'description': t.description, 'due_date': t.due_date.isoformat(), 'is_completed': t.is_completed, 'contact_id': t.contact_id} for t in tasks],
        'notes': [{'id': n.id, 'content': n.content, 'task_id': n.task_id} for n in notes]
    }

    return jsonify(response), 200

@task.route('/actualizar/<int:task_id>', methods=['POST'])
def update_task(task_id):
    # Obtener la tarea de la base de datos por su ID
    task_to_update = Task.query.get(task_id)
    
    # Verificar si la tarea existe
    if not task_to_update:
        return jsonify({"error": "Task not found"}), 404

    # Obtener los datos de la solicitud
    data = request.get_json()

    # Actualizar los campos necesarios
    task_to_update.title = data.get('title', task_to_update.title)
    task_to_update.description = data.get('description', task_to_update.description)
    task_to_update.due_date = data.get('due_date', task_to_update.due_date)
    task_to_update.is_completed = data.get('is_completed', task_to_update.is_completed)
    task_to_update.contact_id = data.get('contact_id', task_to_update.contact_id)

    # Guardar los cambios en la base de datos
    db.session.commit()

    return jsonify({
        'id': task_to_update.id,
        'title': task_to_update.title,
        'description': task_to_update.description,
        'due_date': task_to_update.due_date.isoformat(),
        'is_completed': task_to_update.is_completed,
        'contact_id': task_to_update.contact_id
    }), 200