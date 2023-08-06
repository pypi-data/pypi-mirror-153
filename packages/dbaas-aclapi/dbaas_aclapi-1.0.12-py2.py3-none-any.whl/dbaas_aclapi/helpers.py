# -*- coding: utf-8 -*-
import logging

logging.basicConfig()
LOG = logging.getLogger("AclHelpers")
LOG.setLevel(logging.DEBUG)


def iter_on_acl_query_results(acl_client, rule):
    query_results = acl_client.query_acls(rule)
    for environment in query_results.get('envs', []):
        for vlan in environment.get('vlans', []):
            environment_id = vlan['environment']
            vlan_id = vlan['num_vlan']
            for rule in vlan.get('rules', []):
                rule_id = rule['id']
                yield environment_id, vlan_id, rule_id


def iter_on_acl_rules(acl_client, rule):
    query_results = acl_client.query_acls(rule)

    if "items" in query_results:
        for item in query_results['items']:
            yield item
    else:
        for environment in query_results.get('envs', []):
            for vlan in environment.get('vlans', []):
                for rule in vlan.get('rules', []):
                    yield rule
