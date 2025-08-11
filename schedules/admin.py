from django.contrib import admin
from .models import Faculty, Group, Subject, Schedule, Grade
# Register your models here.

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'level',)
    search_fields = ('name', 'faculty', 'level',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score',)
    list_filter = ['student', 'subject', 'score']
    search_fields = ['student', 'subject']

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('group', 'subject', 'teacher', 'week_day', 'start_time', 'end_time', 'room')
    list_filter = ('group', 'week_day', 'room',)
    search_fields = ('teacher__user__first_name', 'subject__name', 'room')

admin.site.register(Schedule, ScheduleAdmin)



