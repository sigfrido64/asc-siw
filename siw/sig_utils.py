# coding=utf-8
import os


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

