import os
from random import randrange

from flask import Blueprint, make_response, render_template, request, session, redirect, url_for
from flask_restful import Resource

from App.model import db, Student, Users, Grades, Course, is_login
from utils.exits_init import api

user_blue = Blueprint('user', __name__)


@user_blue.route('/')
def set_cookie():
    tem = render_template('cookie.html')
    res = make_response(tem)
    res.set_cookie('ticket', '1312123', max_age=10)
    return res


@user_blue.route('/delcookie')
def del_cookie():
    tem = render_template('/user/cookie.html')
    res = make_response(tem)
    res.delete_cookie('ticket')
    return res


@user_blue.route('/create_db/')
def create_db():
    db.create_all()
    return '创建成功'


@user_blue.route('/drop_db')
def drop_db():
    db.drop_all()
    return '删除成功'


@user_blue.route('/create_student')
def create_student():
    stu = Student(s_name="小美", s_age=20)
    db.session.add(stu)
    db.session.commit()

    return '添加成功'


@user_blue.route('/select_stu', methods=['GET'])
def select_stu():
    # stus = Student.query.filter(Student.s_name == '小美').all()
    stu = Student.query.filter_by(s_name='小白').first()
    stu.s_name = '小黑'
    db.session.add(stu)
    db.session.commit()
    return render_template('student.html', stu=stu)


@user_blue.route('/delete', methods=['GET'])
def delete_student():
    stu = Student.query.filter(Student.s_name == '大锤')
    db.session.delete(stu)
    db.session.commit()
    return '删除成功'


@user_blue.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('/user/user_login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(u_name=username, u_pwd=password).first()
        if not user:
            return render_template('/user/user_login.html', msg='用户或密码错误')
        session['u_id'] = user.u_id
        return redirect(url_for('user.select_all_student'))


@user_blue.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('/user/user_register.html')
    if request.method == 'POST':
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        media_url = os.path.join(os.path.join(BASE_DIR, 'static'), 'media')
        u_name = request.form.get('username')
        u_email = request.form.get('email')
        u_pwd = request.form.get('password')
        u_icon = request.files.get('icon')
        u_icon.save(os.path.join(media_url, u_icon.filename))
        u_auater = '/static/media/' + u_icon.filename
        user = Users(u_name=u_name, u_email=u_email, u_pwd=u_pwd, u_icon=u_auater)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))


@user_blue.route('/logout/')
def logout():
    session.pop('u_id', None)
    return render_template('/user/user_login.html')


@user_blue.route('/create_many/')
def create_many():
    stus = []
    for _ in range(10):
        s_name = '大锤%s' % (randrange(1000))
        s_age = '%d' % (randrange(28))
        stu = Student(s_name=s_name, s_age=s_age)
        stus.append(stu)

    db.session.add_all(stus)
    db.session.commit()
    return '创建成功'


@user_blue.route('/create_grades/')
def create_grades():
    grades = []
    name = {'通信工程': '拉电缆', '电信工程': '烧电焊', '自动化': '发电', '车辆工程': '修车', '小学教育': '弄小朋友'}
    for k, v in name.items():
        grade = Grades(g_name=k, g_desc=v)
        grades.append(grade)

    db.session.add_all(grades)
    db.session.commit()
    return '创建成功'


@user_blue.route('/select_grade/')
@is_login
def select_grade():
    grades = Grades.query.order_by('g_id')
    return render_template('grades.html', grades=grades)


@user_blue.route('/add_student_by_grade/', methods=['GET', 'POST'])
def add_student_by_grade():
    if request.method == 'GET':
        g_id = request.args.get('g_id')
        return render_template('edit.html', g_id=g_id)
    if request.method == 'POST':
        g_id = request.form.get('g_id')
        s_name = request.form.get('s_name')
        s_age = request.form.get('s_age')
        stu = Student(s_name=s_name, s_age=s_age, grade_id=g_id)
        db.session.add(stu)
        db.session.commit()
        return redirect(url_for('user.select_grade'))


@user_blue.route('/select_student_by_grade/')
def select_student_by_grade():
    page = request.args.get('page', 1)
    g_id = request.args.get('g_id')
    paginate = Student.query.filter_by(grade_id=g_id).paginate(page, 10)
    students = paginate.items
    if students == []:
        return render_template('none.html', msg='该班级暂时没有学生')
    grade = students[0].grades.g_name
    return render_template('student.html', grade=grade, stus=students, paginate=paginate)


@user_blue.route('/select_all_student/', methods=['GET'])
def select_all_student():
    page = int(request.args.get('page', 1))
    paginate = Student.query.paginate(page, 2)
    stus = paginate.items

    return render_template('student.html', stus=stus, paginate=paginate)


@user_blue.route('/edit_student/', methods=['GET', 'POST'])
@is_login
def edit():
    if request.method == 'GET':
        return render_template('edit.html')
    if request.method == 'POST':
        s_id = request.args.get('id')
        s_name = request.form.get('s_name')
        s_age = request.form.get('s_age')
        stu = Student.query.filter_by(s_id=s_id).first()
        stu.s_name = s_name
        stu.s_age = s_age
        db.session.add(stu)
        db.session.commit()
        return redirect(url_for('user.select_all_student'))


@user_blue.route('/delete_student/')
@is_login
def delete():
    s_id = request.args.get('id')
    student = Student.query.get(s_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('user.select_all_student'))


@user_blue.route('/delete_grade/')
def delete_grade():
    g_id = request.args.get('g_id')
    grade = Grades.query.get(g_id)
    db.session.delete(grade)
    db.session.commit()
    return redirect(url_for('user.select_grade'))


@user_blue.route('/create_course/')
def create_course():
    course = ['线性代数', '模拟电路', '数字电路', '计算机基础', '汽车理论', '通信原理']
    course_list = []
    for c_name in course:
        course = Course(c_name=c_name)
        course_list.append(course)
    db.session.add_all(course_list)
    db.session.commit()
    return '添加成功'


@user_blue.route('/choice_course/', methods=['GET', 'POST'])
def choice_course():
    if request.method == 'GET':
        courses = Course.query.all()
        return render_template('choice_course.html', courses=courses)
    if request.method == 'POST':
        s_id = request.args.get('id')
        student = Student.query.get(s_id)
        c_id = request.form.get('c_id')
        course = Course.query.get(c_id)
        course.sc.append(student)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('user.select_all_student'))


class CourseApi(Resource):

    def get(self):
        courses = Course.query.all()
        return [course.to_dict() for course in courses]

    def post(self, id):
        s_id = request.args.get('id')
        student = Student.query.get(s_id)
        c_id = request.form.get('c_id')
        course = Course.query.get(c_id)
        course.sc.append(student)
        db.session.add(course)
        db.session.commit()


api.add_resource(CourseApi, '/api/choice_courses/')

