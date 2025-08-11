from django.urls import path
from .views import (RegisterUserView,
                    RegisterStudentView,
                    RegisterEmployeeView,
                    RegisterTeacherView)

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('register/student/', RegisterStudentView.as_view()),
    path('register/employee/', RegisterEmployeeView.as_view()),
    path('register/teacher/', RegisterTeacherView.as_view()),
]