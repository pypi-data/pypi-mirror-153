from syft_proto.execution.v1.plan_pb2 import Plan as PlanPB
from syft_proto.execution.v1.state_pb2 import State as StatePB

from syft.execution.state import State
from syft.execution.placeholder import PlaceHolder
from syft.execution.plan import Plan

from syft.serde import protobuf
import binascii
import syft as sy

import torch as th
import json

#hook = sy.TorchHook(th)  # hook PyTorch ie add extra functionalities
sy.make_hook(globals())

# force protobuf serialization for tensors
hook.local_worker.framework = None
th.random.manual_seed(1)

class Syft(object):
    def convert_list_updates_to_states(self, model_params):
        model_params_state = State(
            state_placeholders=[
                PlaceHolder().instantiate(param)
                for param in model_params
            ]
        )
        return model_params_state

    def convert_updates_to_states(self, tensor):
        return State(state_placeholders=[PlaceHolder().instantiate(tensor)])

    def convert_func_to_plan(self, func, args_shape=None, state=None, trace_autograd=False,
        args_dtypes=()):

        args_shape = args_shape
        args_dtypes = args_dtypes
        state_tensors = state or ()
        # include_state is used to distinguish if the initial plan is a function or a class:
        # if it's a function, then the state should be provided in the args, so include_state
        # will be true. And to know if it was indeed a function, we just need to see if a
        # "manual" state was provided.
        include_state = state is not None
        trace_autograd = trace_autograd

        plan = Plan(
            name=func.__name__,
            include_state=False,
            forward_func=func,
            state_tensors=(),
            id=sy.ID_PROVIDER.pop(),
            owner=sy.local_worker,
        )

        # Build the plan automatically
        if args_shape:
            args_ = PlaceHolder.create_placeholders(self.args_shape, self.args_dtypes)
            try:
                plan.build(*args_, trace_autograd=self.trace_autograd)
            except TypeError as e:
                raise ValueError(
                    "Automatic build using @func2plan failed!\nCheck that:\n"
                    " - you have provided the correct number of shapes in args_shape\n"
                    " - you have no simple numbers like int or float as args. If you do "
                    "so, please consider using a tensor instead."
                )

        return plan

    def _sendable_ser_step1(self, obj):
        worker = hook.local_worker
        pb = protobuf.serde._bufferize(worker, obj)
        return pb.SerializeToString()

    def _sendable_ser_step2(self, obj):
        # hexlified = binascii.hexlify(msg).decode()
        return str(binascii.hexlify(obj))

    def serialize_to_sendable(self, obj):
        msg = self._sendable_ser_step1(obj)
        msg = self._sendable_ser_step2(msg)
        return msg

    def _parse_plan(self, plan_hex):
        pb = PlanPB()
        unhex = binascii.unhexlify(plan_hex.strip()[2:-1])
        pb.ParseFromString(unhex)
        plan = protobuf.serde._unbufferize(hook.local_worker, pb)
        return plan

    def _parse_params(self, model_params_hex):
        pb = StatePB()
        unhex = binascii.unhexlify(model_params_hex.strip()[2:-1])
        pb.ParseFromString(unhex)
        model_params_state = protobuf.serde._unbufferize(hook.local_worker, pb)
        model_params = model_params_state.tensors()
        return model_params

    def prepare_compute(self, type, func, configs, initial_values, model_params = None):
        """
        assumes the channel is already configured.
        func: the training or compute function
        type: int: 1,2 (where 1 is compute, and 2 is training)
        initial_values: dictionary of args with values to build the func.
        model_params: initial params for the model if type is model.
        """
        # 1. build the plan.
        trace_autograd = True if type == 'model' else False
        plan = self.convert_func_to_plan(func, trace_autograd = trace_autograd)

        if not plan.is_built:
            plan.build(*initial_values, trace_autograd = trace_autograd)

        # 2. serialize the plan.
        ser_plan = self.serialize_to_sendable(plan)
        msg = {
            "compute_func": str(ser_plan),
        }

        if type == 'model': # model
            if not model_params:
                raise Exception("Must provide initial model parameters !")

            serialized_params = self.serialize_to_sendable(self.convert_list_updates_to_states(model_params))
            msg.update({"model_params": str(serialized_params)})

        # 3 add configs
        msg.update(configs)
        return msg
