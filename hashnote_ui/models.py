from django.db import models
from singleton_models.models import SingletonModel

class HashNote(models.Model):
    """
    Simple representation of a hash note. Content is the value of the 
    note and created_at is the datetime at which the note was created in UTC
    """
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField('date created')

    def __unicode__(self):
        return self.content

class Filter(SingletonModel):
    """
    Stores the last filter term. This is important because the filter
    should not be reset if the user initiates another action (such as adding
    a new hashnote). This is a singleton model so any calls to save() will
    overwrite the existing record.
    """
    term = models.CharField(max_length=200)

    def __unicode__(self):
        return self.term
