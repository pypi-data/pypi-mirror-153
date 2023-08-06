import json
import unittest
from dbaas_aclapi.acl_base_client import AclClient, GET


class Response(object):

    def __init__(self, data):
        self.data = json.dumps(data)

    def getheaders(self):
        return {'headers': 'ok'}


class FakeUrllib3PoolManager(object):
    def __init__(self, *args, **kwargs):
        self._calls = []

    def _append_call(self, method, url, payload=None, timeout=None):
        self._calls.append((method, url, payload, timeout))

    def request(self, method, url, headers, timeout=None):
        self._append_call(method, url, None, timeout)
        return Response({'test': 'ok'})

    def urlopen(self, method, body, url, headers):
        self._append_call(method, url, body)
        return Response({'test': 'ok'})

    @property
    def calls(self):
        return self._calls


class AclApiStub(AclClient):

    def __init__(self, *args, **kwargs):
        super(AclApiStub, self).__init__(*args, **kwargs)
        self._http_pool = FakeUrllib3PoolManager()

    def _make_request(self, endpoint, http_verb=GET, payload=None, timeout=None):
        super(AclApiStub, self)._make_request(
            endpoint, http_verb=http_verb, payload=payload, timeout=timeout
        )
        response = Response({'response': True})
        if endpoint.endswith('/acl/search'):
            json_dict = {
                "envs": [{
                    "kind": "default#acl",
                    "environment": "13912",
                    "rules": [{
                        "id": "68",
                        "action": "permit",
                        "protocol": "ip",
                        "source": "0.0.0.0/0",
                        "destination": "10.70.1.80/32"
                    }],
                    "vlans": [{
                        "kind": "object#acl",
                        "environment": "13912",
                        "num_vlan": 8,
                        "rules": [{
                            "id": "98920",
                            "sequence": 9,
                            "action": "permit",
                            "protocol": "tcp",
                            "source": "10.236.250.0/24",
                            "destination": "10.70.1.80/32",
                            "l4-options": {
                                "dest-port-op": "eq",
                                "dest-port-start": "22"
                            },
                        }]
                    }]
                }]
            }
            response = Response(json_dict)
        return response

    @property
    def last_request(self):
        return self._http_pool.calls[-1]


class AclApiTestCase(unittest.TestCase):

    def setUp(self):
        self.base_url = 'https://acl_api.mock.test.globoi.globo.com/'
        self.username = 'dbaas'
        self.password = 'dbaas'
        self.database_environment = 'dev'
        self.ip_version = 4
        self.acl_api_client = AclApiStub(
            self.base_url, self.username, self.password,
            self.database_environment, self.ip_version
        )

    def _assert_route(self, correct_route, route):
        self.assertEqual(
            correct_route, self.acl_api_client._build_route(route)
        )


class Request(object):
    def __init__(self, user):
        self.args = [user]


class DatabaseBind(object):
    def __init__(self, bind_address):
        self._bind_address = bind_address

    @property
    def bind_address(self):
        return self._bind_address


class CredentialFake():

    def __init__(self, environment):
        self.environment = environment

    def get_parameters_by_group(self, group):
        return {}


def get_credentials_fake(environment):
    return CredentialFake(environment)
