from datacenter.duration_calculate import is_visit_long, format_duration

from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime


def get_duration_who_in_storage_now(visit):
    if visit:
        duration = localtime() - visit
        return duration.total_seconds()
    else:
        return


def storage_information_view(request):
    visits = Visit.objects.order_by("entered_at").filter(leaved_at=None)
    non_closed_visits = []
    for visit in visits:
        duration_secs = get_duration_who_in_storage_now(visit.entered_at)
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
