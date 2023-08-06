from jaeger_client import Config
from rasa.constants import ENV_JAEGER_REPORTING_HOST, ENV_JAEGER_REPORTING_PORT

def get_config(service):
    return Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'local_agent': {
                'reporting_host': ENV_JAEGER_REPORTING_HOST,
                'reporting_port': ENV_JAEGER_REPORTING_PORT,
            }
        },
        service_name=service)


def initialize_tracer(service):
    return get_config(service).initialize_tracer()  # also sets opentracing.tracer


class ConversationTracer(object):
    __instance = None

    @staticmethod
    def get_instance():
        if ConversationTracer.__instance is not None:
            return ConversationTracer.__instance

        return ConversationTracer('conversation-writer')

    def __init__(self, service):
        if ConversationTracer.__instance is not None:
            raise Exception("Instance has been initialized. Please use get_instance() instead.")

        self.tracer = get_config(service).new_tracer()
        ConversationTracer.__instance = self


class CueTracer(object):
    __instance = None

    @staticmethod
    def get_instance():
        if CueTracer.__instance is not None:
            return CueTracer.__instance

        return CueTracer('cue-writer')

    def __init__(self, service):
        if CueTracer.__instance is not None:
            raise Exception("Instance has been initialized. Please use get_instance() instead.")

        self.tracer = get_config(service).new_tracer()
        CueTracer.__instance = self


class UpmTracer(object):
    __instance = None

    @staticmethod
    def get_instance():
        if UpmTracer.__instance is not None:
            return UpmTracer.__instance

        return UpmTracer('upm-writer')

    def __init__(self, service):
        if UpmTracer.__instance is not None:
            raise Exception("Instance has been initialized. Please use get_instance() instead.")

        self.tracer = get_config(service).new_tracer()
        UpmTracer.__instance = self


conversation_tracer = ConversationTracer.get_instance().tracer
cue_tracer = CueTracer.get_instance().tracer
upm_tracer = UpmTracer.get_instance().tracer
