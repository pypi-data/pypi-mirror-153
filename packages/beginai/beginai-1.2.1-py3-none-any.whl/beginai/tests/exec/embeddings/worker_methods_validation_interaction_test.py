from .mock_service import BeginWorkerMock

APP_ID = 1
LICENSE_KEY = 10

def test_register_interaction_without_user_id():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    try:
        bw.register_interaction(user_id = '', object_name='', object_id=1, action='like')
    except ValueError:
        assert True

def test_register_interaction_without_object_name():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    try:
        bw.register_interaction(user_id = 1, object_name='', object_id=1, action='like')
    except ValueError:
        assert True

def test_register_interaction_without_object_id():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    try:
        bw.register_interaction(user_id = 1, object_name='product', object_id=None, action='like')
    except ValueError:
        assert True

def test_register_interaction_without_action_id():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    try:
        bw.register_interaction(user_id = 1, object_name='product', object_id=1, action='')
    except ValueError:
        assert True

def test_register_interaction_with_the_same_product_id():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = "product"
    object_id = 10
    user_id = 1

    bw.register_interaction(user_id, object_name, 'like', object_id)
    bw.register_interaction(user_id, object_name, 'dislike', object_id)

    results = bw.get_data().get('interactions').get(user_id).get(object_name)

    assert results == { object_id: [ 'like', 'dislike' ]}

def test_register_interaction_with_different_product_id():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = "product"
    object_id_one = 10
    object_id_two = 20
    user_id = 1

    bw.register_interaction(user_id, object_name, 'LIKE', object_id_one)
    bw.register_interaction(user_id, object_name, 'DISLIKE', object_id_two)

    results = bw.get_data().get('interactions').get(user_id).get(object_name)
    assert results == { object_id_one: [ 'like' ], object_id_two: ['dislike']}
