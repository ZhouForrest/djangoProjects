from django.contrib.auth.models import User
from django.core import paginator
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from app.models import Grades, Students
from day01.settings import PAGE_NUMBERS
from utils.function import is_login


@is_login
def index(request):

    return render(request, 'index.html')#根据请求渲染页面

@is_login
def head(request):
    user = request.user
    return render(request, 'head.html', {'user':user})

@is_login
def grade(request):
    grades = Grades.objects.all()
    page_num = request.GET.get('page_num', 1)#通过get请求拿page_num的值,如果没有默认值为1
    paginator = Paginator(grades, 3)#分页每页显示3条信息
    pages = paginator.page(int(page_num))#获取页码为page_num的所有信息
    ctx = {
        'pages':pages,
    }
    return render(request, 'grade.html', ctx)

@is_login
def left(request):
    return render(request, 'left.html')

@is_login
def head2(request):
    return render(request, 'head2.html')

@is_login
def addgrade(request):

    if request.method == 'GET':
        return render(request, 'addgrade.html')
    else:
        g_name = request.POST.get('grade_name')
        g = Grades()
        g.g_name = g_name
        g.save()
        return HttpResponseRedirect(reverse('app:grade'))

@is_login
def changepwd(request):

    return render(request, 'changepwd.html')

@is_login
def student(request):

    students = Students.objects.all()
    paginator = Paginator(students, PAGE_NUMBERS)
    page_num = request.GET.get('page_num', 1)
    pages = paginator.page(int(page_num))
    ctx = {
        'pages': pages,
    }
    return render(request, 'student.html', ctx)

@is_login
def main(request):

    return render(request, 'main.html')

@is_login
def addstu(request):
    if request.method == 'GET':
        pages = Grades.objects.all()
        return render(request, 'addstu.html', {'pages':pages})
    else:
        s_name = request.POST.get('s_name')#获取学生姓名
        g_id = request.POST.get('g_id')#获取所属班级
        grade = Grades.objects.filter(id=g_id).first()
        s_img = request.FILES.get('s_img')
        # grade = Grades.objects.get(id=g_id)
        stu = Students.objects.create(s_name=s_name, g_id=grade.id, s_img=s_img)
        stu.save()
        # Students.objects.create(s_name=s_name, g=grade)
        return HttpResponseRedirect(reverse('app:student'))

@is_login
def del_stu(request, id):

    # s_id = request.GET.get('id')
    Students.objects.get(id=id).delete()

    return HttpResponseRedirect(reverse('app:student'))

@is_login
def editgrade(request):
    if request.method == 'GET':
        grade_id = request.GET.get('grade_id')
        return render(request, 'addgrade.html', {'grade_id': grade_id})
    else:
        grade_id = request.POST.get('grade_id')
        grade_name = request.POST.get('grade_name')

        g = Grades.objects.filter(pk=grade_id).first()
        g.g_name = grade_name
        g.save()
        return HttpResponseRedirect(reverse('app:grade'))


# def select(request):
#
#     grade = Grades.objects.filter(g_name__contains='python').first()
#     stus = grade.students_set.all()#通过一找多
#     stu = stus.filter(s_language__gt=F('s_math')+10)#F处理数学运算
#     stu2 = stus.filter(Q(s_language__gt=80) | Q(s_math__lt=80))#Q处理关系运算


