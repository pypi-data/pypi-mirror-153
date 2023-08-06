from . import ParseAndExecute
from ...orchapi.api import OrchAPI
from tqdm import tqdm
import pandas as pd
import datetime

class AlgorithmsApplier(object):

    host = "https://sdk.begin.ai"

    INTERACTIONS = 'interactions'

    def __init__(self, app_id, license_key, host = None):
        self.orchapi = OrchAPI()
        self.orchapi.configure_orch_connection(host or self.host)
        self.orchapi.set_app_id_and_license_key(app_id = app_id, license_key = license_key)
        self._submission_in_progress = False

        self.embeddings = {}
        self.files = {}
    
    def load_user_data(self, filename, unique_identifier_column, label_column = None):
        if unique_identifier_column == '' or unique_identifier_column is None:
            raise ValueError('The unique indentifier column must be provided')

        self._add_data_to_files_dictionary(filename, 'user', unique_identifier_column, label_column=label_column)

    def load_object_data(self, filename, object_name, unique_identifier_column, label_column = None):
        if object_name == '' or object_name is None:
            raise ValueError('The object name must be provied before the file is loaded')

        if unique_identifier_column == '' or unique_identifier_column is None:
            raise ValueError('The unique indentifier column must be provided')

        self._add_data_to_files_dictionary(filename, object_name, unique_identifier_column, label_column=label_column)

    def load_interactions(self, filename, unique_identifier_column, target_object_name, 
            target_unique_identifier_column, interaction_column_name):
        if unique_identifier_column == '' or unique_identifier_column is None:
            raise ValueError('The unique indentifier column must be provided')
        if target_object_name == '' or target_object_name is None:
            raise ValueError('The target object when registering an interaction must be provided')
        if target_unique_identifier_column == '' or target_unique_identifier_column is None:
            raise ValueError('The target unique indentifer column when registering an interaction must be provided')
        if interaction_column_name == '' or interaction_column_name is None:
            raise ValueError('The interaction column when registering an interaction must be provided')
        
        target_object = {
            'name': target_object_name.lower(),
            'uuid_column': target_unique_identifier_column.lower(),
            'interaction_column': interaction_column_name.lower()
        }

        self._add_data_to_files_dictionary(filename, self.INTERACTIONS, unique_identifier_column, target_object)

    def _add_data_to_files_dictionary(self, filename, object_name, uuid_column, target_object = {}, label_column = None):
        self.files[object_name] = {
            'data': self._read_file(filename),
            'uuid_column': uuid_column.lower(),
            'target_object': target_object,
            'label_column': label_column
        }

    def _read_file(self, filename):
        if filename == '' or filename is None:
            raise ValueError('File must be provided')

        df = pd.read_csv(filename, dtype=str)
        df = df.rename(columns=str.lower)
        return df

    def _get_instructions(self):
        return self.orchapi.fetch_instructions()

    def learn_from_data(self, update=False):
        if len(self.files) == 0:
            return

        print("Start time: ", datetime.datetime.now())

        instructions_id, current_embeddings_version, instructions = \
            self._get_instructions()

        self._generate_signatures(instructions)

        self._submit(instructions_id, current_embeddings_version, update)

        print("End time: ", datetime.datetime.now())
        self.flush_memory()

    def flush_memory(self):
        self.embeddings = {}
        self.files = {}

    def _generate_signatures(self, instructions):
        parser = ParseAndExecute(instructions)

        for object in self.files.keys():
            object_config = self.files[object]

            df = object_config['data']
            uuid_column = object_config['uuid_column']
            label_column = object_config['label_column']

            dictionary = df.to_dict(orient='records')

            object_data = []

            if object == self.INTERACTIONS:
                target_object = object_config['target_object']
                target_object_name = target_object['name']
                user_interactions = self._parse_interactions(df, uuid_column, target_object)

                for user_id in user_interactions.keys():
                    value = user_interactions[user_id]
                    parser.feed(value)
                    results = parser.parse(object)
                    if len(results) > 0:
                        object_data.append([str(user_id), target_object_name, results[target_object_name]])
                            
            else:
                for index, row in tqdm(enumerate(dictionary)):
                    row = self._handle_labels(label_column, row)
                    parser.feed(row)
                    results = parser.parse(object)
                    if len(results) > 0:
                        key = row[uuid_column]
                        object_data.append([ key, results ])

            if len(object_data) > 0: 
                if object not in self.embeddings:
                    self.embeddings[object] = []

                self.embeddings[object] = object_data

    def _handle_labels(self, label_column, row):
        # TODO faster to do this on dataframe level.
        value = row.get(label_column, '')
        if label_column is not None and value is not None:
            row['labels'] = [ value ]
        return row

    def _parse_interactions(self, df, uuid_column, target_object):
        target_object_name = target_object['name']
        interaction_column = target_object['interaction_column']
        df = df.groupby([uuid_column, target_object['uuid_column']], as_index=False)
 
        user_interactions = {}
        for key, group in tqdm(df):
            uuid = key[0]
            target_uuid = key[1]

            if uuid not in user_interactions:
                user_interactions[uuid] = {}
            
            if target_object_name not in user_interactions[uuid]:
                user_interactions[uuid][target_object_name] = {}

            if target_uuid not in user_interactions[uuid][target_object_name]: 
                user_interactions[uuid][target_object_name][target_uuid] = []

            value = str(group[interaction_column].values[0]).lower()
            user_interactions[uuid][target_object_name][target_uuid].append(value)
                    
        return user_interactions

    def _submit(self, instructions_id, current_version, update):
        if self._submission_in_progress or len(self.embeddings) == 0:
            return

        print("Working on submitting existing set. please wait.")

        self._submission_in_progress = True

        self._update_interactions_structure_before_batch()

        for key in self.embeddings.keys():
            print("Submiting embeddings associated with {}".format(key))
            if key == self.INTERACTIONS:
                for target_object in self.embeddings[key]:
                    self._submit_objects(self.embeddings[key][target_object], key, instructions_id, current_version, target_object)
            else:
                self._submit_objects(self.embeddings[key], key, instructions_id, current_version, None, update)

        self._submission_in_progress = False            

    def _update_interactions_structure_before_batch(self):
        if len(self.embeddings) == 0 or self.INTERACTIONS not in self.embeddings:
            return

        grouped_by_target_object = {}        

        for data in self.embeddings[self.INTERACTIONS]:
            target_object = data[1]
            interactions = data[2]

            if target_object not in grouped_by_target_object:
                grouped_by_target_object[target_object] = []

            for object_id in interactions.keys():
                grouped_by_target_object[target_object].append({
                    'person_id': data[0],
                    'object_id': str(object_id),
                    'interaction': interactions[object_id],
                })

        self.embeddings[self.INTERACTIONS] = grouped_by_target_object

    def _submit_objects(self, data, key, instructions_id, current_version, target_object = None, update = False):
        end_counter = 20000
        start_counter = 0
        all_ = len(data)
        while(start_counter < all_):
            slice = data[start_counter:end_counter]
            self.orchapi.submit_embeddings_batch(slice, instructions_id, current_version, key, target_object, update)
            print("submitted {} at index {} out of {} {}".format(len(slice), start_counter, all_, key))
            start_counter += 20000
            end_counter += 20000

    def recommend(self, project_id, user_id, limit = None, page = None):
        return self.orchapi.recommend(project_id, user_id, limit, page)

    def predict_engagement(self, project_id, user_id, object_id):
        return self.orchapi.predict_engagement(project_id, user_id, object_id)

    def fake_detect(self, project_id, target_id):
        return self.orchapi.fake_detect(project_id, target_id)

    def classify(self, project_id, target_id):
        return self.orchapi.classify(project_id, target_id)

    def get_training_performance(self, project_id):
        return self.orchapi.training_results(project_id)

    # maintenance end points

    def learn_from_data_dry_run(self):
        """
        does not submit embeddings, only generates them.
        """
        if len(self.files) == 0:
            return

        print("Start time: ", datetime.datetime.now())

        instructions_id, current_embeddings_version, instructions = \
            self._get_instructions()

        self._generate_signatures(instructions)
        return self.embeddings

    def map_feature_to_instructions(self, object_type, raw_emb):
        """
        expect a row of raw data, will do the following:
        - fetch and apply instructions.
        - generate an embedding
        - demonstrate the transformation from original data to the final value
           and the instruct used for the trnsformation.
        """
        instructions_id, current_embeddings_version, instructions = \
            self._get_instructions()
        instructs_by_order = {}
        for i in instructions[0][object_type]:
            instructs_by_order.update({i['higher_order']: i})

        parser = ParseAndExecute(instructions)
        parser.feed(raw_emb)
        emb_val = parser.parse('book')

        res = {}
        for i, ev in enumerate(emb_val):
            instruction = instructs_by_order[i+1]
            f_id = instruction['f_id']
            res[f_id] = ("value: ",ev, instruction['instruct'], "raw: ", raw_emb[f_id])
        return res
            


    # def infer(self, object, project_id):
    #     # apply instruction on the object.
    #     self.parser.feed(object)
    #     embedding = self.parser.parse()
    #     # infer.
    #     return self.orchapi.infer(embedding, project_id)
