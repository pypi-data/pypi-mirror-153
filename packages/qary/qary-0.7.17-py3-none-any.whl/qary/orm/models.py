# import os

from django.db import models
# from django.conf import settings  # noqa

from qary.etl.fileutils import LARGE_FILES


class Title(models.Model):
    """ Document title for composing Wikipedia and other web searches

    >>> created, obj = Title.objects.get_or_create(text='this is a test, this is only a test')
    >>> created
    True
    """
    text = models.TextField(default='', null=True, help_text='Article title string')


def load_csv(path=LARGE_FILES['wikipedia-titles']['path']):
    """ Load the wikipidia titles CSV into the Title database table """
    pass
