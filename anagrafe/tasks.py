import string
# Create your tasks here

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery import shared_task


@shared_task
def prova(total):
    for i in range(total):
        print("Sono alla : ", str(i))
    return 'Finito !'
