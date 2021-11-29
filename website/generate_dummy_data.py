"""
A utility to generate dummy data.

Most of the generation is hardcoded,
you might want to change quantities
and probabilities

Note that the preferred way of populating the
database on development reset is by running:

    $ python manage.py loaddata fixtures/*.json

"""

import codecs
import random

from django.contrib.auth.models import User
from faker import Faker

from notes.models import BulletPoint, Category, Note, SharedItem

faker = Faker()


# Stats
total_bulletpoints = 0
total_categories = 0
total_notes = 0
total_shareditems = 0
total_users = 0


def create_categories(num_categories):
    # XXX: this is outdated and probably doesn't work
    global total_categories
    categories = []
    for _ in range(num_categories):
        name = faker.unique.word().title()
        parent = random.choice(
            categories) if categories and random.random() < 0.75 else None
        category = Category.objects.create(name=name, parent=parent)
        categories.append(category)
    total_categories += num_categories
    return categories


def create_bulletpoints(note, num_bulletpoints):
    global total_bulletpoints
    bulletpoints = []
    for _ in range(num_bulletpoints):
        parent = random.choice(
            bulletpoints) if bulletpoints and random.random() < 0.5 else None
        content = faker.text(256)
        bulletpoint = BulletPoint.objects.create(
            parent=parent,
            note=note,
            content=content,
            order_id=1337  # TODO: figure out the order_id thing
        )
        bulletpoints.append(bulletpoint)
    total_bulletpoints += num_bulletpoints


def create_notes(
    author,
    num_notes,
    min_bulletpoints_per_note,
    max_bulletpoints_per_note,
    category_choices=(),
    shareditem__user_choices=(),

):
    global total_shareditems, total_notes
    for _ in range(num_notes):
        title = faker.text(30)
        num_categories = min(len(category_choices), random.randint(0, 3))
        categories = random.choices(category_choices, k=num_categories)
        note = Note.objects.create(author=author, title=title)
        note.categories.set(categories)

        num_shareditems = random.randint(-7, 4)
        if num_shareditems > 0:
            num_users = min(len(shareditem__user_choices), num_shareditems)
            users = random.choices(shareditem__user_choices, k=num_users)
            for user in users:
                perm_level = random.choice(SharedItem.PERM_LEVEL_CHOICES)[0]
                SharedItem.objects.create(
                    user=user, perm_level=perm_level, note=note
                )
            total_shareditems += num_shareditems

        num_bulletpoints = random.randint(
            min_bulletpoints_per_note, max_bulletpoints_per_note)
        create_bulletpoints(note, num_bulletpoints)
    total_notes += num_notes


def generate_user_data(
    num_users,
    min_notes_per_user,
    max_notes_per_user,
    min_bulletpoints_per_note,
    max_bulletpoints_per_note,
    note_category_choices=()
):
    global total_users
    users = []
    for _ in range(num_users):
        # XXX: techincally the profile cannot be unique 😬
        profile = faker.profile()
        username = profile['username']
        email = profile['mail'] if random.random() < 0.75 else None
        password = codecs.decode('lqqnqrzrtanup', 'rot13')[::-1]
        user = User.objects.create_user(username, email, password)

        if random.random() < 0.57:
            user.first_name, user.last_name = profile['name'].rsplit(' ', 1)
            user.save()

        num_notes = random.randint(
            min_bulletpoints_per_note, max_bulletpoints_per_note
        )
        create_notes(
            user,
            num_notes,
            min_bulletpoints_per_note,
            max_bulletpoints_per_note,
            note_category_choices,
            shareditem__user_choices=users,
        )

        users.append(user)
    total_users += num_users


def main():
    categories = create_categories(num_categories=35)
    generate_user_data(
        num_users=100,
        max_notes_per_user=10,
        min_notes_per_user=5,
        min_bulletpoints_per_note=10,
        max_bulletpoints_per_note=24,
        note_category_choices=categories,
    )

    print('Created:')
    print(total_bulletpoints, 'BulletPoints')
    print(total_categories, 'Categories')
    print(total_notes, 'Notes')
    print(total_shareditems, 'SharedItems')
    print(total_users, 'Users')


if __name__ == "__main__":
    main()
