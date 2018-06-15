from datetime import datetime
from functools import wraps

from flask import session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    s_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_name = db.Column(db.String(16), unique=True)
    s_age = db.Column(db.Integer, default=1)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.g_id'), nullable=True)

    __tablename__ = "student"

    def to_dict(self):
        return {
        's_id': self.s_id,
        's_name': self.s_name,
        's_age': self.s_age,
        'grade_id':self.grade_id
        }


class Users(db.Model):
    u_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_name = db.Column(db.String(20), unique=True)
    u_pwd = db.Column(db.String(16))
    u_email = db.Column(db.String(64))
    u_icon = db.Column(db.String(200))


    __tablename__ = 'user'


class Grades(db.Model):
    g_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    g_name = db.Column(db.String(20))
    g_desc = db.Column(db.String(30), nullable=True)
    g_create_time = db.Column(db.DateTime, default=datetime.now)
    student = db.relationship('Student', backref='grades', lazy=True)

    def to_dict(self):
        return{
        'g_id': self.g_id,
        'g_name': self.g_name,
        'g_create_time': self.g_create_time.strftime('%Y-%m-%d'),
        'student': [student.to_dict() for student in self.student]
        }


sc = db.Table('sc',
              db.Column('s_id', db.Integer, db.ForeignKey('student.s_id'), primary_key=True),
              db.Column('c_id', db.Integer, db.ForeignKey('course.c_id'), primary_key=True))


class Course(db.Model):
    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_name = db.Column(db.String(20), unique=True)
    c_create_time = db.Column(db.DateTime, default=datetime.now)
    sc = db.relationship('Student', secondary=sc, backref=db.backref('course', lazy=True))

    __tablename__ = 'course'

    def to_dict(self):
        return {
            'c_id': self.c_id,
            'c_name': self.c_name,
            'c_create_time': self.c_create_time.strftime('%Y-%m-%d'),
            'sc': [student.to_dict() for student in self.sc]
            }


#functools.wraps 的作用是将原函数对象的指定属性复制给包装函数对象, 默认有 module、name、doc,或者通过参数选择。


def is_login(func):
    @wraps(func)
    def check_login():
        user_session = session.get('u_id')
        if user_session:
            return func()
        else:
            return redirect(url_for('user.login'))
    return check_login





