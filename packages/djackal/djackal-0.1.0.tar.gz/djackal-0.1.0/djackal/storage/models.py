from django.db import models

from djackal.shortcuts import get_object_or


class Storage(models.Model):
    key = models.CharField(primary_key=True, max_length=150)
    value = models.TextField()

    @classmethod
    def set(cls, key, value):
        val = cls.get(key)
        if val is None:
            val = cls(key=key)
        val.value = value
        val.save()
        return val

    @classmethod
    def get(cls, key, default=None, f=None):
        val = get_object_or(cls, this=default, key=key)
        if f:
            val = f(val)
        return val

    @classmethod
    def remove(cls, key):
        cls.objects.filter(key=key).delete()

