from datetime import datetime


def commit_dates(commits):

    dates = []

    for commit in commits:

        date = commit["commit"]["author"]["date"]

        dates.append(datetime.fromisoformat(date.replace("Z", "+00:00")))

    return sorted(dates)


def average_gap_days(dates):

    if len(dates) < 2:
        return 0

    gaps = []

    for i in range(1, len(dates)):

        gap = (dates[i] - dates[i - 1]).days

        gaps.append(gap)

    return round(sum(gaps) / len(gaps), 2)


def commit_frequency(dates):

    if len(dates) < 2:
        return len(dates)

    span = (dates[-1] - dates[0]).days

    if span == 0:
        return len(dates)

    return round(len(dates) / span, 3)
