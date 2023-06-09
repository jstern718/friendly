from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

bcrypt = Bcrypt()
db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://i.pinimg.com/originals/4a/d8/60/4ad860d80de937bc63f5a7069b7d0215.jpg"


class Match(db.Model):

    __tablename__ = 'matches'

    user_being_matched = db.Column(
        db.String(16),
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True,
    )

    user_matching = db.Column(
        db.String(16),
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True,
    )

    match_status = db.Column(
        db.Boolean,
        nullable=False,
    )


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    username = db.Column(
        db.String(16),
        primary_key=True,
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.String(256),
        nullable=False,
    )

    first_name = db.Column(
        db.String(50),
        nullable=False,
    )

    last_name = db.Column(
        db.String(30),
        nullable=False,
    )

    hobbies = db.Column(
        db.Text,
        nullable=False,
        default="",
    )

    interests = db.Column(
        db.Text,
        nullable=False,
        default="",
    )

    zipcode = db.Column(
        db.String(5),
        nullable=False,
    )

    friend_radius = db.Column(
        db.Integer,
        nullable=False,
    )

    image_url = db.Column(
        db.String(255),
        nullable=False,
        default=DEFAULT_IMAGE_URL,
    )


    matched = db.relationship(
        "User",
        secondary="matches",
        primaryjoin=(Match.user_being_matched == username),
        secondaryjoin=(Match.user_matching == username),
        backref="matching",
    )


    def __repr__(self):
        return f"<User #{self.username}: {self.first_name} {self.last_name}, {self.email}>"


    @classmethod
    def signup(cls, username, first_name, last_name, email, password,
               hobbies, interests, zipcode, friend_radius,
               image_url=DEFAULT_IMAGE_URL):
        """Sign up user.

        Hashes password and adds user to session.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd,
            hobbies=hobbies,
            interests=interests,
            zipcode=zipcode,
            friend_radius=friend_radius,
            image_url=image_url,
        )

        db.session.add(user)
        return user


    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = cls.query.filter_by(username=username).one_or_none()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)