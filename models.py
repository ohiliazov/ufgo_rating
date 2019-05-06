from manage import db


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    code = db.Column(db.String(2), nullable=False, unique=True)

    players = db.relationship("Player")
    tournaments = db.relationship("Tournament")

    def __repr__(self):
        return f'City: {self.name}'

    def __str__(self):
        return self.name


class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    pin = db.Column(db.String, unique=True)
    full_name = db.Column(db.String(64))
    japanese_rank = db.Column(db.String(3))
    national_rank = db.Column(db.String(5))
    is_active = db.Column(db.Boolean, default=True)
    ratings = db.relationship("TournamentPlayer")

    def __repr__(self):
        return f'Player: {self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Tournament(db.Model):
    __tablename__ = 'tournament'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))

    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    info = db.Column(db.Text)

    matches = db.relationship("Match")
    participants = db.relationship("TournamentPlayer")

    def __repr__(self):
        return f"Tournament: {self.name}"

    def __str__(self):
        return f"{self.name} {self.date}"


class TournamentPlayer(db.Model):
    __tablename__ = 'tournament_player'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))

    rating_start = db.Column(db.Integer, nullable=False)
    rating_end = db.Column(db.Integer, nullable=False)
    is_manual = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Rating: {self.player_id} {self.tournament_id} {self.rating}'

    def __str__(self):
        return f'{self.player_id} {self.tournament_id} {self.rating}'


class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(
        db.Integer, db.ForeignKey('tournament_player.id', name='fk_player_id'))
    opponent_id = db.Column(
        db.Integer, db.ForeignKey('tournament_player.id', name='fk_opponent_id'))

    result = db.Column(db.Enum('win', 'loss', 'draw'), nullable=True)
    color = db.Column(db.Enum('black', 'white'), nullable=True)
    handicap = db.Column(db.Integer, default=0)
    is_ranked = db.Column(db.Boolean, default=True)
