import json

from ..utils.syft import Syft
from ..orchapi.api import OrchAPI
from ..conn.mqtt import MQTTClient


class ExecuteRemoteCompute(Syft, OrchAPI):
    def __init__(self, device_id):
        self.id = device_id
        self.model_params = None
        self.func = None
        self.reply_address = None
        self.reply_connector = None
        # to be set by the user.
        self.model_executor = None
        self.compute_executor = None
        self.participant_id = None
        # state to not run two rounds async.
        self.is_in_round = False

    def connection_info(self):
        # https://github.com/OpenMined/PySyft/blob/3f4388bf3309fcb154ea32d365265bf808cdac6b/syft/workers/model_centric_fl_worker.py#L241
        pass

    def request_participation(self):
        res = self._request_participation_in_cycle(self.id, self.job_id, self.cycle_seq)
        if not res['success']:
            return False, res['message']
        if res['result'].get('participant_id'):
            self.participant_id = res['result'].get('participant_id')
            return True, "accepted"
        return False, "uknown reason"

    def verify_key(self, key):
        """
        TODO: introduce jwt tokens for authentication.
        """
        return

    def process_message(self, msg):
        print("processing request")
        if self.is_in_round:
            print("ignoring message, as I'm working currently.")
            return

        self.is_in_round = True

        func = msg.get('func')
        model_params = msg.get('model_params', None)
        epochs = msg.get('epochs', 1)
        batch_size = msg.get('batch_size')
        lr = msg.get('learning_rate', 0)
        type = msg.get('type')
        # Identification data.
        self.job_id = msg.get('job_id')
        self.cycle_seq = msg.get('cycle_seq')
        print("going to request to participate")
        # decide to participate
        if msg.get('auth_required'):
            can_participate, _participation_msg = self.request_participation()
            if not can_participate:
                self.is_in_round = False
                self._reset()
                print("cannot participate, skipping round ", _participation_msg)
                return

        # allow for jwt tokens
        # if msg.get('auth_key'):
        #    good = self.verify_key(msg.get('auth_key'))
        #    if not good:
        #        return

        # parse plan
        self.func = self._parse_plan(func)

        if model_params and type == 'model':
            self.model_params = self._parse_params(model_params)
        # where to send back.
        # TODO support sending back through other protocols.
        self.reply_address = msg.get('reply_address')
        self.reply_connector = msg.get('reply_connector')
        if type == 'model':
            try:
                updated_model_params = self.model_executor(
                    training_func = self.func.torchscript,
                    model_params = self.model_params,
                    batch_size = batch_size,
                    epochs = epochs,
                    learning_rate = lr
                )
                diff = self.calculate_model_params_diff(updated_model_params)
                self.report(diff)
            except Exception as e:
                print("failed to excute due to exception in executor, e: ", e)
                self._reset()

        elif type == 'compute':
            try:
                results = self.compute_executor(
                    func = self.func
                )
                self.report(results)
            except Exception as e:
                print("failed to excute due to exception in executor, e: ", e)
                self._reset()

    def calculate_model_params_diff(self, updated_model_params: list):
        # Calc params diff
        orig_params = self.model_params
        diff_params = [orig_params[i] - updated_model_params[i] for i in range(len(orig_params))]

        return diff_params

        # Wrap diff in State
        #diff_ph = [PlaceHolder().instantiate(t) for t in diff_params]
        #diff = State(state_placeholders=diff_ph)

        #response = self.grid_worker.report(
        #    worker_id=self.fl_client.worker_id,
        #    request_key=self.cycle_params["request_key"],
        #    diff=diff,
        #)

    def _reset(self):
        """
        reset to allow for next round.
        """
        self.participant_id = None
        self.job_id = None
        self.cycle_seq = None
        self.model_params = None
        self.func = None
        self.reply_address = None
        self.reply_connector = None
        self.is_in_round = False

    def report(self, updates):
        # add edge id.
        if type(updates) == list:
            states = self.convert_list_updates_to_states(updates)
        else:
            states = self.convert_updates_to_states(updates)
        serialized = self.serialize_to_sendable(states)
        msg = {
            'device_id': self.id,
            'participant_id': self.participant_id,
            'updates': str(serialized),
            'job_id': self.job_id,
            'cycle_seq': self.cycle_seq
        }

        self._send_report(msg)
        self._reset()


class ExecuteRemoteComputeMQTT(ExecuteRemoteCompute, MQTTClient):
    def configure_client_connection(self, host, port):
        """
        configure MQTT connection.
        """
        self.host = host
        self.port = port
        self._connect()

    def start(self):
        if not (self.model_executor or self.compute_executor):
            raise Exception("Cannot start without a model_executor or compute_executor specified.")
        self._start()

    def _send_report(self, report):
        self._send_msg(self.reply_address, json.dumps(report))
