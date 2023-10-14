from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Article, Scope, Tag


class ScopeInLineFormset(BaseInlineFormSet):
    def clean(self):

        count = 0

        for form in self.forms:

            if form.cleaned_data.get('is_main'):
                count += 1

            if count > 1:
                raise ValidationError('Вы не можете указать несколько основных разделов.')

        if count == 0:
            raise ValidationError('Необходимо указать основной раздел.')

        return super().clean()  # вызываем базовый код переопределяемого метода


class ScopeInLine(admin.TabularInline):
    model = Scope
    formset = ScopeInLineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInLine, ]
    list_display = ['id', 'title', 'text', 'published_at', 'image']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # inlines = [ScopeInLine, ]
    list_display = ['id', 'name']

