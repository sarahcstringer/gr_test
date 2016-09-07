
from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import Course, User, Enrollment, UserStatus, connect_to_db, db, User
from datetime import datetime
from sqlalchemy import or_

# from flask import Blueprint, current_app

# uploader = Blueprint('uploader', __name__, template_folder='templates')

app = Flask(__name__)
app.secret_key = "ABC"

@app.template_filter('strftime')
def _jinja2_filter_datetime(date):
    # print date
    # print type(date)
    # date = dateutil.parser.parse(date)
    # native = date.replace(tzinfo=None)
    date = date.strftime('%b %d, %Y')
    # format='%b %d, %Y'
    return date 

# uploader.jinja_env.filters['datetime'] = format_datetime

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/view_stuff')
def view_stuff():
    courses = Course.query.all()
    instructors = Enrollment.query.filter_by(participant_status='INST').all()
    instructors = sorted(set(instructor.participant for instructor in instructors))
    # print instructors[0].first_name

    return render_template('view_stuff.html', courses=courses, instructors=instructors)

@app.route('/view_instructor/<inst_id>')
def view_instructor(inst_id):

    instructor = User.query.get(inst_id)
    courses = Enrollment.query.filter_by(participant_id=inst_id).all()


    return render_template('view_instructor.html', instructor=instructor, courses=courses)

@app.route('/view_course/<course_id>')
def view_course(course_id):

    course = Course.query.get(course_id)
    instructor = Enrollment.query.filter_by(course_id=course_id, participant_status='INST').first().participant

    return render_template('view_course.html', course=course, instructor=instructor)

@app.route('/update_instructors', methods=['POST'])
def update_instructors():

    search_term = request.form.get('searchTerms')
    instructors = db.session.query(User.user_id, User.first_name, User.last_name).filter(or_(User.first_name.like('%'+search_term.upper()+'%'), User.last_name.like('%'+search_term.upper()+'%'))).all()

    return jsonify({'results': instructors})

@app.route('/login', methods=['POST'])
def log_in():

    email = request.form.get('email')
    password = request.form.get('password')
    print email
    print password

    try:
        user = User.query.filter_by(email=email, password=password).one()
        session['user'] = user.user_id
        session['user_fname'] = user.first_name
    except:
        pass

    return render_template('homepage.html')

if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()