from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To avoid warning
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Incomplete')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Create tables if not exist
@app.before_first_request
def create_tables():
    db.create_all()

# Home route (GET and POST to add tasks)
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':  # Add a task
        new_task = Task(
            title=request.form['title'],
            due_date=request.form['due_date'],
            priority=request.form['priority'],
            user_id=session['user_id']
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))

    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return render_template('tasks.html', tasks=tasks, user=session['username'])

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            flash('Username already exists')
        else:
            hashed_password = generate_password_hash(request.form['password'])
            new_user = User(username=request.form['username'], password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created. Please login.')
            return redirect(url_for('login'))
    return render_template('register.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Update task status route
@app.route('/update_status/<int:id>')
def update_status(id):
    task = Task.query.get_or_404(id)
    task.status = 'Complete' if task.status == 'Incomplete' else 'Incomplete'
    db.session.commit()
    return redirect(url_for('home'))

# Delete task route
@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))
@app.route('/test')
def test():
    return render_template('base.html')


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)

