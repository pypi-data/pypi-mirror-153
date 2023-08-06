from beginai.exec.embeddings.instructions.category import Sequence

_GB_EMPTY_VALUE = 999
CATEGORY_VALUE = 1

sequence_map = {
    'category': CATEGORY_VALUE,
    '_GB_EMPTY': _GB_EMPTY_VALUE
}

def test_apply_with_None_value_should_return_GB_EMPTY_value():
    sequence = Sequence(sequence_map)
    sequence_value = sequence.apply( value = None )
    assert _GB_EMPTY_VALUE == sequence_value

def test_apply_with_empty_value_should_return_GB_EMPTY_value():
    sequence = Sequence(sequence_map)
    sequence_value = sequence.apply( value = '' )
    assert _GB_EMPTY_VALUE == sequence_value

def test_apply_with_category_key_should_return_value():
    sequence = Sequence(sequence_map)
    sequence_value = sequence.apply( value = 'category' )
    assert CATEGORY_VALUE == sequence_value