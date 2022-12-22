from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

# Setting Up Flask App and Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "49inCoding"
db = SQLAlchemy(app)


# Class
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), unique=True)


# with app.app_context():
#     db.create_all()

# Routes for the website
@app.route("/")
def home():
    tasks = db.session.query(Tasks).all()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["GET", "POST"])
def add_task():
    task_to_add = request.form["newTask"]
    new_task = Tasks(
        task=task_to_add
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/remove", methods=["GET", "POST"])
def remove_task():
    task_id = request.args.get("id")
    task_to_delete = Tasks.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
