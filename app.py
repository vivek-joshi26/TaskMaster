from flask import Flask, render_template, url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
import os, json, signal
from datetime import datetime

from flask.json import jsonify
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Creates structure for the Table inside the DB
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default =datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# Routes the request received
@app.route('/', methods=['POST','GET'])
def index():
    # For POST request below section will be executed
    if request.method == 'POST':
        # Data will be passed from the Input tag inside Form of index.html file whose name is content
        task_content = request.form['content']
        # A new object for Todo will be created which can be persisted on the DB
        new_task = Todo(content=task_content)
        try:
            # we try to connect to the DB and commit the changes
            db.session.add(new_task)
            db.session.commit()
            # once above 2 steps executes it will redirect to the mentioned link
            return redirect('/')
        except:
            # In case there'a any error encountered in the try block it will be handled from here
            return 'There was an error adding your task'
    # GET request will come here
    else:
        # we are getting all the tasks present in the Todo table in the order of date
        tasks = Todo.query.order_by(Todo.date_created).all()
        # it will pass the tasks to the index.html page
        return render_template("index.html", tasks = tasks)

# This is called from the index page, when we click on delete, it contain hyperlink for delete/task.id
@app.route('/delete/<int:id>')
def delete(id):
    # IT tries to get the data from the DB and if not present will return 404
    task_to_delete = Todo.query.get_or_404(id)

    try:
        # Used to Delete the record from the DB
        db.session.delete(task_to_delete)
        db.session.commit()
        # After deleting redirects back to the homepage
        return redirect('/')
    except:
         return "There was a problem deleting this task"


# This is called from the index page, when we click on update, it contain hyperlink for update/task.id
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    # IT tries to get the data from the DB and if not present will return 404
    task = Todo.query.get_or_404(id)

    # POST method is directed when we click on the Update Task button on the update.html page
    if request.method == 'POST':
        # It updates the content of the earlier task data with what is written in the text area of update.html page with class name as content
        task.content = request.form['content']
        try:
            # updates the record in DB and redirects back to homepage
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating the Task"
    else:
        # By default it comes to else because when we click on update in the index.html page it's a get request, so now update.html page will be displayed on the screen and the task will be passed to it
        return render_template('update.html', task = task)

@app.route('/stopServer')
def stopServer():
    os.kill(os.getpid(),signal.SIGINT)
    return jsonify({"success": True, "message" :"Server is shutting down"})
    

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port= 8070)


