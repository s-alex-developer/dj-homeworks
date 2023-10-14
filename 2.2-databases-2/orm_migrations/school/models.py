from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    subject = models.CharField(max_length=30, verbose_name='Предмет')

    class Meta:
        verbose_name = 'Преподавателя'
        verbose_name_plural = 'Преподаватели'
        ordering = ['name']

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    group = models.CharField(max_length=30, verbose_name='Класс')

    class Meta:
        verbose_name = 'Ученика'
        verbose_name_plural = 'Ученики'
        ordering = ['name']

    def __str__(self):
        return self.name


class StudentTeacher(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='students_teachers',
                                verbose_name='Студент')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='students_teachers', verbose_name='')

    class Meta:
        verbose_name = 'Учителя'
        verbose_name_plural = 'Преподаватели ученика:'
        db_table = 'school_student_teacher'

    def __str__(self):
        return ''

