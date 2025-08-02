from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy 
db = SQLAlchemy()

# -------------------
# User model
# -------------------
class User(db.Model):
    """
    Represents both admin and normal users.
    Admin is identified by is_admin=True.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)  # email
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    qualification = db.Column(db.String(120))
    dob = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


# -------------------
# Subject model
# -------------------
class Subject(db.Model):
    """
    Represents a field of study. Created by Admin.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)


# -------------------
# Chapter model
# -------------------
class Chapter(db.Model):
    """
    Represents a module under a Subject.
    """
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)

    # Relationship back to Subject
    subject = db.relationship('Subject', backref=db.backref('chapters', lazy=True))


# -------------------
# Quiz model
# -------------------
class Quiz(db.Model):
    """
    Represents a quiz for a specific Chapter.
    """
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    title = db.Column(db.String(255))
    date_of_quiz = db.Column(db.Date)
    time_duration = db.Column(db.Time)
    remarks = db.Column(db.Text)

    chapter = db.relationship('Chapter', backref=db.backref('quizzes', lazy=True))


# -------------------
# Question model
# -------------------
class Question(db.Model):
    """
    Represents a question under a specific Quiz.
    """
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255))
    option2 = db.Column(db.String(255))
    option3 = db.Column(db.String(255))
    option4 = db.Column(db.String(255))
    correct_answer = db.Column(db.String(255))

    quiz = db.relationship('Quiz', backref=db.backref('questions', lazy=True))


# -------------------
# Score model
# -------------------
class Score(db.Model):
    """
    Stores details of a user's quiz attempt.
    """
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime)
    total_scored = db.Column(db.Integer)

    quiz = db.relationship('Quiz', backref=db.backref('scores', lazy=True))
    user = db.relationship('User', backref=db.backref('scores', lazy=True))
