from flask import Flask, render_template
from flask_assets import Bundle, Environment
import lib.parse_html as p

app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()


@app.route("/")
@app.route("/index")
def index():
    return render_template("raw.html")


@app.route("/question/<int:id>")
def question(id: int):
    soup = p.get_soup(id)
    return render_template(
        "question.html",
        image_link=p.get_image_link(soup),
        question=str(p.get_question(soup)),
        answers= p.get_answers(soup),
        enc_string=p.get_enc_string(p.get_script(soup),id),
        id=id
    )


if __name__ == "__main__":
    app.run(debug=True)
