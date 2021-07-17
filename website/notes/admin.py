from django.contrib import admin
from django.forms import Textarea
from django.db import models as mdl

from . import models


class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 0
    formfield_overrides = {
        mdl.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'note')
    formfield_overrides = {
        mdl.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("name",)}


class BulletPointInline(admin.TabularInline):
    model = models.BulletPoint
    extra = 0
    formfield_overrides = {
        mdl.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }


class BulletPointAdmin(admin.ModelAdmin):
    inlines = [BulletPointInline]
    list_display = ('content', 'note', 'order_id', 'parent')
    formfield_overrides = {
        mdl.TextField: {'widget': Textarea(attrs={'rows': 3})},
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


class NoteAdmin(admin.ModelAdmin):
    inlines = [BulletPointInline, CommentInline]
    list_display = ('title',)


admin.site.register(models.Note, NoteAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.BulletPoint, BulletPointAdmin)
# admin.site.register(models.Quiz, QuizAdmin)
# admin.site.register(models.Question, QuestionAdmin)
# admin.site.register(models.Choice)
