"""
https://medium.com/@adriennedomingus/soft-deletion-in-django-e4882581c340
The delete method means that whenever you call .delete() on any object that inherits from the
SoftDeletionModel, it won’t actually be deleted from the database — its deleted_at attribute will
be set instead

hard_delete gives you the option to really truly delete something from the database if you want to,
but is named something other than the usual delete methods to ensure that you have to think about
what you’re doing before you do it, and actually mean to do it. This usually won’t be exposed to
users, but could only be called by developers from the shell.

The pieces:
    * delete — bulk deleting a QuerySet bypasses an individual object’s delete method, which is why this is needed here as well
    * alive and dead are just helpers — you may find you don’t need them.
    * hard_delete, as above, actually removes the objects from your database, but does this on a QuerySet instead of an individual object
"""
import datetime

now = datetime.datetime.now()
from django.db import models
from django.db.models.query import QuerySet


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=now)

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = now
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()
