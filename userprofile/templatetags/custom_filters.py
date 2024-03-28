from django import template
from django.utils import timezone


register = template.Library()

@register.filter
def timesince_custom(post_datetime):
    local_pdatetime = timezone.localtime(post_datetime)
    date_now = timezone.localtime(timezone.now())
    difference_seconds = (date_now - local_pdatetime).total_seconds()
    print(date_now, local_pdatetime)
    if 1 < difference_seconds < 59:
        return f"{int(difference_seconds)}s"
    elif difference_seconds < 59 * 60:
        remain_minutes = int(difference_seconds // 60)
        return f"{remain_minutes}m"
    elif difference_seconds < 24 * 3600:
        remain_hours = int(difference_seconds // 3600)
        return f"{remain_hours}h"
    elif difference_seconds <= 100 * 24 * 60 * 60:
        remain_days = int(difference_seconds // 60 // 60 // 24)
        return f"{remain_days}d"
    else:
        return f'{local_pdatetime.year}-{local_pdatetime.month}-{local_pdatetime.day}'