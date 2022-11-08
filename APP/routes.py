from APP.db.db import get_db, get_user
from APP.lib import parse_html as p
import APP.user as u
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


def init_routes(app):
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
        except:
            usr_name = None

        return render_template(
            "index.html", cur=str(records), curr_usr_name=usr_name, records=leaderboard
        )

    @app.route("/quiz")
    def quiz():
        wrong_answers = []
        if g.user:
            db = get_db()
            u_id = g.user["id"]
            wrong_answers = db.execute(f"SELECT question_id FROM answer_log WHERE status = 'Wrong' AND author_id = {u_id}").fetchall()
        return render_template("quiz.html",data=[x[0] for x in wrong_answers])
    @app.route("/profile")
    def profile():
        db = get_db()
        records = db.execute(
            "SELECT * FROM record WHERE author_id =" + str(g.user["id"])
        ).fetchall()
        for record in records:
            db.execute(f"SELECT * FROM answer_log WHERE record_id ={record[0]}")

        records.sort(reverse=True, key=lambda x: x[3])
        return render_template(
            "profile.html", records=records, logs=u.get_all_logs(g.user["id"]), str=str
        )

    @app.route("/profile/edit")
    def edit_profile():
        return render_template("edit_profile.html")


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

    @app.route("/record/<int:r_id>", methods=["GET"])
    def record_by_id(r_id):
        db = get_db()
        record = db.execute(f"SELECT * FROM record WHERE id ={r_id}").fetchone()
        if g.user and g.user["id"] == record[1]:
            return render_template(
                "database.html",
                command=f"SELECT * FROM answer_log WHERE record_id ={r_id}",
                db=db,
                len=len,
                enumerate=enumerate,
            )
        else:
            return "You must be the author of this record to access it"

    @app.route("/db/<string:table>", methods=["GET"])
    def render_db(table):
        db = get_db()
        command = "SELECT * FROM " + table
        if table == "schema":
            with open("APP/db/schema.sql", "r") as f:
                return f.read()

        import sqlite3

        try:
            db.execute(command)
        except sqlite3.OperationalError:
            return f"""no table named {table}"""
        else:
            return render_template(
                "database.html",
                db=db,
                table=table,
                command=command,
                enumerate=enumerate,
                len=len,
            )
