import requests
import urllib.parse
from enum import Enum

class _URL(Enum):
    FETCH_INSTRUCTIONS_URL = "/{}/fetch"
    SUBMIT_EMBEDDING_URL = "/embeddings/{}/embedding"
    SUBMIT_EMBEDDING_BATCH_URL = "/embeddings/{}/embedding/batch"
    RECOMMENDATION_URL = "/{}/recommend/{}"
    FAKE_DETECTION_URL = "/{}/detect_fake/{}"
    CLASSIFY_URL = "/{}/classify/{}"
    PREDICT_ENGAGEMENT_URL = "/{}/predict_engagement/{}/{}"
    TRAINING_RESULTS_URL = "/{}/training_report/"

class OrchAPI(object):
    """
    interacts with orchestrator end points.
    """
    def __init__(self):
        self.project_id = None
        self.compute_group_id = None
        self.host = None
        self.token = None

    def configure_orch_connection(self, host, port = None):
        if port is None:
            self.host = host
        else:
            self.host = "{}:{}".format(host, port)

    def set_token(self, token):
        self.token = token

    def set_app_id_and_license_key(self, license_key, app_id):
        self.app_id = app_id
        self.license_key = license_key

    def _send_post(self, uri, msg):
        """
        msg: dictionary holding values as expected by the end point.
        """
        headers = {"AppID": self.app_id, "LicenseKey": self.license_key}        
        res = requests.post(self.host + uri, json = msg, headers=headers)

        if res.status_code == 401:
            raise ValueError('App ID/License Key are invalid, please check your application credentials')

        return res.json()

    def _send_get(self, uri, query_str_obj = {}):
        """
        query_str_obj: dictionary holding values as expected by the end point.
        """
        headers = {"AppID": self.app_id, "LicenseKey": self.license_key}

        url = self.host + uri

        if query_str_obj is not None:
            query_str = urllib.parse.urlencode(query_str_obj)
            url += '?' + query_str

        res = requests.get(url, headers=headers)

        if res.status_code == 401:
            raise ValueError('App ID/License Key are invalid, please check your application credentials')

        results = res.json()

        empty_results = { 'results': [] }
        if results is None or results == 500:
            return empty_results
        if results['success'] == False:
            return empty_results

        return results['result']

    def create_project(self, name, description):
        """
        args:
            name: project name
            description: project description
        """
        return self._send_post('/project/', {'name':name, 'description': description})

    def create_compute_group(self, name, description, type):
        """
        args:
            name: project name
            description: project description
            type: (compute or model) this determines if training is required
                for jobs in this group.
        """
        if not self.project_id:
            return {'err': 'must set project id first'}
        return self._send_post('/project/{}/compute_group/'.format(self.project_id),
            {'name':name, 'type': type, 'description': description})

    def set_project(self, id):
        self.project_id = id

    def set_compute_group(self, id):
        # get the compute group and set self.type
        group = self.get_compute_group(id)
        if not group['result'] or not len(group['result']['compute_groups']):
            return "Group Not Found"
        self.compute_group_id = id
        self.type = group['result']['compute_groups'][0]['type']

    def get_projects(self):
        return self._send_get('/project/all/')

    def get_compute_groups(self):
        if not self.project_id:
            return {'err': 'Must set project first.'}
        return self._send_get('/project/{}/compute_group/all/'.format(self.project_id))

    def get_compute_group(self, id):
        if not self.project_id:
            return {'err': 'Must set project first.'}
        return self._send_get('/project/{}/compute_group/{}/'.format(self.project_id, id))

    def create_channel(self, name, address):
        return self._send_post('/channels/', {'name':name, 'address': address})

    def get_channels(self):
        # include job filter.
        return self._send_get('/channels/all/')

    def get_active_jobs(self):
        if not self.project_id or not self.compute_group_id:
            return {'err': 'Must set project and compute group first.'}
        return self._send_get('/jobs/active/')

    def _create_job(self, kwargs):
        """
        #TODO validate params for the type of the job.
        """
        if not self.compute_group_id:
            return {'err': 'Must set project and compute group first.'}

        # hack for datetime.
        d = kwargs.get('keep_until', None)
        if d:
            kwargs['keep_until'] = kwargs['keep_until'].__str__()
        return self._send_post('/jobs/{}/'.format(self.compute_group_id), kwargs)

    def _get_job_status(self, job_id):
        pass

    def _get_last_checkpoint(self, job_id):
        return self._send_get('/jobs/{}/checkpoint/last/'.format(job_id))

    def _request_participation_in_cycle(self, device_id, job_id, cycle_seq):
        return self._send_post('/cycles/{}/cycle/{}/'.format(job_id, cycle_seq),
            msg = {'device_id': device_id})

    # embeddings related stuff.
    def submit_schema(self, schema_dict):
        schema = {"schema" : schema_dict}
        self._send_post("/embeddings/{}/schema".format(self.app_id), msg=schema)

    def fetch_instructions(self):
        results = self._send_get(_URL.FETCH_INSTRUCTIONS_URL.value.format(self.app_id))
        if 'instructions' not in results:
            raise Exception('Instruction not found for the App ID provided')

        instructions = results['instructions'][0]
        instructions_id = instructions['instruction_id']
        version_number = instructions['version']
        return instructions_id, version_number, instructions

    def submit_embeddings(self, embeddings, instruction_id, version_number):
        data = {
            "embeddings": embeddings,
            "version_number": version_number
        }
        res = self._send_post(_URL.SUBMIT_EMBEDDING_URL.value.format(instruction_id), msg=data)
        return res['result']

    def submit_embeddings_batch(self, embeddings, instr_id, version_number, type, target_object, update = False):
        data = {
            "version_number": version_number,
            "embeddings": embeddings,
            "type": type,
            "target_object": target_object,
            "update": update,
        }
        return self._send_post(_URL.SUBMIT_EMBEDDING_BATCH_URL.value.format(instr_id), msg=data)

    def infer(self, embedding, project_id):
        data = {
            "embedding": embedding
        }
        res = self._send_post("/embeddings/{}/inference".format(project_id), msg=data)
        return res['result']

    def recommend(self, project_id, user_id, limit = None, page = None):
        pagination = {}

        if limit is not None:
            pagination['limit'] = limit
        if page is not None:
            pagination['page'] = page

        return self._send_get(_URL.RECOMMENDATION_URL.value.format(project_id, user_id), pagination)['results']
    
    def fake_detect(self, project_id, target_id):
        results = self._send_get(_URL.FAKE_DETECTION_URL.value.format(project_id, target_id))['results']
        if len(results) == 0:
            return "NOT_FOUND"
        return results

    def classify(self, project_id, target_id):
        results = self._send_get(_URL.CLASSIFY_URL.value.format(project_id, target_id))['results']
        if len(results) == 0:
            return "NOT_FOUND"
        return results

    def predict_engagement(self, project_id, user_id, object_id):
        results = self._send_get(_URL.PREDICT_ENGAGEMENT_URL.value.format(project_id, user_id, object_id))['results']
        return self._process_results_or_return_not_found(results)

    def training_results(self, project_id ):
        return self._send_get(_URL.TRAINING_RESULTS_URL.value.format(project_id))

    def _process_results_or_return_not_found(self, results):
        if isinstance(results, list):
            return "NOT_FOUND"

        return results

class StreamingAPI(object):
    """
    this is to get live updates on socket on a job.
    """
    pass
