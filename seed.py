from model import Course, User, UserStatus, Enrollment, connect_to_db, db
from server import app
import openpyxl
from datetime import datetime

def load_status():
    Enrollment.query.delete()
    User.query.delete()
    Course.query.delete()
    UserStatus.query.delete()

    inst = UserStatus(status_id='INST', status_name='instructor')
    part = UserStatus(status_id='PART', status_name='participant')

    db.session.add_all([inst, part])
    db.session.commit()

def load_courses():

    

    wb = openpyxl.load_workbook('2016WSCourses.xlsx')
    sheet = wb.get_sheet_by_name('Sheet1')

    # print sheet.rows()

    for row in sheet.rows[1:]:
        cap, cat, code, course_name, num, start, end, nights, status, short, desc_long, instructor, bio, rate, rate_desc = row
        
        if num.value:
            course = Course(course_id=num.value, course_title=course_name.value, course_description=desc_long.value,
                            start_date=start.value, end_date=end.value, cap=cap.value)
            db.session.add(course)
            db.session.commit()

        if instructor.value:
            first_name=instructor.value.split(' ')[0]
            last_name=' '.join(instructor.value.split(' ')[1:])

            try:
                instructor = User.query.filter_by(first_name=first_name, last_name=last_name).one()
                print 'found this instructor', instructor.first_name
            except:
                instructor=User(first_name=first_name, last_name=last_name, bio=bio.value)
                db.session.add(instructor)
                db.session.commit()

            enrollment = Enrollment(course_id=course.course_id, participant_id=instructor.user_id, participant_status='INST')
            db.session.add(enrollment)
            db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_status()
    load_courses()
