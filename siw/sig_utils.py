# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
import os
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from amm.models.mixins import AnnoFormativo


def response_debug(response):
    print('\nresponse :', response)
    print('\ncontent : ', response.content)
    print('\nurl match : ', response.resolver_match)
    for template in response.templates:
        print('\n template : ', template.name)


def from_human_to_computer_bytesize(size):
    units = {"B": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3, "TB": 1024 ** 4}
    
    number, unit = [string.strip().upper() for string in size.split()]
    return int(float(number) * units[unit])


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def get_total_directory_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def from_choices_to_list(choices):
    """
    Data le choices di un modello riporta in formato lista per esportazione in Json
    :param choices: Le scelte come le ho impostate nel modello.
    :return: La sorgente Json da riportare per il controllo ComboBox.
    """
    choices_list = list()
    for choice in choices:
        stato = dict()
        stato['id'] = choice[0]
        stato['descrizione'] = choice[1]
        choices_list.append(stato)
    return JsonResponse(choices_list, safe=False)


def get_anno_formativo(request):
    return get_object_or_404(AnnoFormativo, pk=request.session['anno_formativo_pk'])


def set_anno_formativo_default(request):
    if 'anno_formativo' not in request.session:
        anno_formativo_obj = AnnoFormativo.objects.get(default=True)
        request.session['anno_formativo'] = anno_formativo_obj.anno_formativo
        request.session['anno_formativo_pk'] = anno_formativo_obj.pk
