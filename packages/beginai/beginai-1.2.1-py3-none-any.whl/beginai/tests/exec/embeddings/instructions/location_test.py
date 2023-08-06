from beginai.exec.embeddings.instructions.location import DistanceFromField, DistanceFromPoint

HALIFAX_COORDINATES = {
    "latitude": 44.648766,
    "longitude": -63.575237
}

DARTMOUTH_COORDINATES = {
    "latitude": 44.671490,
    "longitude": -63.571411
}

def test_distance_from_field():
    expected = 2.545647634422763

    distance_from_field = DistanceFromField()
    result = distance_from_field.apply(HALIFAX_COORDINATES, DARTMOUTH_COORDINATES)

    assert expected == result

def test_distance_from_point():
    expected = 2.545647634422763

    distance_from_field = DistanceFromPoint(HALIFAX_COORDINATES.get('latitude'), HALIFAX_COORDINATES.get('longitude'))
    result = distance_from_field.apply(DARTMOUTH_COORDINATES)

    assert expected == result
    