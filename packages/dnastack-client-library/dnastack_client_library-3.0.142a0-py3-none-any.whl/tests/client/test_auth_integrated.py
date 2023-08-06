from uuid import uuid4

from typing import Any, Dict, List

from dnastack import DataConnectClient
from dnastack.client.collections.client import STANDARD_COLLECTION_SERVICE_TYPE_V1_0, CollectionServiceClient
from dnastack.client.data_connect import DATA_CONNECT_TYPE_V1_0
from dnastack.client.service_registry.models import ServiceType
from dnastack.common.environments import env
from dnastack.common.events import Event
from dnastack.configuration.models import ServiceEndpoint
from tests.exam_helper import BaseTestCase, client_id, client_secret, token_endpoint, EventCollector


class TestOAuth2AuthenticatorIntegrationTest(BaseTestCase):
    test_collection_service_url = env('E2E_COLLECTION_SERVICE_URL',
                                      default='https://collection-service.viral.ai/')

    test_data_connect_url = env('E2E_PROTECTED_DATA_CONNECT_URL',
                                default='https://collection-service.viral.ai/data-connect/')

    def test_auth_info_consolidation(self):
        """
        Test auth info consolidation.

        In this scenario, there should be only one authentication initiated.
        """
        event_collector = EventCollector(['authentication-before',
                                          'authentication-ok',
                                          'authentication-failure',
                                          'refresh-before',
                                          'refresh-ok',
                                          'refresh-failure',
                                          'session-restored',
                                          'session-not-restored',
                                          'session-revoked'])

        cs = CollectionServiceClient.make(self.__create_endpoint('test-collection-service',
                                                                 STANDARD_COLLECTION_SERVICE_TYPE_V1_0,
                                                                 self.test_collection_service_url))
        dc = DataConnectClient.make(self.__create_endpoint('test-data-connect',
                                                           DATA_CONNECT_TYPE_V1_0,
                                                           self.test_data_connect_url))

        event_collector.prepare_for_interception(cs)
        event_collector.prepare_for_interception(dc)

        # Trigger the authentication and confirm that some clients are still working normally.
        self.assert_not_empty([collection.slugName for collection in cs.list_collections()])  # First round
        self.assert_not_empty([row for row in dc.query('SELECT 1 AS x')])  # Second round
        self.assert_not_empty([row for row in dc.query('SELECT 3 AS x')])  # Third round)

        self.assertEqual([s.type for s in event_collector.sequence],
                         ['session-not-restored', 'authentication-before', 'authentication-ok'])

    def __create_endpoint(self, id: str, type: ServiceType, url: str) -> ServiceEndpoint:
        return ServiceEndpoint(
            id=id,
            type=type,
            url=url,
            authentication=dict(
                type='oauth2',
                client_id=client_id,
                client_secret=client_secret,
                grant_type='client_credentials',
                resource_url=f'{self.test_collection_service_url} {self.test_data_connect_url}',
                token_endpoint=token_endpoint,
            ),
        )

    def __create_event_interceptor(self, client_events: List[str], event_type):
        def intercept(event: Event):
            self._logger.debug(f'Intercepted E/{event_type}: {event}')
            client_events.append(event_type)

        return intercept
