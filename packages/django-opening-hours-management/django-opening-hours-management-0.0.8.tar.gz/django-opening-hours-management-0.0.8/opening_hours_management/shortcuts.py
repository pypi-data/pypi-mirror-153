def time_total_seconds(t):
    return (t.hour * 60 + t.minute) * 60 + t.second


def format_time_range(opening_time, closing_time):
    return "{open} - {close}".format(
        open=opening_time.strftime("%Hh%M"), close=closing_time.strftime("%Hh%M")
    )
