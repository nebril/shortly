from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
import requests

from shorten.models import User


class Command(BaseCommand):
    help = 'Adds randomly generated users'

    def add_arguments(self, parser):
        parser.add_argument('user_count', type=int)

    def handle(self, *args, **options):
        user_count = options["user_count"]
        if user_count > 5000 or user_count < 1:
            raise CommandError("user_count needs to be between 1 and 5000")

        params = {
            "results": user_count,
            "inc": "name,login,email,registered"
        }
        r = requests.get('https://randomuser.me/api', params=params)

        if r.status_code != 200:
            raise CommandError(
                "request to {} failed with status code {}".format(
                    r.url, r.status_code))

        data = r.json()

        tz = timezone.get_current_timezone()
        for random_user in data["results"]:
            date = datetime.strptime(random_user["registered"],
                                     "%Y-%m-%d %H:%M:%S")
            date = timezone.make_aware(date, tz)
            u = User(
                username=random_user["login"]["username"],
                first_name=random_user["name"]["first"],
                last_name=random_user["name"]["last"],
                email=random_user["email"],
                password=random_user["login"]["sha256"],
                date_joined=date
            )
            u.save()

        self.stdout.write(self.style.SUCCESS(
            'Created {} users.'.format(data["info"]["results"])))
