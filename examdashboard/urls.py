"""
URL configuration for examdashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views
from examquestions import views as examquestionsview

urlpatterns = [
    #re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    #re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('reg',views.reg,name='reg'),
    path('reg/user',views.regUser,name="reg-user"),
    path('login',views.login,name="login"),
    path('login/user',views.loginUser,name="login-user"),
    path('otp/user/<user_id>',views.otp_verification_page,name="otp-user"),
    path('otp/user/verify/',views.otp_verify,name="otp-user-verify"),
    path('change/mobile/number/<user_id>',views.change_number,name="otp-user-verify"),
    path('exam-list',examquestionsview.exam_list,name="exam-list"),
    path('exam-details/<id>',examquestionsview.exam_details,name="exam_details"),
    path('views_exam_details/<id>',examquestionsview.views_exam_details,name="views_exam_details"),
    path('start-exam',examquestionsview.startexam,name="exam-start"),
    path('get_next_question',examquestionsview.get_next_question,name="exam-start"),
    path('save_next',examquestionsview.save_next,name="save_next"),
    path('result_page/<id>',examquestionsview.result_page,name="result_page"),
    path('',views.home,name="home"),
    path('admin/', admin.site.urls),
]
