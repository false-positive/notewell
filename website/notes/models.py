from typing import Text
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

# Just a friendly reminder to makemigrations and migrate after changing this file :)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        # enforcing that there can not be two categories under a parent with same slug
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"

    def get_full_path(self):
        full_path = [self.slug]
        k = self.parent
        while k is not None:
            full_path.append(k.slug)
            k = k.parent
        return '/'.join(full_path[::-1])

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' / '.join(full_path[::-1])


class Note(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Name of Note'), max_length=64)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
