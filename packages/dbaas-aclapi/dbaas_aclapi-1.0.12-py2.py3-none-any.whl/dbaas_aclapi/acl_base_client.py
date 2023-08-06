# -*- coding: utf-8 -*-
import json
import urllib3
import logging
import copy
from urllib import urlencode
from dbaas_aclapi import helpers

logging.basicConfig()
LOG = logging.getLogger("AclBaseClient")
LOG.setLevel(logging.DEBUG)


GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

STATUS_APPLIED = "APPLIED"
STATUS_APPROVED = "APPROVED"
STATUS_ERROR = "ERROR"
STATUS_PENDING = "PENDING"
STATUS_PROCESSING = "PROCESSING"

VALID_STATUS = [
    STATUS_APPLIED,
    STATUS_APPROVED,
    STATUS_PENDING,
    STATUS_PROCESSING
]


class GetRuleError(Exception):
    pass


class GetAuthTokenError(Exception):
    pass


class AclApplyError(Exception):
    pass


def get_credentials(environment):
    ''' get credentials available for environment '''
    from util import get_credentials_for
    from dbaas_credentials.models import CredentialType

    credentials = []
    credential_types = (CredentialType.ACLAPI, CredentialType.LIBERA_3)

    for tp in credential_types:
        credential = get_credentials_for(environment, tp)
        if credential is not None:
            credentials.append(credential)

    return credentials


def get_acl_client(environment):
    ''' return credential objects '''
    credentials = get_credentials(environment)
    acl_clients = []


    for cred in credentials:
        acl_clients.append(
            AclClient(
                cred.endpoint, cred.user, cred.password,
                environment, ip_version=4,
                auth_url=cred.get_parameter_by_name("AUTH_URL"),
                project=cred.get_parameter_by_name("project")
            )
        )

    return acl_clients


