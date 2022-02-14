from django.db import models
from users.models import CustomUser
from backend import settings


class Authentified(models.Model):

    class Meta:
        abstract=True

    #author = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, null=False, blank=False, on_delete=models.CASCADE,
    #                           related_name="%(app_label)s_%(class)s_related")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, null=False, blank=False, on_delete=models.CASCADE,
                               related_name="creator")
    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, null=True, blank=True, on_delete=models.CASCADE,
                               related_name="last_editor")
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    last_edited = models.DateTimeField(auto_now = True, auto_now_add = False)