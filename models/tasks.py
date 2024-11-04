from utils.db import db

class Task(db.Model):
    __tablename__ = 'tasks'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=True)  # Relación con el modelo Contact

    contact = db.relationship('Contact', backref='tasks')  # Relación inversa con Contact

    def __init__(self, title, description, due_date=None, is_completed=False, contact_id=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.is_completed = is_completed
        self.contact_id = contact_id

    def __repr__(self):
        return f'<Task {self.title}>'
