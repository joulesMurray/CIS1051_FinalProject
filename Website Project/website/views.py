from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Entry
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        name = request.form.get('name')#This will get the name from HTML
        amount = request.form.get('amount')#Gets the dollar amount of the service
       
        if not name:
            flash('Name is required!', category='error') 
        elif not amount or float(amount) <= 0:
            flash('Please enter a valid dollar amount!', category='error')
        else:
            try:
                 new_entery = Entry(name=name, amount=float(amount), user_id=current_user.id)
                 db.session.add(new_entery)
                 db.session.commit()
                 flash('Information Added', category='success')
            except Exception as e:
                 print(f"Error: {e}")
                 flash('Error, try again', category='error')
    entries = Entry.query.filter_by(user_id=current_user.id).all()

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_entry():  
    entry_data = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    entryId = entry_data.get['entryId']
    entry = Entry.query.get(entryId)
    if entry:
        if entry.user_id == current_user.id:
            try:
                db.session.delete(entry)
                db.session.commit()
                return jsonify({'message': 'The entry you selected was deleted successfully'}), 200
            except Exception as e:
                return jsonify({'error': 'There was an error deleting the entry, please try again'}), 400

    return jsonify({'error': 'Entry was not found or you do not have permission to delete that entry'}), 404