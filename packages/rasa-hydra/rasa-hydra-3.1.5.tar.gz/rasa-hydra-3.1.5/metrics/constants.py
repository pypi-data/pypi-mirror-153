from prometheus_client import Gauge, Histogram, Counter

# Create a metric to track time spent and requests made.
REQUEST_TIME = Histogram('request_processing_seconds', 'Time spent processing request', ['app', 'method', 'endpoint'])
CURRENT_USER = Gauge('current_users', 'Total number of current users', ['channel'], multiprocess_mode='livesum')
CHAT_LATENCY = Histogram('chat_latency_seconds_histogram', 'Latency of a chat response', ['channel', 'endpoint'])
OUTGOING_REQUEST_LATENCY_SEC = Histogram(
    'outgoing_request_latency_sec',
    'Latency of the requests to other applications',
    ['endpoint', 'http_status', 'method']
)
ACTION_PREDICT_EXECUTE_TIME = Histogram('next_action_prediction_execute_time', 'Time taken to predict and execute next action')

APP_NAV = Counter(
    'app_nav',
    'Number of nlu prompts and a sum of their corresponding results',
    ['prompt', 'result', 'asr_engine']

)