from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

# import hazelcast

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)


# client = hazelcast.HazelcastClient(cluster_name="tasks") 

# map = client.get_map("my-distributed-map").blocking()

# map.put("1", "John")
# map.put("2", "Mary")
# map.put("3", "Jane")


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    picture = db.Column(db.String(255), nullable=True)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        picture = request.files['picture'] if 'picture' in request.files else None

        if picture:
            filename = secure_filename(picture.filename)
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        new_task = Task(title=title, description=description, picture=filename)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('delete.html', task=task)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
