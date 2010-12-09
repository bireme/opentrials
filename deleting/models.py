from django.db import models
from django.db.models.query import QuerySet

class NotDeletedQuerySet(QuerySet):
    def delete(self):
        self.update(_deleted=True)

class NotDeletedManager(models.Manager):
    """
    Returns only objects with _deleted=False
    """
    def get_query_set(self):
        qs = NotDeletedQuerySet(self.model) #, using=self._db)

        return qs.filter(_deleted=False)

class DeletedQuerySet(QuerySet):
    def recover(self):
        self.update(_deleted=False)

class DeletedManager(models.Manager):
    """
    Returns only objects with _deleted=True
    """
    def get_query_set(self):
        qs = DeletedQuerySet(self.model) #, using=self._db)

        return qs.filter(_deleted=True)

    def recover(self):
        return self.get_query_set().recover()

class AllObjectsQuerySet(QuerySet):
    def delete(self):
        self.update(_deleted=True)

    def recover(self):
        self.update(_deleted=False)

class AllObjectsManager(DeletedManager):
    """
    Returns all objects not matters if _deleted or not
    """
    def get_query_set(self):
        return AllObjectsQuerySet(self.model) #, using=self._db)

class ControlledDeletion(models.Model):
    """
    This class implements the inheritance deletion functions to avoid real deletion
    and just set field '_deleted' as True
    """

    class Meta:
        abstract = True

    # Managers
    objects = NotDeletedManager()
    deleted_objects = DeletedManager()
    all_objects = AllObjectsManager()

    # Fields
    _deleted = models.BooleanField(default=False, blank=True, db_index=True, editable=False)

    def delete(self, *args, **kwargs):
        """
        Instead of delete the object, just changes field _deleted to True
        """
        self._deleted = True
        self.save()

    def recover(self, *args, **kwargs):
        """
        Sets _deleted to False to recover object
        """
        self._deleted = False
        self.save()

