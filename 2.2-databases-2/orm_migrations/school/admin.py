from django.contrib import admin

from .models import Student, Teacher, StudentTeacher


class StudentTeacherInLine(admin.TabularInline):
    model = StudentTeacher
    extra = 1


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group']
    inlines = [StudentTeacherInLine, ]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject']


