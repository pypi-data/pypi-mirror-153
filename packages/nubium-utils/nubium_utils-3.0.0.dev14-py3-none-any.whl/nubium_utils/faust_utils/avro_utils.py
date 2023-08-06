import json

from schema_registry.client import SchemaRegistryClient, schema
from schema_registry.serializers import FaustSerializer
from .faust_runtime_vars import env_vars


def get_avro_client() -> SchemaRegistryClient:
    """
    Configures a client for the schema registry using an environment variable
    :return: (SchemaRegistryClient)
    """
    return SchemaRegistryClient(url=env_vars()['SCHEMA_REGISTRY_URL'])


def key_serializer(client) -> FaustSerializer:
    """
    Creates Faust Serializer for generic string schema
    """
    return FaustSerializer(schema_registry_client=client,
                           schema_subject='generic_faust_avro_key',
                           schema=schema.AvroSchema('''{"type":"string"}'''))


def value_serializer(client, topic, schema_dict):
    return FaustSerializer(schema_registry_client=client,
                           schema_subject=topic,
                           schema=schema.AvroSchema(json.dumps(schema_dict)))
