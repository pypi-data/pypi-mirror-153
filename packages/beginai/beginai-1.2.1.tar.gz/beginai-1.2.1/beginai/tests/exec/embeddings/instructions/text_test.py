from beginai.exec.embeddings.instructions.text import Length, CountDigits, StandardName, CountWord, Tokenize

def test_text_length():
    value = 'My string'    
    assert len(value) == Length().apply(value)

def test_text_length_when_none():
    value = None  
    assert None == Length().apply(value)

def test_counting_number_of_digits_should_be_zero():
    value = 'No digits here'
    expected = 0
    assert expected == CountDigits().apply(value)

def test_counting_number_of_digits_should_be_two():
    value = '1 digit here and another 1 here'
    expected = 2
    assert expected == CountDigits().apply(value)

def test_name_standard_even_when_maskered():
    standard_names = ['Chandler', 'Ross', 'Joey', 'Rachel', 'Phoebe', 'Monica']
    masked_name = 'Ch?an(dl)er'
    expected = True
    assert expected == StandardName(standard_names).apply(masked_name)

def test_counting_how_many_times_same_word_appears_should_be_two():
    value = 'Oh Hello, there, hello again!'
    expected = 2
    assert expected == CountWord("hello").apply(value)

def test_tokenizer():
    value = 'Oh Hello'
    expected = {
        'input_ids': [101, 2821, 7592, 102, 0, 0, 0, 0], 
        'attention_mask': [1, 1, 1, 1, 0, 0, 0, 0], 
        'len_': 4
    }
    assert expected == Tokenize().apply(value)

def test_tokenizer_with_empty_value_provided():
    value = ''
    expected = {
        'input_ids': [], 
        'attention_mask': [], 
        'len_': 0
    }
    assert expected == Tokenize().apply(value)
