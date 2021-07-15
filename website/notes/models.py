import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

# Just a friendly reminder to makemigrations and migrate after changing this file :)

class Note(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Name of Note'), max_length=64)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
