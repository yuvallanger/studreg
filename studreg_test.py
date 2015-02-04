import os
import unittest
import config
import tempfile

def make_request(data):
    username = 'copy_people'
    password = config.local_config.api_user['copy_people']
    return request(
        'http://127.0.0.1:5002',
        auth=(username, password),
        data=data
    )

class StudregTestCase(unittest.TestCase):
    def setUp(self):
        self.config = config

    def test_failing(self):
        assert False

    def login(self, username, password):
        return self.app.post()

if __name__ == '__main__':
    unittest.main()