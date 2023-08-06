# runtime environment variables used by both confluent-kafka and faust implementations

from os import environ
from .env_var_generator import env_vars_creator


def default_env_vars():
    """
    Environment variables that have defaults if not specified.
    """
    return {
        'LOGLEVEL': environ.get('LOGLEVEL', 'INFO'),
        'KAFKA_CLUSTER': environ.get('KAFKA_CLUSTER', 'bifrost-kafka-bootstrap:9093'),
        'SCHEMA_REGISTRY_URL': environ.get('SCHEMA_REGISTRY_URL', 'http://bifrost-schema-registry:8081'),
        'USE_SSL': environ.get('USE_SSL', 'true'),
        'SSL_CA_LOCATION': environ.get('SSL_CA_LOCATION', '/opt/app-root/cert/client-trusted-certs/trusted-certs.pem'),
        'SSL_CERTIFICATE_LOCATION': environ.get('SSL_CERTIFICATE_LOCATION', '/opt/app-root/cert/clients-ca-cert/ca.crt'),
        'SSL_KEY_LOCATION': environ.get('SSL_KEY_LOCATION', '/opt/app-root/cert/clients-ca/ca.key'),
        'USE_SASL': environ.get('USE_SASL', 'false'),
        'SASL_USERNAME': environ.get('SASL_USERNAME', ''),
        'SASL_PASSWORD': environ.get('SASL_PASSWORD', ''),

        # Metrics Manager
        'DO_METRICS_PUSHING': environ.get('DO_METRICS_PUSHING', 'true'),
        'METRICS_PUSH_RATE': environ.get('METRICS_PUSH_RATE', '10'),
        'METRICS_SERVICE_NAME': environ.get('METRICS_SERVICE_NAME', 'bifrost-metrics-cache-headless.mktg-ops--kafka.svc.cluster.local'),
        'METRICS_SERVICE_PORT': environ.get('METRICS_SERVICE_PORT', '8080'),
        'METRICS_POD_PORT': environ.get('METRICS_POD_PORT', '9091'),

        'CONSUMER_HEARTBEAT_TIMEOUT_SECONDS': '90'}


def required_env_vars():
    """
    Environment variables that require a value (aka no default specified).
    """
    return {
        'HOSTNAME': environ['HOSTNAME'],  # NOTE: Every Openshift pod has a default HOSTNAME (its own pod name).
        'APP_NAME': environ['NU_APP_NAME']}


def all_env_vars():
    return {
        **default_env_vars(),
        **required_env_vars()
    }


env_vars = env_vars_creator(all_env_vars)
