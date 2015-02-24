"""
Studreg, Hafakulta's student union membership management system.

Copyright (C) 2014,2015 Yuval Langer.

This file is part of Studreg.

Studreg is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Studreg is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Studreg.  If not, see <http://www.gnu.org/licenses/>.
"""


from __future__ import print_function
import os
import unittest
import config
import tempfile

try:
    import simplejson as json
except ImportError:
    import json

import requests


def make_post_request(data):
    username = 'copy_people'
    password = config.local_config.api_user['copy_people']
    return requests.post(
        'https://aguda.org.il/studreg/api/beta/membership_status',
        auth=(username, password),
        data=data,
    )


def make_get_request(params):
    username = 'copy_people'
    password = config.local_config.api_user['copy_people']
    return requests.get(
        'https://aguda.org.il/studreg/api/beta/membership_status',
        auth=(username, password),
        params=params,
    )


class StudregTestCase(unittest.TestCase):
    def setUp(self):
        self.config = config

    def test_failing(self):
        assert False

    def test_no_id(self):
        data = dict(
            email='yuval.langer@gmail.com',
        )
        r = make_post_request(data)

        result = json.loads(r.text)
        expected = json.loads('{"student_existence": "student_missing"}')

        print(result)
        print(expected)

        assert result == expected

    def test_exists_and_agudaorg_member(self):
        data = dict(
            email='doron.zaada@mail.huji.ac.il',
        )
        r = make_post_request(data)

        result = json.loads(r.text)
        expected = json.loads('{"aguda_membership_status": "member"}')

        print(result)
        print(expected)

        assert result == expected

    def test_get_no_id(self):
        params = dict(
            email='yuval.langer@gmail.com',
        )
        r = make_get_request(params=params)

        result = json.loads(r.text)
        expected = json.loads('{"student_existence": "student_missing"}')

        print(result)
        print(expected)

        assert result == expected

    def test_get_exists_and_agudaorg_member(self):
        params = dict(
            email='doron.zaada@mail.huji.ac.il',
        )
        r = make_get_request(params=params)

        result = json.loads(r.text)
        expected = json.loads('{"aguda_membership_status": "member"}')

        print(result)
        print(expected)

        assert result == expected
if __name__ == '__main__':
    unittest.main()
