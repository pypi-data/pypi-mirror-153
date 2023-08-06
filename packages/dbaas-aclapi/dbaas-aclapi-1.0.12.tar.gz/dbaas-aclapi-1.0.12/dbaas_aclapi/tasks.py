# -*- coding: utf-8 -*-
import re
import copy
import logging
from time import sleep
from notification.models import TaskHistory
from dbaas_aclapi import helpers
from dbaas_aclapi.acl_base_client import get_acl_client
from acl_base_client import STATUS_PENDING, STATUS_ERROR, STATUS_APPLIED

logging.basicConfig()
LOG = logging.getLogger("AclTask")
LOG.setLevel(logging.DEBUG)
MAX_RETRIES_CHECK_APPLY = 25
SLEEP_CHECK_APPLY = 4


class ReplicateACLError(Exception):
    pass


class ReplicateACLAllErrors(Exception):
    pass

class RunJobError(Exception):
    pass


def is_ip(check_ip):
    expression = re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    return expression.match(check_ip)


def replicate_acl_for(database, old_ip, new_ip, old_sa=None, new_sa=None):
    all_errors = []
    acl_clients = get_acl_client(database.environment)
    destinations = {
        old_ip: new_ip
    }

    if old_sa:
        destinations.update({old_sa: new_sa})

    for acl in acl_clients:
        for d in destinations:

            # old and new is the same
            if d == destinations[d]:
                continue

            search = d
            if is_ip(search):
                search = "%s/32" % search

            filter_params = {"destination": search, "status": STATUS_APPLIED} if acl.is_libera_3 \
                else {"destination": search}

            for rule in helpers.iter_on_acl_rules(acl, filter_params):
                try:
                    copy_acl_rule(rule, destinations[d], acl,
                                  database, new_sa)
                    LOG.info("Rule {} copied to {}".format(
                        rule, destinations[d]))
                except Exception as e:
                    error = "Rule {} could not be copied to {}. {}".format(
                        rule, destinations[d], e)
                    LOG.warn(error)
                    all_errors.append(error)

        # get and apply pending acls.
        if acl.is_libera_3:
            for dest in [new_ip, new_sa]:
                current_apply_try = 0
                if not dest:
                    continue

                search_destination = dest
                if is_ip(search_destination):
                    search_destination = "%s/32" % search_destination

                search_pending = {
                    "destination": search_destination,
                    "status": STATUS_PENDING
                }
                while True:
                    has_pending = False
                    to_apply = helpers.iter_on_acl_rules(
                                acl,
                                search_pending)

                    for rule in to_apply:
                        has_pending = True
                        acl.apply_acl(rule)

                    if not has_pending:
                        break

                    if current_apply_try > MAX_RETRIES_CHECK_APPLY:
                        for rule in to_apply:
                            all_errors.append(
                                "Error while apply ACLs. Rule {} are pending".format(rule)
                            )
                        break

                    current_apply_try += 1
                    sleep(SLEEP_CHECK_APPLY)

                search_errors = {
                    "destination": search_destination,
                    "status": STATUS_ERROR
                }
                has_error = helpers.iter_on_acl_rules(
                                acl,
                                search_errors)

                for rule in has_error:
                    all_errors.append(
                        "Rule {} has ERROR status.".format(rule)
                    )

        if all_errors:
            raise ReplicateACLAllErrors(
                "Some ACLs cannot be replicated.\
                 Please check error message and try again:\n%s" % '\n'.join(all_errors)
            )


def destroy_acl_for(database, ip):
    acl_client = get_acl_client(database.environment)
    for environment_id, vlan_id, rule_id in helpers.iter_on_acl_query_results(
        acl_client, {"destination": ip}
    ):
        try:
            response = acl_client.delete_acl(environment_id, vlan_id, rule_id)
        except Exception as e:
            LOG.warn("Rule could not be deleted! {}".format(e))
        else:
            if 'job' in response:
                LOG.info("Rule deleted. Job: {}".format(response['job']))


def copy_acl_rule(
     rule, new_destination, acl_client, database, new_sa=None):
    data = {"kind": "object#acl", "rules": []}
    acl_environment = None
    vlan = None

    new_rule = copy.deepcopy(rule)
    if is_ip(new_destination):
        new_rule['destination'] = '{}/32'.format(new_destination)

    # check if rule exists by IP and SA
    if any([acl_client.is_rule_executed(new_rule, new_sa=new_sa),
            acl_client.is_rule_executed(new_rule)]):
        LOG.info(
            ("ACL for rule: {} is already replicated and executed for new "
             "rule: {}".format(
                rule, new_rule
             ))
        )
        return

    if not acl_client.is_libera_3:
        data['rules'].append(new_rule)
        acl_environment, vlan = new_rule['source'].split('/')
    else:
        # overwrite data format to
        # libera3
        data = {"access": {
            "destination": [new_rule["destination"]],
            "ports": new_rule["ports"],
            "protocol": new_rule["protocol"],
            "source": new_rule["source"]
        }}
    response, status_code = acl_client.grant_acl_for(
        environment=acl_environment, vlan=vlan,
        payload=data, new_sa=new_sa
    )

    if status_code != 201:
        raise ReplicateACLError(
            "\nError on ACL Replication \nstatus: {} \nResponse: {}".format(
                status_code, response
            )
        )
    else:
        run_job_resp, run_job_status = acl_client.run_job(
            response.get("job", ""),
            timeout=30
        )


def register_task(request, user):
    LOG.info(
        "id: {} | task: {} | kwargs: {} | args: {}".format(
            request.id,
            request.task,
            request.kwargs,
            str(request.args)
        )
    )

    task_history = TaskHistory.register(
        request=request, user=user,
        worker_name=get_worker_name()
    )
    task_history.update_details(persist=True, details="Loading Process...")

    return task_history


def get_worker_name():
    from billiard import current_process
    p = current_process()
    return p.initargs[1].split('@')[1]
