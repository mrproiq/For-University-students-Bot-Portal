from django.db import models
from users.models import Student
# Create your models here.

class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    level = models.IntegerField(choices=[(1, "1-kurs"), (2, "2-kurs"), (3, "3-kurs"), (4, "4-kurs")])

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    WEEK_DAYS = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]


    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('users.Teacher', on_delete=models.SET_NULL, null=True)
    week_day = models.CharField(max_length=20, choices=WEEK_DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=20)

    class Meta:
        db_table = 'schedule'

    def __str__(self):
        return f"{self.group} - {self.subject} {self.WEEK_DAYS}"

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE )
    score = models.IntegerField()

    def __str__(self):
        return f"{self.student.user.first_name} - {self.subject.name}: {self.score}"