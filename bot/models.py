from django.db import models


class Account(models.Model):
    nickname = models.charField(max_length=200)
    token = models.charField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.charField(max_length=200)
    mid = models.charField(max_length=200)
