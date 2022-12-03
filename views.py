from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from models import Note
from app import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 5:
            flash('笔记太短了', category='error')
        else:
            new_note = Note(note=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
    return render_template('home.html', user=current_user)


@views.route('/delete/note', methods=['POST'])
def delete_note():
    data = json.loads(request.data)
    note_id = data.get('noteID')
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('删除成功!', category='success')
    return jsonify({})

