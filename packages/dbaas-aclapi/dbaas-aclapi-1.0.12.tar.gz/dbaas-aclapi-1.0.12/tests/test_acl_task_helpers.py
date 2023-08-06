import unittest
from dbaas_aclapi import helpers
from .factory import AclApiTestCase, Request


class TaskHelpersTest(AclApiTestCase):
    def test_build_data_default_options_dict(self):
        action = 'permit'
        bind_address = '10.253.1.5'
        database_name = 'mysql_test'
        database_environment = 'dev'

        description = "{} {} access for database {} in {}".format(
            action, bind_address, database_name, database_environment)

        data = {"kind": "object#acl", "rules": []}
        default_options = {"protocol": "tcp",
                           "source": "",
                           "destination": "",
                           "description": description,
                           "action": action,
                           "l4-options": {"dest-port-start": "",
                                          "dest-port-op": "eq"}
                           }
        r_data, r_default_options = helpers.build_data_default_options_dict(
            action, bind_address, database_name, database_environment)

        self.assertEqual(data, r_data)
        self.assertEqual(default_options, r_default_options)

    def test_iter_on_acl_query_results(self):
        query_gen = helpers.iter_on_acl_query_results(
            self.acl_api_client, {"test": "test"})

        test_ran = False
        for environment_id, vlan_id, rule_id in query_gen:
            test_ran = True
            self.assertEqual(environment_id, '13912')
            self.assertEqual(vlan_id, 8)
            self.assertEqual(rule_id, '98920')

        self.assertEqual(test_ran, True)

    def test_iter_on_acl_rules(self):
        query_gen = helpers.iter_on_acl_rules(
            self.acl_api_client, {"test": "test"})

        test_ran = False
        rule = {
            "id": "98920",
            "sequence": 9,
            "action": "permit",
            "protocol": "tcp",
            "source": "10.236.250.0/24",
            "destination": "10.70.1.80/32",
            "l4-options": {
                "dest-port-op": "eq",
                "dest-port-start": "22"
            }
        }

        for acl_rule in query_gen:
            test_ran = True
            self.assertEqual(acl_rule, rule)

        self.assertEqual(test_ran, True)

    @unittest.skip("Must fix import")
    def test_get_user_from_param(self):
        user = helpers.get_user('test', 'admin', 'permit')
        self.assertEqual(user, 'admin')

    @unittest.skip("Must fix import")
    def test_get_user_from_request(self):
        request = Request('root')
        user = helpers.get_user(request, None, 'permit')
        self.assertEqual(user, 'root')

    def tearDown(self):
        pass
