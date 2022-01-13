import datetime

from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime


def get_duration(visit):
    if type(visit) == datetime.datetime:
        duration = localtime() - visit
        return duration.seconds
    else:
        return


def format_duration(duration):
    hours, remainder_secs = divmod(duration, 3600)
    minutes, seconds = divmod(remainder_secs, 60)
    duration_min = duration // 60
    duration_formated = '{:02} часов {:02} минут {:02} секунд'.format(
        int(hours),
        int(minutes),
        int(seconds),
    )
    return duration_formated, duration_min


def is_visit_long(visit, minutes=60):
    if visit.leaved_at:
        duration_secs = visit.leaved_at - visit.entered_at
        _, duration = format_duration(duration_secs.seconds)
        if duration < minutes:
            return False


def storage_information_view(request):
    visits = Visit.objects.order_by("entered_at")
    non_closed_visits = []
    for visit in visits:
        is_visit_long(visit, minutes=60)
        if not visit.leaved_at:
            duration_secs = get_duration(visit.entered_at)
            if duration_secs:
                duration_formated, _ = format_duration(duration_secs)
                non_closed_visits.append({
                    'who_entered': visit.passcard.owner_name,
                    'entered_at': visit.entered_at,
                    'duration': duration_formated,

                }
                )
    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }

    return render(request, 'storage_information.html', context)
