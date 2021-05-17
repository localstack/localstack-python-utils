# LOCALSTACK-UTILS
Python utility to integrate Localstack with Unit tests.

### Prerequisites
- Docker
- Localstack


### Instalation (soon...)

### Usage example

``` python
import time
import boto3
import unittest
from localstack_utils import startup_localstack, stop_localstack

class kinesis_test(unittest.TestCase):
        def setUp(self):
            startup_localstack()
            session = boto3.session.Session()

        def tearDown(self):
            stop_localstack()
            return super().tearDown()

        def test_create_stream(self):
            kinesis = boto3.client(
                service_name='kinesis',
                aws_access_key_id='test',
                aws_secret_access_key='test',
                endpoint_url='http://localhost:4566')

            kinesis.create_stream(StreamName='test', ShardCount=1)
            time.sleep(5)

            response = kinesis.list_streams()
            self.assertGreater(len(response.get('StreamNames', [])),0)
```
