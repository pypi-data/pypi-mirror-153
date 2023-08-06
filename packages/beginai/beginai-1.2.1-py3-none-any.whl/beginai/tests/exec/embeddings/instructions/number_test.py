from beginai.exec.embeddings.instructions.number import Slice, CompareToField, CompareToNumber

def test_compare_two_numbers_are_the_same():
    compare_to = 10
    value = 10
    expected_result = True
    assert expected_result == CompareToNumber(compare_to).apply(value)

def test_compare_two_field_values_are_the_same_should_return_false_when_one_is_a_string_with_letters():
    compare_to = 10
    value = "10A"
    expected_result = False
    assert expected_result == CompareToField().apply(value, compare_to)

def test_compare_two_field_values_are_the_same_should_return_true():
    compare_to = 10
    value = "10"
    expected_result = True
    assert expected_result == CompareToField().apply(value, compare_to)


def test_slice():
    minv = 10
    maxv = 100
    num_slices = 2
    value = 80
    expected_result = 2

    sliceObject = Slice(minv, maxv, num_slices)
    result = sliceObject.apply(value)
    assert expected_result == result