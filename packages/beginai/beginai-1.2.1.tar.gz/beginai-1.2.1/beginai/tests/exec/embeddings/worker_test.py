from freezegun import freeze_time
from .mock_service import BeginWorkerMock
import json

APP_ID = 1
LICENSE_KEY = 10

@freeze_time("2021-05-16")
def test_learn_from_data():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.set_data({
        "user":{
            "111":{
                "dateofbirth":"09-12-1989",
                "userlocation":{
                    "latitude":36.8507689,
                    "longitude":-76.2858726
                },
                "numberfield": 10,
                "textfield": "Hello!"
            },
            "222": {
                "dateofbirth":"09-12-1990",
                "userlocation":{
                    "latitude":36.8507689,
                    "longitude":-76.2858726
                },
                "numberfield": 120,
                "textfield": "Hellooooooo!"
            }
        },
        "interactions":{
            "111": {
                "product":{
                    "10":[
                        "like",
                        "comment",
                        "like"
                    ],
                    "20":[
                        "dislike"
                    ],
                    "30":[
                        "comment"
                    ]

                }
            }
        },
        "product":{
            "10":{
                "description":"....the description...",
                "randomnumber": 100.0,
                "publisheddate": "09-12-1999"
            },
            "20":{
                "description":"hi!",
                "randomnumber": 100.0,
                "publisheddate": "09-12-1991"
            },
            "30":{
                "description":"hi!!",
                "randomnumber": 100.0,
                "publisheddate": "09-12-1991"
            }
        }
    })

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = {
        "user":{
            "111":{
                'embedding': [ 31.0, 4.0, 1.0, 6.0 ],
                'labels': [],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            },
            "222": {
                'embedding': [ 30.0, 4.0, 8.0, 12.0 ],
                'labels': [],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            }
        },
        "interactions":{
            "111": {
                "product": {
                    "10": {
                        "sent_bin": 2,
                        "sentiment": 5,
                        "label": "POSITIVE"
                    },
                    '20': {
                        "sent_bin": 1,
                        "sentiment": 1,
                        "label": "NEGATIVE"
                    },
                    '30': {
                        "sent_bin": 1,
                        "sentiment": 4,
                        "label": "NEUTRAL"
                    },
                }
            }
        },
        "product":{
            "10": {
                'embedding': [ 22.0, 7.0, 21.0 ],
                'labels': [],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            },
            '20':{
                'embedding': [ 3.0, 7.0, 29.0 ],
                'labels': [],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            },
            '30':{
                'embedding': [ 4.0, 7.0, 29.0 ],
                'labels': [],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            }
        }
    }
    assert json.dumps(result, sort_keys=True) == json.dumps(expected, sort_keys=True)

@freeze_time("2021-05-16")
def test_learn_from_data_with_different_types_of_interaction():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.set_data({
        "user":{
            "111":{
                "dateofbirth":"09-12-1989",
                "userlocation":{
                    "latitude":36.8507689,
                    "longitude":-76.2858726
                },
                "numberfield": 10,
                "textfield": "Hellooooooo!"
            }
        },
        "interactions":{
            "111": {
                "product":{
                    "10":[
                        "like",
                        "comment",
                        "like"
                    ],
                    "20":[
                        "dislike"
                    ]
                },
                "user":{
                    "1234":[
                        "report"
                    ]
                }
            }
        },
        "product":{
            "10":{
                "description":"....the description...",
                "randomnumber": 100.0,
                "publisheddate": "09-12-1990"
            },
            "20":{
                "description":"hi!",
                "randomnumber": 50.0,
                "publisheddate": "09-12-1991"
            }
        }
    })

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = {
        "user":{
            "111":{
                'embedding': [ 31.0, 4.0, 1.0, 12.0 ],
                'labels': [],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            }
        },
        "interactions":{
            "111": {
                "product":{
                    "10": {
                        "sent_bin": 2,
                        "sentiment": 5,
                        "label": "POSITIVE"
                    },
                    '20': {
                        "sent_bin": 1,
                        "sentiment": 1,
                        "label": "NEGATIVE"
                    },
                },
                "user": {
                    "1234": {
                        "sent_bin": 1,
                        "sentiment": 2,
                        "label": "NEGATIVE"
                    },
                }
            }
        },
        "product":{
            "10":{
                'embedding': [ 22.0, 7.0, 30.0 ],
                'labels': [],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            },
            '20':{
                'embedding': [ 3.0, 4.0, 29.0 ],
                'labels': [],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            }
        }
    }
    assert expected == result


def test_learn_from_data_remove_empty_objects():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.set_data({
        "user":{
            "111":{}
        },
        "product":{
            "10":{
                "description":"....the description...",
                "randomnumber": 10.0,
                "publisheddate": "09-12-1991"
            },
            "20":{
                "description":"hi!",
                "randomnumber": 1,
                "publisheddate": "09-12-1993"
            }
        }
    })

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = {
        "product":{
            "10":{
                'embedding': [ 22.0, 1.0, 30.0 ],
                'labels': [],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            },
            '20':{
                'embedding': [ 3.0, 1.0, 28.0 ],
                'labels': [],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            }
        }
    }
    assert expected == result

