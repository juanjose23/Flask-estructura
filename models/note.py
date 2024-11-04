from utils.db import db

class Note(db.Model):
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)

    task = db.relationship('Task', backref=db.backref('notes', lazy=True))

    def __init__(self, content, task_id):
        self.content = content
        self.task_id = task_id
