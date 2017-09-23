import datetime


# returns a list of pairs of datetime and string of datetime suitable to be given as an argument od ChoiceFields.choices
# List contains only weekdays
def get_list_dates(count_days):
    d = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    end_date = d + count_days* delta

    print("Now: ", d)
    print("End date: ", end_date)

    choices_dates = list()

    while d <= end_date:
        if d.weekday() < 5:
            choices_dates.append((d, d.strftime("%Y-%m-%d")))
        d += delta

    return choices_dates


def get_apps_times_for_date():
    # find a way to use date

    d = datetime.datetime(2014, 5, 12, 8,
                          00)  # first 3 numbers don't matter, I only use hours and minutes from this temporary object
    delta = datetime.timedelta(minutes=20)
    choices_times = list()

    while d.hour < 16:
        choices_times.append((d, d.strftime('%H:%M')))
        d += delta

    return choices_times