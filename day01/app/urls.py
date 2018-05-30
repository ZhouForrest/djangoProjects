from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from app import views

urlpatterns = [
    # url(r'^index/', login_required(views.index), name='index'),#djanggo自带验证登录
    url(r'^index/', views.index, name='index'),
    url(r'^left/', views.left, name='left'),
    url(r'^grade/', views.grade, name='grade'),
    url(r'^head/', views.head, name='head'),
    url(r'^head2/', views.head2, name='head2'),
    url(r'^login/', views.head2, name='login'),
    url(r'^addgrade/', views.addgrade, name='addgrade'),
    url(r'^addstu/', views.addstu, name='addstu'),
    url(r'^changepwd/', views.changepwd, name='changepwd'),
    url(r'^main/', views.main, name='main'),
    url(r'^student/', views.student, name='student'),
    url(r'^del_stu/(?P<id>\d+)', views.del_stu, name='del_stu'),
    url(r'^editgrade/', views.editgrade, name='editgrade'),
    # url(r'^select/', views.select, name='select')

]