from flask import  jsonify ,Blueprint, render_template, request, redirect, url_for, flash
from models.events import Event
from utils.db import db
from datetime import datetime 
events = Blueprint("events", __name__)


@events.route('/events')
def index():
    if Event.query.count() == 0: 
        new_event = Event(title='Meeting', date=datetime.utcnow(), contact_id=2)
        db.session.add(new_event)
        db.session.commit()

    all_events = Event.query.all()
    return jsonify([{'id': e.id, 'title': e.title, 'date': e.date.isoformat(), 'contact_id': e.contact_id} for e in all_events]), 200


@events.route('/events/contact/<int:contact_id>', methods=['GET'])
def events_by_contact(contact_id):
    # Filtra los eventos por el ID del contacto
    events_for_contact = Event.query.filter_by(contact_id=contact_id).all()
    
    if not events_for_contact:
        return jsonify({'message': 'No events found for this contact.'}), 404

    return jsonify([{'id': e.id, 'title': e.title, 'date': e.date.isoformat(), 'contact_id': e.contact_id} for e in events_for_contact]), 200