from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    # url(r'^userper/', views.userper, name='userper')
    #自行实现验证
    # url(r'^my_login/', views.my_login, name='my_login'),
    # url(r'^my_register/', views.my_register, name='my_register'),
    # url(r'^my_logout/', views.my_logout, name='my_logout'),
    ]