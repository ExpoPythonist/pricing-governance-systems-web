from django import template
import re
import math
from user.models import Settings

register = template.Library()


# remove value with  space
@register.filter
def replace(value, search):
    return value.replace(search, " ")


# get dictionary value by key
@register.filter
def keyvalue(dict, key):
    return dict[key]


# sum two value
@register.filter
def data_sum(value, increment_value):
    return int(value) + int(increment_value)


# increment_one
@register.filter
def increment_one(value):
    return int(value) + 1


# remove -
@register.filter
def remove_minus(value):
    return abs(value)


@register.filter
def human_format(num):
    format_number = float(num)
    magnitude = 0
    if format_number > 9999:
        while abs(format_number) >= 1000:
            magnitude += 1
            format_number /= 1000.00
        # add more suffixes if you need them
        return '%.2f%s' % (format_number, ['', 'k', 'm', 'g', 't', 'p'][magnitude])
    else:
        return num



@register.filter
def millify(n):
    millnames = ['','K','M','B','T']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


@register.filter
def convert_volume(value):
    frm = "MT"
    settings = Settings.objects.filter()
    if settings.count() == 1:
        settings = settings.first()
        target = settings.volume
    else:
        target = "MT"

    if frm == target:
        return value
    elif frm == "MT":
        if target == "KG":
            return (value * 1000)
        elif target == "LB":
            return (value *  2204.623)

    return value

@register.filter
def get_default_volume(value):
    settings = Settings.objects.filter()
    if settings.count() == 1:
        settings = settings.first()
        return settings.volume
    else:
        return "MT"

