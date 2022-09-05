class Score(db.Model):
    __tablename__ = 'records'
    name = db.Column(db.String)
    score = db.Column(db.Integer)

    def __init__(self, name, score):
        self.name = name
        self.score = score