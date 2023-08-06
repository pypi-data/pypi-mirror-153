from beginai.exec.embeddings.instructions.interaction import InteractionEncoding

SEQUENCE_MAP = {
    'like': 5,
    'love': 6,
    'dislike': 1,
    'hate': 2,
    'comment': 4,
    '_GB_EMPTY': 0.00011
}

def test_apply_without_values():
    encoding = InteractionEncoding(SEQUENCE_MAP)
    result = encoding.apply([])
    expected = {
        'sent_bin': 1,
        'sentiment': 0.00011,
        'label': "NEUTRAL"
    }
    assert expected == result

def test_apply_more_positive_than_negative():
    encoding = InteractionEncoding(SEQUENCE_MAP)

    values = ["like", "comment", "dislike", "love", "hate"]

    result = encoding.apply(values)

    expected = {
        'sent_bin': 2,
        'sentiment': 6,
        'label': "POSITIVE"
    }

    assert expected == result

def test_apply_more_negative_than_positive():
    encoding = InteractionEncoding(SEQUENCE_MAP)

    values = ["dislike"]

    result = encoding.apply(values)

    expected = {
        'sent_bin': 1,
        'sentiment': 1,
        'label': "NEGATIVE"
    }

    assert expected == result

def test_apply_neutral():
    encoding = InteractionEncoding(SEQUENCE_MAP)

    values = ["comment"]

    result = encoding.apply(values)

    expected = {
        'sent_bin': 1,
        'sentiment': 4,
        'label': "NEUTRAL"
    }

    assert expected == result
