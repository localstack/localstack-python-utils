import time
import boto3
import unittest
from localstack_utils.localstack import startup_localstack, stop_localstack


class TestKinesis(unittest.TestCase):
    def setUp(self):
        startup_localstack(image_name="localstack/localstack")

    def tearDown(self):
        stop_localstack()
        return super().tearDown()

    def test_create_stream(self):
        kinesis = boto3.client(
            service_name="kinesis",
            aws_access_key_id="test",
            aws_secret_access_key="test",
            endpoint_url="http://localhost:4566",
        )

        kinesis.create_stream(StreamName="test", ShardCount=1)
        time.sleep(1)

        response = kinesis.list_streams()
        self.assertGreater(len(response.get("StreamNames", [])), 0)
