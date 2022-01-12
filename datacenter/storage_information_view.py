import datetime

from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime


def get_duration(visit):
    if type(visit) == datetime.datetime:
        duration = localtime() - visit
        return duration.seconds
    else:
        return None


def format_duration(duration):
    hours, remainder_secs = divmod(duration, 3600)
    minutes, seconds = divmod(remainder_secs, 60)
    return '{:02} часов {:02} минут {:02} секунд'.format(
        int(hours),
        int(minutes),
        int(seconds),
    )


def storage_information_view(request):

    visits = Visit.objects.all()
    non_closed_visits = []
    for visit in visits:
        if not visit.leaved_at:
            if type(visit.entered_at) == datetime.datetime:
                duration_secs = get_duration(visit.entered_at)
                if duration_secs:
                    duration = format_duration(duration_secs)
                    non_closed_visits.append({
                        'who_entered': visit.passcard.owner_name,
                        'entered_at': visit.entered_at,
                        'duration': duration,
                    }
                    )
    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }

    return render(request, 'storage_information.html', context)
