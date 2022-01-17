from datacenter.duration_calculate import is_visit_long, format_duration, get_duration

from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    visits = Visit.objects.filter(passcard__passcode=passcode)
    this_passcard_visits = []
    for visit in visits:
            is_strange = is_visit_long(visit, minutes=60)
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
