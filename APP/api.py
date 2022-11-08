from APP.lib import parse_html as p
from APP.db.db import get_db, get_user


from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/questao/<int:id>", methods=["GET"])
def question(id: int):
    soup = p.get_soup(id)
    obj = {
        "question": str(p.get_question(soup)),
        "answers": p.get_answers(soup),
        "enc_string": p.get_enc_string(p.get_script(soup), id),
        "question_info": p.get_question_info(soup),
        "id": id,
    }
    return obj

@api.route("/record", methods=["POST"])
def post_record():
    db = get_db()
    try:
        req = request.get_json()
    except:
        req = request.from_values()
    try:
        curr_usr = session["user_id"]
    except KeyError:
        flash("not logged in bruh")
    else:
        db.execute(
            "INSERT INTO record (author_id,score) VALUES(?,?)",
            (session["user_id"], req["score"]),
        )
        record_id = db.execute('SELECT * FROM record ORDER BY id DESC LIMIT 1').fetchone()[0]
        # db.execute('INSERT INTO answer_log VALUES(?,?,?)',(req['wrong_answers'][0],"Wrong",session["user_id"]))

        for answer in req['wrong_answers']:
            db.execute('INSERT INTO answer_log VALUES(?,?,?,?)',(answer,"Wrong",session["user_id"],record_id))
        for answer in req['right_answers']:
            db.execute('INSERT INTO answer_log VALUES(?,?,?,?)',(answer,"Right",session["user_id"],record_id))
    db.commit()
    return "DONE YAY"