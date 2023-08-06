import asyncio
import inspect
import json
from functools import wraps

import yaml
from aiokit import AioThing
from grpc import StatusCode
from grpc.experimental.aio import insecure_channel
from izihawa_utils.pb_to_json import MessageToDict


def expose(fn=None, with_from_file=False):
    if fn:
        fn._exposable = True
        fn._with_from_file = False
    else:
        def real_expose(fn):
            return expose(fn=fn, with_from_file=with_from_file)
        return real_expose


def from_file(method):
    def inner(file_path):
        with open(file_path, 'rb') as f:
            file_data = f.read()
        if file_path.endswith('.yaml') or file_path.endswith('.yml'):
            data = yaml.safe_load(file_data)
        elif file_path.endswith('.json'):
            data = json.loads(file_data)
        else:
            raise ValueError(f'Unknown format for `{file_path}`, only `json`, `yml` or `json` are supported')
        return method(**data)
    return inner


def format_json(response):
    return json.dumps(MessageToDict(response, bytes_to_unicode=True, preserving_proto_field_name=True), indent=2)


def format_yaml(response):
    return yaml.safe_dump(
        MessageToDict(response, bytes_to_unicode=True, preserving_proto_field_name=True),
        default_flow_style=False,
    ).rstrip('\n')


fmt = {
    'json': format_json,
    'yaml': format_yaml,
}


def add_format(fn):
    oldsig = inspect.signature(fn)
    params = list(oldsig.parameters.values())
    for i, param in enumerate(params):
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            break
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            break
    else:
        i = len(params)
    name = 'format'
    while name in oldsig.parameters:
        name += '_'
    newparam = inspect.Parameter(name,
                                 inspect.Parameter.KEYWORD_ONLY,
                                 default='json')
    params.insert(i, newparam)
    sig = oldsig.replace(parameters=params)

    @wraps(fn)
    async def exposing_wrapper(self, *args, **kwargs):
        bound = sig.bind(self, *args, **kwargs)
        bound.apply_defaults()
        format = bound.arguments[name]
        del bound.arguments[name]
        result = await fn(*bound.args, **bound.kwargs)
        print(fmt[format](result))

    exposing_wrapper.__signature__ = sig
    return exposing_wrapper


class BaseGrpcClient(AioThing):
    temporary_errors = (
        StatusCode.CANCELLED,
        StatusCode.UNAVAILABLE,
    )
    stub_clses = {}

    def __init__(
        self,
        endpoint,
        max_retries: int = 2,
        retry_delay: float = 0.5,
        connection_timeout: float = None,
    ):
        super().__init__()
        if endpoint is None:
            raise RuntimeError(f'`endpoint` must be passed for {self.__class__.__name__} constructor')
        config = [
            ('grpc.dns_min_time_between_resolutions_ms', 1000),
            ('grpc.initial_reconnect_backoff_ms', 1000),
            ('grpc.lb_policy_name', 'pick_first'),
            ('grpc.min_reconnect_backoff_ms', 1000),
            ('grpc.max_reconnect_backoff_ms', 2000),
            ('grpc.service_config', json.dumps({'methodConfig': [{
                'name': [{}],
                'retryPolicy': {
                    'maxAttempts': max_retries,
                    'initialBackoff': f'{retry_delay}s',
                    'maxBackoff': f'{retry_delay}s',
                    'backoffMultiplier': 1,
                    'retryableStatusCodes': list(map(lambda x: x.name, self.temporary_errors)),
                }
            }]}))
        ]
        self.connection_timeout = connection_timeout
        self.channel = insecure_channel(endpoint, config)
        self.stubs = {}
        for stub_name, stub_cls in self.stub_clses.items():
            self.stubs[stub_name] = stub_cls(self.channel)

    async def start(self):
        await asyncio.wait_for(self.channel.channel_ready(), timeout=self.connection_timeout)

    async def stop(self):
        await self.channel.close()

    def get_interface(self):
        interface = {}
        for method_name in dir(self):
            method = getattr(self, method_name)
            if callable(method) and getattr(method, '_exposable', False):
                interface[method_name.replace('_', '-')] = add_format(method)
                if getattr(method, '_with_from_file'):
                    interface[method_name.replace('_', '-') + '-from-file'] = from_file(add_format(method))
        return interface
