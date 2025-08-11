from django.db import models
from schedules.models import Group
# Create your models here.


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group)

    class Meta:
        db_table = 'announcement'

    def __str__(self):
        return self.title
