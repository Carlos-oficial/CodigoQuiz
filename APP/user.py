from APP.db.db import get_db, get_user
from APP.lib import parse_html as p

def concat_matrix(matrix):
    acc = []
    for l in matrix:
        for item in l:
            acc.append(item)
    return acc

def get_all_logs(u_id):
    db = get_db()
    records = db.execute(
        f"SELECT * FROM record WHERE author_id ={u_id}"
    ).fetchall()
    logs_ = [db.execute(f"SELECT * FROM answer_log WHERE record_id ={record[0]}").fetchall() for record in records]
    logs = [(x[3],x[0],x[1]) for x in concat_matrix(logs_)]
    return logs

