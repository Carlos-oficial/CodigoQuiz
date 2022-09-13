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
    db.commit()
    return req["name"]