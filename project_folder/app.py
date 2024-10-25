from flask_migrate import Migrate
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    streak = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    recurrence = db.Column(db.String(20), nullable=False, default='none')  # Recurring tasks
    category = db.Column(db.String(50), nullable=False)  # Categories/tags
    priority = db.Column(db.String(20), nullable=False, default='medium')  # Task prioritization

@app.route('/')
def index():
    category_filter = request.args.get('category')
    if category_filter:
        tasks = Task.query.filter_by(category=category_filter).order_by(Task.priority.desc(), Task.due_date).all()
    else:
        tasks = Task.query.order_by(Task.priority.desc(), Task.due_date).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    due_date = request.form['due_date']
    recurrence = request.form['recurrence']
    category = request.form['category']
    priority = request.form['priority']
    new_task = Task(
        name=task_name, 
        due_date=datetime.strptime(due_date, '%Y-%m-%d'), 
        recurrence=recurrence, 
        category=category, 
        priority=priority
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

def handle_recurring_tasks():
    tasks = Task.query.all()
    for task in tasks:
        if task.completed and task.recurrence != 'none':
            if task.recurrence == 'daily':
                task.due_date += timedelta(days=1)
            elif task.recurrence == 'weekly':
                task.due_date += timedelta(weeks=1)
            elif task.recurrence == 'monthly':
                task.due_date += timedelta(weeks=4)  # Approximate month
            task.completed = False
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)

migrate = Migrate(app, db)

