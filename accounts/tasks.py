# coding=utf-8
from __future__ import absolute_import, unicode_literals
import string
import os
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery import shared_task
from siw.sig_utils import get_immediate_subdirectories, get_total_directory_size, from_human_to_computer_bytesize


@shared_task
def check_work_directory(start_path='.', minimun_warning_size='100M'):
    """
    Data una directory mi riporta la lista delle directory in essa contenute e la relativa dimensione.

    """
    directory_list = get_immediate_subdirectories(start_path)
    min_size = from_human_to_computer_bytesize(minimun_warning_size)
    warning_dict = dict()

    for directory in directory_list:
        size = get_total_directory_size(os.path.join(start_path, directory))
        if size > min_size:
            warning_dict[directory] = size
    return warning_dict
