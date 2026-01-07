from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# Association tables
user_likes = db.Table('zyra_user_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('zyra_user.id'), primary_key=True),
    db.Column('music_id', db.Integer, db.ForeignKey('zyra_music.id'), primary_key=True)
)

playlist_songs = db.Table('zyra_playlist_songs',
    db.Column('playlist_id', db.Integer, db.ForeignKey('zyra_playlist.id'), primary_key=True),
    db.Column('music_id', db.Integer, db.ForeignKey('zyra_music.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'zyra_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(20), default='user')
    subscription = db.relationship('Subscription', backref='user', uselist=False, lazy='joined')
    liked_songs = db.relationship('Music', secondary=user_likes, lazy='dynamic', backref=db.backref('liked_by', lazy='dynamic'))
    playlists = db.relationship('Playlist', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'subscription': self.subscription.to_dict() if self.subscription else None
        }

class Plan(db.Model):
    __tablename__ = 'zyra_plan'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    features = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'duration_days': self.duration_days,
            'features': self.features
        }

class Subscription(db.Model):
    __tablename__ = 'zyra_subscription'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('zyra_user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('zyra_plan.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='active')
    
    plan = db.relationship('Plan')

    def to_dict(self):
        return {
            'plan_name': self.plan.name,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'status': self.status
        }
    
    @property
    def is_active(self):
        return self.status == 'active' and self.end_date > datetime.utcnow()

class Playlist(db.Model):
    __tablename__ = 'zyra_playlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('zyra_user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    songs = db.relationship('Music', secondary=playlist_songs, lazy='subquery',
        backref=db.backref('playlists', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'song_count': len(self.songs)
        }

class Payment(db.Model):
    __tablename__ = 'zyra_payment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('zyra_user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('zyra_plan.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='INR')
    status = db.Column(db.String(20), default='completed')
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='payments')

class Music(db.Model):
    __tablename__ = 'zyra_music'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    artist = db.Column(db.String(120), nullable=False)
    album = db.Column(db.String(120))
    url = db.Column(db.String(255), nullable=False)
    cover_image = db.Column(db.String(255))
    is_premium = db.Column(db.Boolean, default=False)
    genre = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'url': self.url,
            'cover_image': self.cover_image,
            'is_premium': self.is_premium,
            'genre': self.genre
        }
