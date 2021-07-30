from django.contrib import admin
from django.forms import Textarea
from django.db import models
from django.shortcuts import reverse
from django.utils.html import format_html

from .models import Comment, BulletPoint, Note, Category, SharedItem


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'note')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("name",)}


class BulletPointInline(admin.TabularInline):
    model = BulletPoint
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }


@admin.register(BulletPoint)
class BulletPointAdmin(admin.ModelAdmin):
    inlines = [BulletPointInline]
    list_display = ('content', 'note', 'order_id', 'parent')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }


# class ChoiceInline(admin.TabularInline):
#     model = models.Choice
#     extra = 0


# class QuestionInline(admin.TabularInline):
#     fields = ['question_text']
#     model = models.Question
#     extra = 0


# class QuestionAdmin(admin.ModelAdmin):
#     # list_display = ('note', 'creation_date')
#     inlines = [ChoiceInline]


# class QuizInline(admin.StackedInline):
#     model = models.Quiz
#     extra = 0


# class QuizAdmin(admin.ModelAdmin):
#     list_display = ('note', 'creation_date')
#     inlines = [QuestionInline]
#     formfield_overrides = {
#         mdl.TextField: {'widget': Textarea(attrs={'rows': 3})},
#     }


# admin.site.register(models.Quiz, QuizAdmin)
# admin.site.register(models.Question, QuestionAdmin)
# admin.site.register(models.Choice)


class SharedItemInline(admin.TabularInline):
    model = SharedItem
    extra = 0


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    inlines = [BulletPointInline, CommentInline, SharedItemInline]
    list_display = ['title', 'author', 'uuid_link']

    @admin.display(ordering='uuid', description='UUID')
    def uuid_link(self, note):
        url = reverse('notes:read', kwargs={'note_id': note.uuid})

        fmt = '<a href="{}" target="_blank">{}</a>'
        return format_html(fmt, url, note.uuid)
