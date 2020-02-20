from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<Task %r>" % self.id


@app.route("/", methods=["GET", "POST"])
def todo_list():
    data = Task.query.all()
    if request.method == "GET":
        return render_template("index.html", data=data)
    else:
        content = request.form["content"]
        new_task = Task(content=content)
        if len(new_task.content) > 0:
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect("/")
            except:
                return "Something went wrong with adding your task to database"
        else:
            return render_template("index.html", data=data)


@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "Something went wrong with deleting your task from database"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task_to_update = Task.query.get_or_404(id)
    if request.method == "GET":
        return render_template("update.html", task=task_to_update)
    else:
        task_to_update.content = request.form["content"]
        task_to_update.date = datetime.now()
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Something went wront with updating your task in database"


if __name__ == "__main__":
    app.run(debug=True)
