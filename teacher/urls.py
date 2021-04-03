from django.urls import path
from teacher.views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    path('add_teacher/', NewTeacher.as_view(), name='add_teacher'),
    path('add_subject/', NewSubject.as_view(), name='add_subject'),
    path('upload-csv/', teacher_upload, name="teacher_upload"),
    path('teacher/<int:pk>', TeacherDetailView.as_view(), name="TeacherDetailView"),
    path('', TeacherListView.as_view(), name="TeacherListView"),
]
