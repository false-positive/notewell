import re
import uuid

from django.db import models
from django.db.models import Q
from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey

# Just a friendly reminder to makemigrations and migrate after changing this :)


class Category(MPTTModel):
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    full_path = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=False)
        if not self.slug:
            raise ValueError('Name cannot be slugified')

        self.full_path = '/'.join(full_path[::-1])

        super().save(*args, **kwargs)


class NoteQuerySet(models.QuerySet):
    def filter_accessible_notes_by(self, user_pk=None):
        if not user_pk:
            return self.select_related('author') \
                .prefetch_related('categories') \
                .filter(status='public')
        else:
            return self.select_related('author') \
                .prefetch_related('categories') \
                .filter(
                    Q(author__pk=user_pk) | Q(shareditem__user__pk=user_pk) | Q(status='public')
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
    content = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10,
                              choices=NOTE_STATUS_CHOICES,
                              default=PRIVATE)
    verified = models.BooleanField(default=False)

    objects = NoteQuerySet.as_manager()

    class Meta:
        unique_together = ['title', 'author']

    def save(self, *args, **kwargs):
        """If name collides, add number at the end, so it doesn't

        Example:

        >>> Note.objects.create(author_id=1, title='N').title
        'N'
        >>> Note.objects.create(author_id=1, title='N').title
        'N 1'
        >>> Note.objects.create(author_id=1, title='N').title
        'N 2'
        >>> Note.objects.get(title='N 1').delete()
        (1, {'notes.Note': 1})
        >>> Note.objects.create(author_id=1, title='N').title
        'N 3'
        >>> Note.objects.create(author_id=1, title='N 3').title
        'N 4'
        >>> Note.objects.create(author_id=2, title='N').title
        'N'
        """
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            title = re.sub(r' \d+$', '', self.title)
            existing_titles = Note.objects \
                .filter(author=self.author) \
                .filter(title__regex=fr'^{title} \d+$') \
                .values_list('title', flat=True) \
                .order_by('title')
            nums = [int(t.split(' ')[-1]) for t in existing_titles]

            unused_num = max(nums) + 1 if nums else 1

            # Alternative approach:
            # Get the first natural number that isn't in list of nums
            # Solution from: https://stackoverflow.com/q/28176866
            # (yes, i understand how it works. don't @ me)
            # unused_num = next(i for i, e in enumerate(nums + [None], 1) if i != e)

            self.title = f'{title} {unused_num}'
            super().save(*args, **kwargs)

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

    class Meta:
        unique_together = ('note', 'user')

    def __str__(self):
        return f'{self.note} - {self.user} ({self.perm_level})'

    def save(self, *args, **kwargs):
        """Enforce uniqueness by deleting existing `SharedItems` before saving on collision."""
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            shareditem = SharedItem.objects.get(note=self.note, user=self.user)
            shareditem.delete()
            super().save(*args, **kwargs)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
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

class Quiz(models.Model):
    creation_date = models.DateField(null=True, auto_now_add=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    content = models.JSONField(null=True)

    def __str__(self):
        return self.note.title + "'s Quiz"