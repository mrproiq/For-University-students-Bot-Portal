from django.contrib import admin
from .models import Student, Teacher, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
# Register your models here.

class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'is_employee', 'is_teacher')
    list_filter = ('is_staff', 'is_superuser', 'is_student', 'is_teacher', 'is_employee')
    ordering = ('email',)

    # formda ko‘rinadigan maydonlar
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Shaxsiy ma’lumotlar', {'fields': ('first_name', 'last_name')}),
        ('Ruxsatlar', {'fields': ('is_staff', 'is_superuser', 'is_active', 'is_student', 'is_teacher', 'is_employee')}),
        ('Muhim sanalar', {'fields': ('last_login',)}),
    )

    # Superuser yaratish formi uchun maydonlar
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    search_fields = ('email',)

admin.site.register(User, CustomUserAdmin)

User = get_user_model()

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user','birth_date', 'faculty', 'group', 'level', 'phone_number')
    list_filter = ('faculty', 'group', 'level')

    def formfield_for_foreignkey(self, db_field, request, **kwargs ):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(is_student=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree', 'subject', 'work_experience')
    search_fields = ('user__first_name', 'user__last_name', 'subject')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(is_teacher=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)