def test_learn_from_returns_no_value_when_property_doesnt_exist():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.set_data({
        "product":{
            "10":{
                "description":"....the description...",
                "randomnumber": 10.0,
                "publisheddate": "09-12-1991"
            },
            "20":{
                "description_doesnt_exist":"hi!",
                "randomnumber1": 1,
                "publisheddate": "09-12-1993"
            }
        }
    })

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = {
        "product":{
            "10":{
                'embedding': [ 22.0, 1.0, 30.0 ],
                'labels': [],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            },
            '20':{
                'embedding': [ 0.00011, 0.00011, 28.0 ],
                'labels': [],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            }
        }
    }
    assert expected == result

def test_learn_from_returns_removes_object_not_defined_in_schema():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.set_data({
        "objectnotinschema": {
            "2": {
                "description": "blah"
            }
        },
        "product":{
            "10":{
                "description":"....the description...",
                "randomnumber": 10.0,
                "publisheddate": "09-12-1991"
            },
            "20":{
                "description_doesnt_exist":"hi!",
                "randomnumber1": 1,
                "publisheddate": "09-12-1993"
            }
        },
        "interactions":{
            "111": {
                "product":{
                    "10":[
                        "like",
                        "comment",
                        "like"
                    ],
                    "20":[
                        "dislike"
                    ]
                },
                "objectnotinschema":{
                    "2":[
                        "report"
                    ]
                }
            }
        }
    })

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = {
        "product":{
            "10":{
                'embedding': [ 22.0, 1.0, 30.0 ],
                'labels': [],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            },
            '20':{
                'embedding': [ 0.00011, 0.00011, 28.0 ],
                'labels': [],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            }
        },
        "interactions":{
            "111": {
                "product":{
                    "10": {
                        "sent_bin": 2,
                        "sentiment": 5,
                        "label": "POSITIVE"
                    },
                    '20': {
                        "sent_bin": 1,
                        "sentiment": 1,
                        "label": "NEGATIVE"
                    },
                }
            }
        }
    }
    assert expected == result

@freeze_time("2021-05-16")
def test_learn_from_data_with_labels():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.set_data({
        "user":{
            "111":{
                "dateofbirth":"09-12-1989",
                "userlocation":{
                    "latitude":36.8507689,
                    "longitude":-76.2858726
                },
                "numberfield": 10,
                "textfield": "Hellooooooo!",
                "labels": ["fake"]
            }
        },
        "product":{
            "10":{
                "description":"....the description...",
                "randomnumber": 10.0,
                "publisheddate": "09-12-1991",
                "labels": ["comedy"]
            },
            "20":{
                "description":"hi!",
                "randomnumber": 1,
                "publisheddate": "09-12-1993",
                "labels": ["mystery"]
            }
        }
    })

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = {
        "user":{
            "111": {
                "embedding": [ 31.0, 4.0, 1.0, 12.0 ],
                "labels": ["fake"],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            }
        },
        "product":{
            "10":{
                "embedding": [ 22.0, 1.0, 29.0 ],
                "labels": ["comedy"],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            },
            '20':{
                "embedding": [ 3.0, 1.0, 27.0 ],
                "labels": ["mystery"],
                'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}
            }
        }
    }
    assert expected == result


@freeze_time("2021-05-16")
def test_learn_from_data_with_tokens():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.set_data({
        "user":{
            "111":{
                "dateofbirth":"09-12-1989",
                "userlocation":{
                    "latitude":36.8507689,
                    "longitude":-76.2858726
                },
                "numberfield": 10,
                "textfield": "Hellooooooo!",
                "labels": ["fake"],
                "name": "Jane",
                "lastName": "Doe"
            }
        },
        "product":{
            "10":{
                "description":"....the description...",
                "randomnumber": 10.0,
                "publisheddate": "09-12-1991",
                "labels": ["comedy"],
                "gender": "fiction"
            },
            "20":{
                "description":"hi!",
                "randomnumber": 1,
                "publisheddate": "09-12-1993",
                "labels": ["mystery"],
                "gender": "romance"
            }
        }
    })

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = {
        "user":{
            "111": {
                "embedding": [ 31.0, 4.0, 1.0, 12.0 ],
                "labels": ["fake"],
                'tokens': {'input_ids': [101, 4869, 3527, 2063, 102, 0, 0], 'attention_mask': [1, 1, 1, 1, 1, 0, 0], 'len_': 5}
            }
        },
        "product":{
            "10":{
                "embedding": [ 22.0, 1.0, 29.0 ],
                "labels": ["comedy"],
                'tokens': {'input_ids': [101, 4349, 102, 0, 0, 0, 0], 'attention_mask': [1, 1, 1, 0, 0, 0, 0], 'len_': 3}
            },
            '20':{
                "embedding": [ 3.0, 1.0, 27.0 ],
                "labels": ["mystery"],
                'tokens': {'input_ids': [101, 7472, 102, 0, 0, 0, 0], 'attention_mask': [1, 1, 1, 0, 0, 0, 0], 'len_': 3}
            }
        }
    }
    assert expected == result
