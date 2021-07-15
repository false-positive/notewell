from django.contrib import admin

from . import models


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'note')

admin.site.register(models.Note)
admin.site.register(models.Comment, CommentAdmin)
