from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from flask_sqlalchemy import SQLAlchemy
import lib.parse_html as p
import json
app = Flask(__name__)
app.secret_key = "vewy secwet uwu"

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

db_name = "CodigoQuiz.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class Score(db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    score = db.Column(db.Integer)

    def __init__(self, name, score):
        self.name = name
        self.score = score


db.create_all()
# Score.query.delete()
db.session.commit()


@app.route("/")
def index():
    records = Score.query.all()
    records.sort(reverse = True, key = lambda x : x.score)

    return render_template("index.html",records=records)


@app.route("/quiz")
def quiz():
    return render_template("quiz.html")


@app.route("/question/<int:id>", methods=["GET"])
def question(id: int):
    soup = p.get_soup(id)
    obj = {
        "question": str(p.get_question(soup)),
        "answers": p.get_answers(soup),
        "enc_string": p.get_enc_string(p.get_script(soup), id),
        "id": id,
    }
    return obj

@app.route("/quiz/record", methods=["POST"])
def post_record():
    try: req = (request.get_json())
    except : req = (request.from_values())
    db.session.add(Score("NAME",req["score"]))
    db.session.commit()
    return req["name"]


@app.route("/db")
def db_show():
    return str(list(map(lambda x: x.__dict__ ,Score.query.all())))


@app.route("/questao/<int:id>", methods=["GET"])
def questao(id: int):
    soup = p.get_soup(id)
    return render_template(
        "question.html",
        render_template=render_template,
        image_link=p.get_image_link(soup),
        question=str(p.get_question(soup)),
        answers=p.get_answers(soup),
        enc_string=p.get_enc_string(p.get_script(soup), id),
        id=id,
    )


if __name__ == "__main__":
    app.run(debug=True)
