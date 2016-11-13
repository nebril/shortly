import hashlib
from random import randint

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.aggregates import Count

from shortly import settings


class UserManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class User(models.Model):
    objects = UserManager()

    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=64)
    date_joined = models.DateTimeField()

    def __str__(self):
        return "{} {} {}".format(self.first, self.last_name, self.username)


class Url(models.Model):
    original_url = models.CharField(max_length=2000)
    shortened_url = models.CharField(max_length=settings.SHORT_URL_MAX_LEN)
    user = models.ForeignKey(User)

    def __str__(self):
        return "{} => {}".format(self.original_url, self.shortened_url)

    @classmethod
    def new(cls, url):
        shortened = hashlib.md5(url).hexdigest()[:settings.SHORT_URL_MAX_LEN]

        try:
            model = cls.objects.get(shortened_url=shortened)
        except ObjectDoesNotExist:
            user = User.objects.random()
            model = cls(original_url=url, user=user, shortened_url=shortened)
            model.save()
        return model

    def build_full_url(self, request):
        return "http://{}/{}".format(request.META['HTTP_HOST'],
                                     self.shortened_url)
