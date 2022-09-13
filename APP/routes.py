from APP.db.db import get_db, get_user
from APP.lib import parse_html as p
import json

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

def init_routes(app, render_template):
    @app.route("/")
    def index():
        db = get_db()
        records = db.execute("SELECT * FROM record").fetchall()
        records.sort(reverse=True, key=lambda x: x[3])

        leaderboard = [
            (get_user(record[1], db)["username"], record[2], record[3])
            for record in records
        ]
        try:
            current_uid = session["user_id"]
            usr_name = get_user(session["user_id"], db)["username"]
        except :
            usr_name = None

        return render_template(
            "index.html", cur=str(records), curr_usr_name=usr_name, records=leaderboard
        )

    @app.route("/quiz")
    def quiz():
        return render_template("quiz.html")

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

    @app.route("/db/<string:table>", methods=["GET"])
    def render_db(table):
        db = get_db()
        command = 'SELECT * FROM '+ table
        return render_template('database.html',db=db,table=table,command=command,enumerate=enumerate)
    
    