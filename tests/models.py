from django.db import models


class Contact(models.Model):

    first_name = models.CharField(max_length=32, null=False, blank=False)
    last_name = models.CharField(max_length=32, null=False, blank=False)
    url = models.URLField(null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    bio = models.TextField(null=False, blank=False)
    birthday = models.DateField(null=False, blank=False)
