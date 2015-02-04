import os
import studreg
import unittest
import tempfile

class StudregTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, studreg.app.config['DATABASE'] = tempfile.mkstemp()
        studreg.app.config['TESTING'] = True
        self.app = studreg.app.test_client()
        studreg.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(studreg.app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post()

if __name__ == '__main__':
    unittest.main()