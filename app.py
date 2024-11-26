from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Contacts
from config import AppConfig

app = Flask(__name__)
app.config.from_object(AppConfig)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        relation = request.form['relation']
        
        if not name or not phone or not relation:
            return render_template('home.html', error = "Please fill in all the fields")
        
        existing_contact = Contacts.query.filter_by(name=name).first()
        if existing_contact:
            return render_template('home.html', error="A contact with this name already exists")
    
        new_contact = Contacts(name = name, phone = phone, relation = relation)
        db.session.add(new_contact)
        db.session.commit()
    
    contacts = Contacts.query.order_by(Contacts.id.desc()).all()
    return render_template('home.html', contacts=contacts)


@app.route('/delete/<int:id>')
def delete(id):
    contact = Contacts.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    contact = Contacts.query.get_or_404(id)
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.phone= request.form['phone']
        contact.relation = request.form['relation']
        
        db.session.commit()
        return redirect('/')
    
    return render_template('edit.html', contact=contact)

if __name__ == '__main__':
    app.run(debug=True)