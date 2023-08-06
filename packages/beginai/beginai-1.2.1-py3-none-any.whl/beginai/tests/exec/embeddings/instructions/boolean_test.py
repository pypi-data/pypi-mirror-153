from beginai.exec.embeddings.instructions.boolean import Boolean

true = 2
false = 1
_GB_EMPTY = 0.00011


def test_apply_with_None_value_should_return_GB_EMPTY_value():
    sequence = Boolean(true, false, _GB_EMPTY)
    sequence_value = sequence.apply( value = None )
    assert _GB_EMPTY == sequence_value

def test_apply_with_true_value_as_number_should_return_2():
    sequence = Boolean(true, false, _GB_EMPTY)
    sequence_value = sequence.apply( value = 1 )
    assert true == sequence_value

def test_apply_with_false_value_as_number_should_return_1():
    sequence = Boolean(true, false, _GB_EMPTY)
    sequence_value = sequence.apply( value = 0 )
    assert false == sequence_value

def test_apply_with_true_value_as_string_should_return_2():
    sequence = Boolean(true, false, _GB_EMPTY)
    sequence_value = sequence.apply( value = "True" )
    assert true == sequence_value

def test_apply_with_false_value_as_string_should_return_1():
    sequence = Boolean(true, false, _GB_EMPTY)
    sequence_value = sequence.apply( value = "False" )
    assert false == sequence_value

def test_apply_with_true_value_as_boolean_should_return_2():
    sequence = Boolean(true, false, _GB_EMPTY)
    sequence_value = sequence.apply( value = True )
    assert true == sequence_value

def test_apply_with_false_value_as_boolean_should_return_1():
    sequence = Boolean(true, false, _GB_EMPTY)
    sequence_value = sequence.apply( value = False )
    assert false == sequence_value
