from beginai.exec.embeddings.worker import BeginWorker
from beginai.orchapi.api import OrchAPI

class BeginWorkerMock(BeginWorker):

    def __init__(self, app_id, license_key):
        super().__init__(app_id, license_key)
        self.orchapi = _FakeOrchAPI()
    
    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
    
    def get_embeddings(self):
        return self.orchapi.embeddings

class _FakeOrchAPI(OrchAPI):

    def fetch_instructions(self):
        instructions_id = 1
        version_number = 0
        instructions_list = {
            "instructions": {
                "user":[
                    {
                        "instruct":"Age",
                        "complexity":1,
                        "params":{
                        
                        },
                        "f_id":"dateOfBirth",
                        "higher_order":1
                    },
                    {
                        "_chains":[
                        [
                            {
                                "instruct":"Age",
                                "complexity":1,
                                "params":{
                                    
                                },
                                "order":1
                            },
                            {
                                "instruct":"Slice",
                                "complexity":1,
                                "params":{
                                    "minv":10,
                                    "maxv":100,
                                    "num_slices":10
                                },
                                "order":2
                            }
                        ]
                        ],
                        "f_id":"dateOfBirth",
                        "higher_order":2
                    },
                    {
                        "instruct":"Slice",
                        "complexity":1,
                        "params":{
                        "minv":0,
                        "maxv":255,
                        "num_slices":10
                        },
                        "f_id":"numberField",
                        "higher_order":3
                    },
                    {
                        "instruct":"Length",
                        "complexity":1,
                        "params":{
                        
                        },
                        "f_id":"textField",
                        "higher_order":4
                    }
                ],
                "product":[{
                        "instruct":"Length",
                        "complexity":1,
                        "params":{
                        
                        },
                        "f_id":"description",
                        "higher_order":1
                    },
                    {
                        "instruct":"Slice",
                        "complexity":1,
                        "params":{
                            "minv":0,
                            "maxv":255,
                            "num_slices":10
                        },
                        "f_id":"randomNumber",
                        "higher_order":2
                    },
                    {
                        "instruct":"Age",
                        "complexity":1,
                        "params":{
                        
                        },
                        "f_id":"publishedDate",
                        "higher_order":3
                    }
                ],
                "interactions":[{
                    "instruct":"InteractionEncoding",
                    "complexity":1,
                    "params":{
                    "sequence_map":{
                        "like":5,
                        "dislike":1,
                        "comment": 4,
                        "_GB_EMPTY":0.00011
                    }
                    },
                    "higher_order":1,
                    "_with_object":"product"
                    },
                    {
                        "instruct":"InteractionEncoding",
                        "complexity":1,
                        "params":{
                        "sequence_map":{
                            "followed":5,
                            "report":2,
                            "_GB_EMPTY":0.00011
                        }
                        },
                        "higher_order":2,
                        "_with_object":"user"
                    }
                ]
            },
            "tokenize":{
                "user":[
                    "name",
                    "lastName"
                ],
                "product":[
                    "gender",
                    "name"
                ]
            },
            "labels": {
                "user":[ "fake", "not_fake" ],
                "product":[ "fiction", "comedy", "mystery" ]
            }
        }
        return instructions_id, version_number, instructions_list

    def submit_embeddings(self, embeddings, instruction_id, version_number):
        self.embeddings = embeddings
