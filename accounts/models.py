from django.db import models


class Guest(models.Model):
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email