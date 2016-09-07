from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(75), unique=True)
    password = db.Column(db.String(30))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    bio = db.Column(db.Text)

class Course(db.Model):

    __tablename__ = 'courses'

    course_id = db.Column(db.String(10), primary_key=True)
    course_title = db.Column(db.String(150))
    course_description = db.Column(db.Text)
    start_date = db.Column(db.DateTime(20))
    end_date = db.Column(db.DateTime(20))
    cap = db.Column(db.Integer)


# class CourseCategories(db.Model):

#     __tablename__ = 'course_cats'


# class MeetingSpace(db.Model):

#     __tablename__ = 'mtg_space'


class UserStatus(db.Model):

    __tablename__ = 'user_status'

    status_id = db.Column(db.String(5), primary_key=True)
    status_name = db.Column(db.String(20))

class Enrollment(db.Model):

    __tablename__ = 'enrollments'

    course_roster_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.String(10), db.ForeignKey('courses.course_id'))
    participant_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    participant_status = db.Column(db.String(5), db.ForeignKey('user_status.status_id'))

    participant = db.relationship('User', backref=db.backref('enrollments'))
    course = db.relationship('Course', backref=db.backref('enrollments'))


# Users:
# address
# phone(extra table?)


# Courses:
# course_id
# course_title
# course_description
# course_instructor
# start_date
# end_date


# Roster
# user_id
# course_id
# permission (Instructor, TA, Participant)

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///GhostRanch'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."