class AclClient(object):

    def __init__(self, base_url, username, password, database_environment,
                 ip_version=4, auth_url=None, project=None):
        LOG.info("Initializing new acl base client.")
        self._pool = None
        self._token = None  
        self.kind = ""
        self.acls = []
        self.headers = {}
        self.base_url = base_url
        self.username = username
        self.password = password
        self.auth_url = auth_url
        self.project = project
        self.ip_version = ip_version
        self.database_environment = database_environment
        self._add_authentication()

    @property
    def is_libera_3(self):
        return "libera3" in self.base_url

    @property
    def _http_pool(self):
        if not self._pool:
            self._pool = urllib3.PoolManager(cert_reqs='CERT_NONE')
        return self._pool

    def _add_authentication(self):
        LOG.info("Setting up authentication.")
        if self.auth_url:
            pre_headers = urllib3.util.make_headers()
            pre_headers["Authorization"] = self._get_jwt_token()

            self.headers.update(pre_headers)
        else:
            basic_auth = '{}:{}'.format(self.username, self.password)
            self.headers.update(urllib3.util.make_headers(basic_auth=basic_auth))

    def _add_content_type_json(self):
        LOG.info("Setting up \"Content-Type\".")
        self.headers.update({'Content-Type': 'application/json'})

    def _get_jwt_token(self):
        if self._token is not None:
            return self._token

        basic_auth = '{}:{}'.format(self.username, self.password)
        headers = urllib3.util.make_headers(basic_auth=basic_auth)

        req = self._http_pool.urlopen(
            method=POST,
            url=self.auth_url,
            headers=headers,
            body="grant_type=client_credentials"
        )

        if req.status != 200:
            raise GetAuthTokenError("Error while get auth token")

        self._token = "JWT %s" % json.loads(req.data)['access_token']
        return self._token

    def _do_get(self, endpoint, timeout=None, payload=None):
        ''' Make a GET request '''
        if payload:
            endpoint = "%s?%s" % (endpoint, urlencode(payload))

        if timeout:
            return self._http_pool.request(
                method=GET, url=endpoint, headers=self.headers,
                timeout=timeout
            )
        return self._http_pool.request(
            method=GET, url=endpoint, headers=self.headers
        )

    def _encode_payload(self, payload):
        if type(payload) is not str:
            payload = json.dumps(payload)

        LOG.info("JSON PAYLOAD: {}".format(payload))
        return payload

    def _do_post(self, http_verb, endpoint, payload):
        self._add_content_type_json()
        return self._http_pool.urlopen(
            method=http_verb, body=self._encode_payload(payload),
            url=endpoint, headers=self.headers
        )

    def _build_route(self, endpoint):
        return self.base_url + endpoint

    def _make_request(self, endpoint, http_verb=GET, payload=None, timeout=None):
        endpoint = self._build_route(endpoint)
        LOG.debug("Requesting {} on {}".format(http_verb, endpoint))

        if http_verb == GET:
            response = self._do_get(endpoint, timeout, payload)
        else:
            response = self._do_post(http_verb, endpoint, payload)

        LOG.debug("Response data: {}".format(response.data))
        LOG.debug("Response headers: {}".format(response.getheaders()))
        return response

    def delete_acl(self, environment_id, vlan, acl_id):
        LOG.info("Deleting ACL.")
        response = self._make_request(
            http_verb=DELETE,
            endpoint="api/ipv{}/acl/{}/{}/{}".format(
                self.ip_version, environment_id, vlan, acl_id
            )
        )
        return json.loads(response.data)

    def grant_acl_for(self, environment, vlan, payload, new_sa=None):
        LOG.info("GRANT ACLs for {} on {}".format(vlan, environment))
        endpoint = "api/ipv{}/acl/{}".format(
                    self.ip_version,
                    "{}/{}".format(environment, vlan)
        )

        if self.is_libera_3:
            endpoint = '/api/v1/access/'

        # if we are using libera3
        # check if SA from origin and destination are
        # in the same VPC
        if (new_sa and self.is_libera_3 and self.check_sa_in_same_vpc(
                payload["access"]["source"], new_sa)):
            payload['access']['destination'] = [new_sa]

        response = self._make_request(
            http_verb=PUT if not self.is_libera_3 else POST,
            payload=payload,
            endpoint=endpoint)

        json_data = json.loads(response.data)

        LOG.debug("JSON request.DATA decoded: {}".format(json_data))

        return json_data, response.status

    def check_sa_in_same_vpc(self, origin, dest):
        endpoint = '/api/v1/vpc/search'
        sa_list = []
        vpc_to_check = ""

        for sa in [origin, dest]:
            sa_list.append(
                sa[0] if isinstance(sa, list) else sa
            )

        req = self._make_request(
            http_verb=POST,
            endpoint=endpoint,
            payload={
                "service_accounts": sa_list
            }
        )

        if req.status != 201:
            return False

        for vpc in json.loads(req.data)["items"]:
            if vpc_to_check and vpc_to_check == vpc["vpc"]:
                return True

            vpc_to_check = vpc["vpc"]

        return False

    def rules_by_network(self, network, params=None):
        url = 'api/ipv{}/acl/{}?{}'.format(
            self.ip_version,
            network,
            urlencode(params or {})
        )
        response = self._make_request(
            http_verb=GET,
            endpoint=url
        )
        json_data = json.loads(response.data)
        LOG.debug(
            "JSON request.DATA decoded for get_rules_by_network: {}".format(
                json_data
            )
        )

        if response.status != 200:
            raise GetRuleError("Cant get rule for network: {} Error: {}".format(
                network,
                response.data
            ))

        for rule in json_data['rules']:
            yield rule

    def is_rule_executed(self, rule_to_find, new_sa=None):
        if "id" in rule_to_find:
            rule_to_find.pop('id')

        ports = []
        if self.is_libera_3:
            ports = rule_to_find.get("ports", [])

            # replace destination if has new_sa
            rule_to_find = {
                'destination': new_sa or rule_to_find['destination'],
                'source': rule_to_find['source'][0],
            }

        for rule_found in helpers.iter_on_acl_rules(self, rule_to_find):
            if self.is_libera_3:
                source, destination = (rule_found['source'],
                                       rule_found['destination'])

                if isinstance(source, list):
                    source = source[0]

                if isinstance(destination, list):
                    destination = destination[0]

                if all([
                 destination == rule_to_find['destination'],
                 source == rule_to_find['source'],
                 rule_found["ports"] == ports,
                 rule_found["status"].upper() in VALID_STATUS]):
                    return True
            else:
                applied_rules = self.rules_by_network(
                    rule_found['source'],
                    params={'status': 'applied'}
                )
                for rule in applied_rules:
                    if rule['id'] == rule_found['id']:
                        return True
        return False

    def get_job(self, job_id):
        LOG.info("Retrieving job {}".format(job_id))
        response = self._make_request(
            endpoint="api/jobs/{}".format(job_id)
        )
        return json.loads(response.data)

    def run_job(self, job_id, timeout=3.0):
        if self.is_libera_3:
            return (None, None)

        LOG.info("Run job {}".format(job_id))

        run_url = self.run_job_endpoint.format(job_id)
        response = self._make_request(endpoint=run_url, timeout=timeout)

        return json.loads(response.data), response.status

    def query_acls(self, payload):
        endpoint = 'api/ipv{}/acl/search'.format(self.ip_version)
        if self.is_libera_3:
            endpoint = '/api/v1/access'

        response = self._make_request(
            http_verb=GET if self.is_libera_3 else POST,
            payload=payload,
            endpoint=endpoint
        )

        return json.loads(response.data)

    @property
    def run_job_endpoint(self):
        url = "api/jobs/{}/run"

        credential = get_credentials(self.database_environment)
        run_job_params = credential[0].get_parameters_by_group('run_params')
        if run_job_params:
            url += '?'
            url += '&'.join('{}={}'.format(key, value)
                            for key, value in run_job_params.items())

        return url

    def apply_acl(self, rule):
        if not self.is_libera_3:
            return

        rule_id = rule.get("id", None)
        if not rule_id:
            return

        endpoint = '/api/v1/access/{}/approve'.format(rule_id)
        req = self._make_request(
            http_verb=POST,
            endpoint=endpoint
        )

        if req.status != 200:
            raise AclApplyError("Error while approve ACL on libera 3")
