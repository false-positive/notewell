from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from django.forms import Textarea
from django.db import models
from django.utils.html import format_html

from .models import Comment, Note, Category, SharedItem, Quiz


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
class CategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 20  # px
    exclude = ('full_path',)
    list_display = ('name', 'slug', 'full_path')
    prepopulated_fields = {'slug': ("name",)}
    # ordering = ('full_path',)


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
    autocomplete_fields = ['user']
    extra = 0


class QuizInline(admin.TabularInline):
    model = Quiz


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    inlines = [CommentInline, SharedItemInline, QuizInline]
    list_display = ['title', 'author', 'uuid_link', 'creation_date', 'status', 'verified']
    list_filter = ['status', 'verified']
    autocomplete_fields = ['author']
    actions = ['verify', 'unverify', 'share_with_admin']
    search_fields = ['title__icontains']

    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('categories')

    @admin.display(ordering='uuid', description='UUID')
    def uuid_link(self, note):
        url = note.get_absolute_url()

        fmt = '<a href="{}" target="_blank">{}</a>'
        return format_html(fmt, url, note.uuid)

    @admin.action(description='Verify')
    def verify(self, request, queryset):
        for note in queryset:
            note.verified = True
            note.save()

    @admin.action(description='Unverify')
    def unverify(self, request, queryset):
        for note in queryset:
            note.verified = False
            note.save()

    @admin.action(description='Give me read access yes')
    def share_with_admin(self, request, queryset):
        # XXX: kinda creepy...
        for note in queryset:
            if note.can_be_read_by(request.user):
                continue
            note.shareditem_set.create(
                perm_level=SharedItem.PERM_LEVEL_READ,
                user=request.user,
            )
