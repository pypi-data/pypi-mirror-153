from ...orchapi.api import OrchAPI
from . import ParseAndExecute
import datetime

class BeginWorker(object):

    host = "https://sdk.begin.ai"

    def __init__(self, app_id, license_key, host = None):
        self.orchapi = OrchAPI()
        self.orchapi.configure_orch_connection(host or self.host)
        self.orchapi.set_app_id_and_license_key(app_id = app_id, license_key = license_key)
        self._reset_to_initial_state()

    def register_user(self, user_id):
        if user_id in self.data.get('user'):
            return
        
        self.data['user'][user_id] = {}

    def register_object(self, object_name, object_id):
        if (object_name == '' or object_name is None) or (object_id == '' or object_id is None):
            raise ValueError('Object name and Object id must be provided')
        
        object_name = object_name.lower()

        if object_name not in self.data:
            self.data[object_name] = {}

        if object_id in self.data.get(object_name):
            return
        
        self.data[object_name][object_id] = {}

    def update_user_text_field(self, user_id, field, value: str):
        self._validate_properties_for_user_object(user_id, field, value)

        if self._is_valid_type(value, str) == False:
            raise ValueError('Value must be a String')

        self._set_value(user_id, field, value, 'user')

    def update_user_boolean_field(self, user_id, field, value: bool):
        self._validate_properties_for_user_object(user_id, field, value)

        if self._is_valid_type(value, bool) == False:
            raise ValueError('Value must be a Boolean')

        self._set_value(user_id, field, value, 'user')

    def update_user_numerical_field(self, user_id, field, value: int or float):
        self._validate_properties_for_user_object(user_id, field, value)

        if self._is_valid_type(value, int) == False and self._is_valid_type(value, float) == False:
            raise ValueError('Value must be either an int or a float')

        self._set_value(user_id, field, value, 'user')

    def update_user_date_field(self, user_id, field, date, date_format='%d-%m-%Y'):
        self._validate_properties_for_user_object(user_id, field, date)

        formatted_date = datetime.datetime.strptime(date, date_format).strftime('%d-%m-%Y')

        self._set_value(user_id, field, formatted_date, 'user')

    def update_user_location_field(self, user_id, field, latitude, longitude):
        if user_id == '' or user_id is None or user_id not in self.data['user']:
            raise ValueError('Either the provided User Id was not provided or this User Id was not registered yet, please register through the register_user method')

        if (field == '' or field is None) or (latitude == '' or latitude is None) or (longitude == '' or longitude is None):
            raise ValueError('Field, latitude and longitude must be provided')

        lat_lng_object = {
            "latitude": latitude,
            "longitude": longitude
        }

        self._set_value(user_id, field, lat_lng_object, 'user')
    
    def update_object_text_field(self, object_name, object_id, field, value: str):
        self._validate_properties_for_other_object(object_name, object_id, field, value)

        if self._is_valid_type(value, str) == False:
            raise ValueError('Value must be a String')

        self._set_value(object_id, field, value, object_name)

    def update_object_boolean_field(self, object_name, object_id, field, value: bool):
        self._validate_properties_for_other_object(object_name, object_id, field, value)

        if self._is_valid_type(value, bool) == False:
            raise ValueError('Value must be Boolean')

        self._set_value(object_id, field, value, object_name)

    def update_object_numerical_field(self, object_name, object_id, field, value: int or float):
        self._validate_properties_for_other_object(object_name, object_id, field, value)

        if self._is_valid_type(value, int) == False and self._is_valid_type(value, float) == False:
            raise ValueError('Value must be either an int or a float')

        self._set_value(object_id, field, value, object_name)

    def update_object_date_field(self, object_name, object_id, field, date, date_format='%d-%m-%Y'):
        self._validate_properties_for_other_object(object_name, object_id, field, date)

        formatted_date = datetime.datetime.strptime(date, date_format).strftime('%d-%m-%Y')

        self._set_value(object_id, field, formatted_date, object_name)

    def _validate_properties_for_user_object(self, user_id, field, value):
        if user_id == '' or user_id is None or user_id not in self.data['user']:
            raise ValueError('Either the User Id was not provided or this User Id was not registered yet, please register through the register_user method')
        
        if self._is_field_value_provided(field, value) == False:
            raise ValueError('Field and Value must be provided')

    def _validate_properties_for_other_object(self, object_name, object_id, field, value):
        if (object_name == '' or object_name is None) or (object_id == '' or object_id is None):
            raise ValueError('Object name and Object id must be provided')

        if self._is_field_value_provided(field, value) == False:
            raise ValueError('Field and Value must be provided')

        object_name = object_name.lower()
        if object_name not in self.data or object_id not in self.data[object_name]:
            raise ValueError("Either the provided object name or id are not registered yet, please register through the register_object method")

    def _is_field_value_provided(self, field, value):
        return (field != '' and field is not None) and (value != '' and value is not None)

    def _set_value(self, object_id, field, value, object_name):
        self.data[object_name.lower()][object_id][field.lower()] = value

    def _is_valid_type(self, value, clazz):
        return isinstance(value, clazz)

    def register_interaction(self, user_id, object_name, action, object_id):
        if (user_id == '' or user_id is None) or (object_name == '' or object_name is None) or (object_id == '' or object_id is None) or (action == '' or action is None):
            raise ValueError("User Id, Object name, Object id and action must be provided when registering an interaction")        

        if user_id not in self.data['interactions']:
            self.data['interactions'][user_id] = {}

        object_name = object_name.lower()

        if object_name not in self.data['interactions'][user_id]:
            self.data['interactions'][user_id][object_name] = {}

        if object_id not in self.data['interactions'][user_id][object_name]:
            self.data['interactions'][user_id][object_name][object_id] = []

        self.data['interactions'][user_id][object_name][object_id].append(action.lower())

    
    def add_label(self, object_name, object_id, label):
        if (object_name == '' or object_name is None) or (object_id == '' or object_id is None):
            raise ValueError('Object name and Object id must be provided')

        object_name = object_name.lower()
        if object_name not in self.data or object_id not in self.data[object_name]:
            raise ValueError("Either the provided object name or id are not registered yet, please register through the properly register method")

        if label is None:
            raise ValueError("Label must be provided")

        object_name = object_name.lower()

        if len(self.data[object_name][object_id].get('labels',[])) == 0:
            self.data[object_name][object_id]['labels'] = []

        self.data[object_name][object_id]['labels'].append(label)

    def learn_from_data(self):
        if len(self.data) == 0:
            return

        instructions_id, current_embeddings_version, instructions = \
            self.orchapi.fetch_instructions()

        self._generate_signatures(instructions)
        self.orchapi.submit_embeddings(self.embeddings, instructions_id, current_embeddings_version)

        self._reset_to_initial_state()

    def _generate_signatures(self, instructions):
        parser = ParseAndExecute(instructions)

        for object_key in self.data.keys():

            object_data = {}

            if object_key == 'interactions':
                user_interactions = self.data[object_key]
                user_interactions_embedding = {}
                for user_id in user_interactions.keys():
                    value = self.data[object_key][user_id]
                    parser.feed(value)
                    results = parser.parse(object_key)
                    if len(results) > 0:
                        user_interactions_embedding[user_id] = results

                object_data = user_interactions_embedding
            else:
                for object_id in self.data[object_key].keys():
                    value = self.data[object_key][object_id]

                    if len(value) == 0:
                        continue

                    parser.feed(value)
                    results = parser.parse(object_key)
                    if len(results) > 0:
                        object_data[object_id] = results
            
            if len(object_data) > 0: 
                if object_key not in self.embeddings:
                    self.embeddings[object_key] = {}

                self.embeddings[object_key] = object_data



    def _reset_to_initial_state(self):
        self.data = {
            "user": {},
            "interactions": {} 
        }
        self.embeddings = {}

    def recommend(self, project_id, user_id, limit = None, page = None):
        return self.orchapi.recommend(project_id, user_id, limit, page)
    
    def fake_detect(self, project_id, target_id):
        return self.orchapi.fake_detect(project_id, target_id)

    def classify(self, project_id, target_id):
        return self.orchapi.classify(project_id, target_id)

    def predict_engagement(self, project_id, user_id, object_id):
        return self.orchapi.predict_engagement(project_id, user_id, object_id)
