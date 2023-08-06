from tests.cli.base import CliTestCase


class TestConfiguration(CliTestCase):
    def test_happy_path(self):
        # No assertion here as long as nothing throws an error.
        self.invoke('endpoints', 'add', '-t', 'collections', 'sample:viral-ai:cs')
        self.invoke('endpoints', 'set', 'sample:viral-ai:cs', 'url', 'https://viral.ai/api/')

        self.invoke('collections', 'list')
        self.invoke('collections', 'tables', 'list', '--collection', 'ncbi-sra')
        self.invoke('collections', 'query', '--collection', 'ncbi-sra', 'SELECT 1')
