import json
import logging.config
from datetime import datetime
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch

from logging_k8s_metadata import setup_logging_k8s_metadata

pod_info_file_contents = {
    '/etc/podinfo/annotations': '''kubernetes.io/config.seen="2022-01-31T16:29:28.744196539Z"
kubernetes.io/config.source="api"
prometheus.io/scrape="true"''',

    '/etc/podinfo/labels': '''app="my-app"
app.kubernetes.io/component="back"
app.kubernetes.io/instance="my-app-main-dev"
app.kubernetes.io/name="my-app"
component="back"
pod-template-hash="86866cf958"''',

    '/etc/podinfo/name': 'my-app-86866cf958-flzv4',
    '/etc/podinfo/namespace': 'my-namespace',
}


def mocked_open(self, *args, **kwargs):
    return mock_open(read_data=pod_info_file_contents[str(self)])()


original_log_record_factory = logging.getLogRecordFactory()


class EnumsTestCase(TestCase):
    def tearDown(self) -> None:
        logging.setLogRecordFactory(original_log_record_factory)

    @patch.object(Path, 'open', mocked_open)
    @patch.object(Path, 'exists', MagicMock(return_value=True))
    def test_pod_info(self):
        setup_logging_k8s_metadata()
        logger = logging.getLogger('faust')
        logger.info(f'Test {datetime.now()}')

        record = logger.makeRecord(logger.name, logging.INFO, "(unknown file)", 0, 'Test', tuple(), None)

        pod_info = getattr(record, 'kubernetes', None)
        self.assertTrue(pod_info)

        pod_info = json.loads(pod_info)
        self.assertIn('annotations', pod_info)
        self.assertIsInstance(pod_info['annotations'], dict)
        self.assertIn('labels', pod_info)
        self.assertIsInstance(pod_info['labels'], dict)
        self.assertIn('name', pod_info)
        self.assertIsInstance(pod_info['name'], str)
        self.assertIn('namespace', pod_info)
        self.assertIsInstance(pod_info['namespace'], str)

    def test_no_pod_info(self):
        setup_logging_k8s_metadata()
        logger = logging.getLogger('faust')
        logger.info(f'Test {datetime.now()}')

        record = logger.makeRecord(logger.name, logging.INFO, "(unknown file)", 0, 'Test', tuple(), None)

        self.assertEqual(getattr(record, 'kubernetes', None), 'null')


def send_log():
    import logging.config
    from datetime import datetime
    import yaml

    setup_logging_k8s_metadata(metadata_dir='data/podinfo')

    logger = logging.getLogger(__name__)
    with open('logging.yml') as f:
        pass
        LOGGING = yaml.safe_load(f.read())
        # fluent lib has bug: https://github.com/fluent/fluent-logger-python/issues/189
        LOGGING['formatters']['fluent']['format']['kubernetes'] = '{kubernetes}'

    logging.config.dictConfig(LOGGING)
    try:
        raise Exception('Original exception.')
    except Exception as e:
        logger.exception(f'Some exception at {datetime.now()}')


if __name__ == '__main__':
    send_log()
