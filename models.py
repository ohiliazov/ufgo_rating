from manage import db


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    players = db.relationship("Player")

    def __repr__(self):
        return f'City: {self.name}'

    def __str__(self):
        return self.name


class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    ratings = db.relationship("RatingHistory")
    japanese_rank = db.Column(db.String(10))
    national_rank = db.Column(db.String(10))

    def __repr__(self):
        return f'Player: {self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class RatingHistory(db.Model):
    __tablename__ = 'rating_history'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    date = db.Column(db.DateTime, nullable=False)
    rating = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'Rating: {self.player_id} {self.date} {self.rating}'

    def __str__(self):
        return {self.rating}


def add_city(name: str):
    if db.session.query(City).filter(City.name == 'Kharkiv') is None:
        db.session.add(City(name=name))
        db.session.commit()
