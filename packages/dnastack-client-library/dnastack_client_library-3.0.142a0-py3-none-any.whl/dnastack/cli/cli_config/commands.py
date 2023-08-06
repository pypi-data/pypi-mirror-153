import click
import json

from dnastack.cli.utils import command
from dnastack.cli.endpoints import endpoint_command_group
from dnastack.cli.service_registry import registry_command_group
from dnastack.client.collections.client import CollectionServiceClient
from dnastack.client.data_connect import DataConnectClient
from dnastack.client.drs import DrsClient
from dnastack.client.service_registry.client import ServiceRegistry
from dnastack.configuration.models import Configuration

_full_schema = Configuration.schema()

service_adapter_types = [
    CollectionServiceClient.get_adapter_type(),
    DataConnectClient.get_adapter_type(),
    DrsClient.get_adapter_type(),
    ServiceRegistry.get_adapter_type(),
]


@click.group("config")
def config_command_group():
    """ Manage global configuration """


@command(config_command_group, "schema")
def config_schema():
    """Show the schema of the configuration file"""
    click.echo(json.dumps(_full_schema, indent=2, sort_keys=True))

# noinspection PyTypeChecker
config_command_group.add_command(registry_command_group)
# noinspection PyTypeChecker
config_command_group.add_command(endpoint_command_group)
