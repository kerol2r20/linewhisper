from django.db import models


class Account(models.Model):
    nickname = models.CharField(max_length=200)
    token = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    mid = models.CharField(max_length=200)
