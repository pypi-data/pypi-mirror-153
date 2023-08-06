from ..conn.mqtt import MQTTClient
from ..orchapi.api import OrchAPI
from ..utils.syft import Syft

# API
class BaseRemoteCompute(Syft):
    def __init__(self):
        self.id = None # when the compute is submitted, it'll get an id.

    def fetch_compute_status(self):
        if not self.id:
            return "this compute is not requested yet."
        return self._get_status(self.id)


class MQTTRemoteCompute(BaseRemoteCompute, MQTTClient):
    def configure_client_connection(self, host, port):
        """
        configure MQTT connection.
        """
        self.host = host
        self.port = port

    def set_broadcast_channel(self, channel):
        self.topic = channel

    def _send_compute(self, msg):
        self.send_msg(msg)

    def _get_status(self, id):
        raise NotImplementedError("status over mqtt are not implemented")

class RemoteCompute(BaseRemoteCompute, OrchAPI):
    # HTTP, assuming Begin AI server will relay the msg.
    def _send_compute(self, msg):
        """
        msg: dictionary holding values (plan and model_params where applicable)
        """
        return self._create_job(msg)

    def _get_status(self, compute_group_id):
        return self._get_job_status(compute_group_id)

    def get_last_checkpoint(self, job_id):
        res = self._get_last_checkpoint(job_id)
        if res['result']:
            checkpoint = res['result']['checkpoint'][0]
            checkpoint['aggr'] = self._parse_params(checkpoint['aggr'])
            return checkpoint
        return res

    def submit_compute(self, func, configs, initial_values, model_params = None):
        msg = self.prepare_compute(self.type, func, configs, initial_values, model_params = model_params)
        res = self._send_compute(msg)
        # get id from res.
        # self.id = res.id
        return res
