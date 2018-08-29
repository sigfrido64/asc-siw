# coding=utf-8


def response_debug(response):
    print('\nresponse :', response)
    print('\ncontent : ', response.content)
    print('\nurl match : ', response.resolver_match)
    for template in response.templates:
        print('\n template : ', template.name)
