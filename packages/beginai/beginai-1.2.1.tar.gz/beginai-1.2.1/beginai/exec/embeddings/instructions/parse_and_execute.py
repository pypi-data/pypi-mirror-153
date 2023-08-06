"""
TODO: look into how to use empty number when value is nan.
because nan is not empty and so it's difficult to manage.
write some tests for the instructions appliers.
introduce a number of instructions appliers and a tool for mobile testing
of instructions and generated embeddings (API).
develop more instructions.
"""

from . import instructions_map
from .interaction import InteractionEncoding

ERR_NUMBER = 0.00011
EMPTY_NUMBER = 0.00012

class ParseAndExecute(object):

    INTERACTIONS_KEY = "interactions"
    LABELS_KEY = "labels"
    TOKENIZE_KEY = "tokenize"

    def __init__(self, data):
        # order the instructions on higher_order.
        self.instructions = self._group_and_sort_instructions(data)
        self.labels = self._retrieve_labels(data)
        self.tokenization_fields = self._retrieve_tokenization_fields(data)
        self.tokenize_instruction = instructions_map['Tokenize']()

    def _group_and_sort_instructions(self, data):
        if len(data) == 0:
            return {}

        sorted_dictionary = {}
        instructions = data.get("instructions", {})
        for instruction_key in instructions.keys():
            sorted_dictionary[instruction_key] = sorted(instructions.get(instruction_key), key=lambda k: k['higher_order'])
        return sorted_dictionary

    def _retrieve_labels(self, data):
        if len(data) == 0:
            return {}
        return data.get(self.LABELS_KEY, {})

    def _retrieve_tokenization_fields(self, data):
        if len(data) == 0:
            return {}
        return data.get(self.TOKENIZE_KEY, {})

    def feed(self, values_dict):
        self.values = values_dict

    def _process_instruction(self, value, instruct):
        klass = instructions_map.get(instruct['instruct'])
        if not klass:
            return ERR_NUMBER
        # if instruction involves multiple fields.
        other_value = None

        instruct_params = instruct.get('params', {}).copy()
        # if params point to another field, get that field value too.
        if "field" in instruct_params:
            other_value = self.values.get(instruct_params['field'])
            del instruct_params['field']

        obj = klass(**instruct_params)

        try:
            if other_value:
                # in case it involves two fields.
                res = obj.apply(value, other_value)
            else:
                res = obj.apply(value)
        except Exception as e:
            return ERR_NUMBER

        if res is None:
            return ERR_NUMBER
        elif isinstance(res, list):
            return res
        elif isinstance(obj, InteractionEncoding):
            return res
        else:
            return float(res)
    
    def _process_labels(self, object_name, object_values):
        labels = []
        
        labels_provided = self.labels.get(object_name)

        if labels_provided == None or len(labels_provided) == 0:
            return labels

        labels_provided = list(set(labels_provided))
        labels_from_api = object_values.get(self.LABELS_KEY, []) 

        if len(labels_from_api) == 0:
            return labels
        
        for label in labels_provided:
            if label in labels_from_api:
                labels.append(label)

        return labels


    def _process_text_tokens(self, object_name, object_values):
        """
        generates one giant list of tokens for every object.
        does not keep text field seperated.
        """
        tokens = []

        field_names = self.tokenization_fields.get(object_name, [])

        if len(field_names) == 0:
            return tokens

        full_text = ''
        for field_name in field_names:
            if field_name in object_values:
                full_text += object_values[field_name]

        return self.tokenize_instruction.apply(full_text)


    def parse(self, object_name):
        embedding = []
        labels = []
        tokens = {'input_ids': [], 'attention_mask': [], 'len_': 0 } 
        if self.instructions.get(object_name) == None:
            return {}

        if object_name == self.INTERACTIONS_KEY:
            return self._process_interactions()
        else:
            if self.labels.get(object_name) is not None:
                labels = self._process_labels(object_name, self.values)

            if self.tokenization_fields.get(object_name) is not None:
                tokens = self._process_text_tokens(object_name, self.values)

            for instruct in self.instructions.get(object_name.lower()):
                chains = instruct.get('_chains', None)
                value = self.values.get(instruct['f_id'].lower())

                if not value and (value != 0 and instruct['instruct'] == 'Boolean'):
                    embedding.append(ERR_NUMBER)
                    continue

                if chains:
                    for chain in chains:
                        chain_list = sorted(chain, key=lambda k: k['order'])
                        for item in chain_list:
                            value = self._process_instruction(value, item)
                        res = value # last response in the chain is the return value.
                        embedding.append(res)
                else:
                    res = self._process_instruction(value, instruct)
                    embedding.append(res)

        return {
            "embedding": embedding,
            "labels": labels,
            "tokens": tokens
        }

    def _process_interactions(self):
        embeddings_per_object = {}
        for object_key in self.values.keys():
            instruction = next((item for item in self.instructions[self.INTERACTIONS_KEY] if item["_with_object"] == object_key), None)

            if instruction is None:
                continue

            embeddings_per_object[object_key] = { }

            for action_object in self.values[object_key]:
                result = self._process_instruction(self.values[object_key][action_object], instruction)
                embeddings_per_object[object_key][action_object] = result

        return embeddings_per_object

