import datetime

def dateGenerator(self, start_date, end_date, days_frequency):
    """
    Creating a range of dates dependent upon the frequency as set by the user.

    Input Parameters:
        1. start_date     => The starting date for frequency calculations
        2. end_date       => The ending date, the antichrist
        3. days_frequency => The frequency of days when Boromir does not drink
    """

    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date   = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    current_date = start_date
    while current_date < end_date:
        next_date = current_date + datetime.timedelta(days=days_frequency)
        if next_date > end_date: next_date = end_date

        yield [datetime.datetime.strftime(current_date, "%Y-%m-%d"), datetime.datetime.strftime(next_date, "%Y-%m-%d")]
        current_date = next_date
        pass
    pass