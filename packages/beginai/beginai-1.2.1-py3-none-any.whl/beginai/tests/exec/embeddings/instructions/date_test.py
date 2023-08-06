from beginai.exec.embeddings.instructions.date import Age, CompareDates
from freezegun import freeze_time

@freeze_time("2021-05-16")
def test_return_age_based_on_todays_mocked_date():
    birthday_date = "16-05-1991"
    age_result = Age().apply(birthday_date)
    expected_result = 30

    assert age_result == expected_result

def test_compare_dates_are_on_the_same_month():
    first_date = "01-01-2022"
    second_date = "01-01-2022"
    compare_on = "month"

    result = CompareDates(compare_on).apply(first_date, second_date)
    expected_result = True

    assert result == expected_result

def test_compare_dates_are_not_on_the_same_month():
    first_date = "01-01-2022"
    second_date = "01-02-2022"
    compare_on = "month"

    result = CompareDates(compare_on).apply(first_date, second_date)
    expected_result = False

    assert result == expected_result