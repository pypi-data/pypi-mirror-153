from datetime import date, datetime

class Age(object):

    def __init__(self):
        pass

    def apply(self, value):
        born = datetime.strptime(value, "%d-%m-%Y").date()
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

class CompareDates(object):
    """
    compare dates from two fields.
    """
    def __init__(self, compare_on):
        # eg. compare on month or day or year.
        self.compare_on = compare_on

    def apply(self, value, other_field_value):
        date1 = datetime.strptime(value, "%d-%m-%Y").date()
        date2 = datetime.strptime(other_field_value, "%d-%m-%Y").date()
        return getattr(date1, self.compare_on) == getattr(date2, self.compare_on)


instructions_map = {
    "Age": Age,
    "CompareDates": CompareDates
}
