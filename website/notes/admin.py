from django.contrib import admin

from . import models


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'note')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("name",)}


admin.site.register(models.Note)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Category, CategoryAdmin)
