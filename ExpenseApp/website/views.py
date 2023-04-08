from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User, Category, Expense
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    if request.method == 'POST':
        name = request.form.get('name')
        user_id = current_user.id
        if not name:
            flash('Name is required!', category='error')
        else:
            category = Category(name=name, user_id=user_id) 
            db.session.add(category)
            db.session.commit()
            flash('Category created!', category='success')

    categories = Category.query.all()
    return render_template('categories.html', user=current_user, categories=categories)

@views.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    if request.method == 'POST':
        amount = request.form.get('amount')
        category_id = request.form.get('category')

        if not amount:
            flash('Amount is required!', category='error')
        elif not category_id:
            flash('Category is required!', category='error')
        else:
            expense = Expense(amount=amount, category_id=category_id, user_id=current_user.id)
            db.session.add(expense)
            db.session.commit()
            flash('Expense created!', category='success')

    categories = Category.query.all()
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return render_template('expenses.html', user=current_user, categories=categories, expenses=expenses)


@views.route('/expenses/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first()
    if expense:
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted!', category='success')
    else:
        flash('Expense not found!', category='error')
    return redirect(url_for('views.expenses'))
