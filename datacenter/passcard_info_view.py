import datetime

from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def get_duration(visit):
    duration_secs = visit.leaved_at - visit.entered_at
    return duration_secs.seconds


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


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.filter(visit__passcard__passcode=passcode)
    visits = Visit.objects.filter(passcard__passcode=passcode)
    this_passcard_visits = []
    for visit in visits:
        if visit.leaved_at:
            is_strange = is_visit_long(visit, minutes=60)
            if type(visit.entered_at) == datetime.datetime:
                duration_secs = get_duration(visit)
                duration_formated, _ = format_duration(duration_secs)
                this_passcard_visits.append(
                    {
                        'entered_at': visit.entered_at,
                        'duration': duration_formated,
                        'is_strange': is_strange
                    },
                )
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
