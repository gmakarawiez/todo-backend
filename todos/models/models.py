from django.db import models
from todos.models.base import Authentified
from backend import settings

# Create your models here.

#class ToDo(Authentified):
class ToDo(models.Model):

    class Meta:
        abstract=False

    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, null=False, blank=False, on_delete=models.CASCADE,
                               related_name="creator")
    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, null=True, blank=True, on_delete=models.CASCADE,
                               related_name="last_editor")
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    last_edited = models.DateTimeField(auto_now = True, auto_now_add = False)

    def __str__(self):
        return self.title
