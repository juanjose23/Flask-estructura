from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.contact import Contact
from utils.db import db
from marshmallow import Schema, fields, validates, ValidationError
import re
contacts = Blueprint("contacts", __name__)
class ContactSchema(Schema):
    fullname = fields.Str(required=True, validate=lambda s: 1 <= len(s) <= 100)  # Longitud mínima y máxima
    email = fields.Email(required=True)
    phone = fields.Str(required=True, validate=lambda s: re.match(r'^\+?[1-9]\d{1,14}$', s))  # Validación de formato de número de teléfono

    @validates('email')
    def validate_email_domain(self, email):
        # Validar que el dominio del correo electrónico sea válido
        allowed_domains = ['example.com', 'example.org','gmail.com']  # Reemplaza con tus dominios permitidos
        if email.split('@')[1] not in allowed_domains:
            raise ValidationError("Email domain must be one of: {}".format(", ".join(allowed_domains)))

    @validates('fullname')
    def validate_fullname(self, fullname):
        if not re.match(r'^[a-zA-Z\s]+$', fullname):
            raise ValidationError("Full name must contain only letters and spaces.")

    @validates('phone')
    def validate_phone(self, phone):
        if len(phone) < 7 or len(phone) > 15:  # Ejemplo de longitud para números de teléfono
            raise ValidationError("Phone number must be between 7 and 15 digits.")


@contacts.route('/')
def index():
    all_contacts = Contact.query.all()
    return render_template('index.html', contacts=all_contacts)

@contacts.route('/new', methods=['POST'])
def add_contact():
    schema = ContactSchema()
    if request.method == 'POST':
        try:
            # Recibir datos del formulario y validarlos
            contact_data = schema.load(request.form)
            print(contact_data)

            # Crear un nuevo objeto Contact
            new_contact = Contact(fullname=contact_data['fullname'], email=contact_data['email'], phone=contact_data['phone'])

            # Guardar el objeto en la base de datos
            db.session.add(new_contact)
            db.session.commit()

            flash('Contact added successfully!', 'success')
        except ValidationError as err:
            flash(f"Error adding contact: {err.messages}", 'danger')

        return redirect(url_for('contacts.index'))

@contacts.route("/update/<string:id>", methods=["GET", "POST"])
def update(id):
    contact = Contact.query.get(id)
    if not contact:
        flash('Contact not found!', 'danger')
        return redirect(url_for('contacts.index'))

    if request.method == "POST":
        schema = ContactSchema()
        try:
            # Validar los datos del formulario
            contact_data = schema.load(request.form)
            contact.fullname = contact_data['fullname']
            contact.email = contact_data['email']
            contact.phone = contact_data['phone']

            db.session.commit()
            flash('Contact updated successfully!', 'success')
            return redirect(url_for('contacts.index'))
        except ValidationError as err:
            flash(f"Error updating contact: {err.messages}", 'danger')

    return render_template("update.html", contact=contact)

@contacts.route("/delete/<id>", methods=["GET"])
def delete(id):
    contact = Contact.query.get(id)
    if not contact:
        flash('Contact not found!', 'danger')
        return redirect(url_for('contacts.index'))

    db.session.delete(contact)
    db.session.commit()
    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('contacts.index'))

@contacts.route("/about")
def about():
    return render_template("about.html")
