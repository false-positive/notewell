import uuid

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

# Just a friendly reminder to makemigrations and migrate after changing this :)

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    full_path = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=False)
        if not self.slug:
            raise ValueError('Name cannot be slugified')

        full_path = [self.slug]
        k = self.parent
        while k is not None:
            full_path.append(k.slug)
            k = k.parent

        self.full_path = '/'.join(full_path[::-1])

        super(Category, self).save(*args, **kwargs)


# class Category(models.Model):
#     name = models.CharField(max_length=256)
#     slug = models.SlugField()
#     full_path = models.CharField(max_length=255)
#     parent = models.ForeignKey(
#         'self',
#         blank=True,
#         null=True,
#         related_name='children',
#         on_delete=models.CASCADE
#     )

#     class Meta:
#         # enforcing that there can not be two categories under a parent with
#         # same slug
#         unique_together = ('slug', 'parent',)
#         verbose_name_plural = "categories"

#

#     def get_full_path(self):
#         full_path = [self.slug]
#         k = self.parent
#         while k is not None:
#             full_path.append(k.slug)
#             k = k.parent
#         return '/'.join(full_path[::-1])


class NoteQuerySet(models.QuerySet):
    def filter_accessible_notes_by(self, user_pk):
        return self.filter(
            Q(author__pk=user_pk) | Q(shareditem__user__pk=user_pk)
        ).distinct()  # For some reason, notes in the QS were repeating


class Note(models.Model):

    PUBLIC = 'public'
    PRIVATE = 'private'

    NOTE_STATUS_CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    )

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=64)
    categories = models.ManyToManyField(Category, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10,
                              choices=NOTE_STATUS_CHOICES,
                              default=PRIVATE)
    verified = models.BooleanField(default=False)

    objects = NoteQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse("notes:read", kwargs={"note_id": self.uuid})

    def can_be_read_by(self, user: User) -> bool:
        if user == self.author:
            return True
        if self.shareditem_set \
                .filter(
                    user=user,
                    perm_level__in=(SharedItem.PERM_LEVEL_READ,
                                    SharedItem.PERM_LEVEL_EDIT),
                ).first():
            return True
        return False

    def can_be_edited_by(self, user: User) -> bool:
        if user == self.author:
            return True
        if self.shareditem_set \
                .filter(
                    user=user,
                    perm_level=SharedItem.PERM_LEVEL_EDIT,
                ).first():
            return True
        return False

    def __str__(self):
        return self.title


class SharedItem(models.Model):
    PERM_LEVEL_READ = 'R'
    PERM_LEVEL_EDIT = 'W'
    PERM_LEVEL_CHOICES = [
        (PERM_LEVEL_READ, 'Viewer'),
        (PERM_LEVEL_EDIT, 'Editor'),
    ]

    perm_level = models.CharField(
        _('Permission Level'), max_length=1,
        choices=PERM_LEVEL_CHOICES, default=PERM_LEVEL_READ
    )
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.note} - {self.user} ({self.perm_level})'


class BulletPoint(models.Model):
    content = models.TextField()
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    order_id = models.IntegerField()

    def __str__(self):
        return self.content


class Comment(models.Model):
    content = models.TextField()
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


# class Quiz(models.Model):
#     creation_date = models.DateField()
#     note = models.ForeignKey(Note, on_delete=models.CASCADE)

#     def __str__(self):
#         return 'Quiz'


# class Choice(models.Model):
#     choice = models.CharField(_("Choice"), max_length=256)
#     question = models.ForeignKey('Question', on_delete=models.CASCADE)


# class Question(models.Model):
#     question_text = models.CharField(_("Question"), max_length=256)
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
#     correct_answer = models.OneToOneField(
#         Choice, on_delete=models.CASCADE, blank=True, null=True)
