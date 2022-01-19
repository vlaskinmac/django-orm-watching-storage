import datetime


def get_duration(visit):
    if visit.leaved_at:
        duration_secs = visit.leaved_at - visit.entered_at
    else:
        leaved_at = datetime.datetime.now()
        duration_secs = leaved_at - visit.entered_at.replace(tzinfo=None)
    return duration_secs.total_seconds()


def format_duration(duration):
    hours, remainder_secs = divmod(duration, 3600)
    minutes, seconds = divmod(remainder_secs, 60)
    duration_min = duration // 60
    duration_formated = '{:02} часов {:02} минут {:02} секунд'.format(
        round(hours),
        round(minutes),
        round(seconds),
    )
    return duration_formated, duration_min


def is_visit_long(visit, minutes=60):
    if visit.leaved_at:
        duration_secs = visit.leaved_at - visit.entered_at
    else:
        leaved_at = datetime.datetime.now()
        duration_secs = leaved_at - visit.entered_at.replace(tzinfo=None)
    return duration_secs.total_seconds() > minutes