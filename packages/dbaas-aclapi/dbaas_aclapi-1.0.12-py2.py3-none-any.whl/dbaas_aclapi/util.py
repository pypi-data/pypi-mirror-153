import logging

logging.basicConfig()
LOG = logging.getLogger("AclBindApi")
LOG.setLevel(logging.DEBUG)


def get_credentials_for(environment, credential_type):
    ''' get credential or return None if it does not exists '''
    from dbaas_credentials.models import Credential
    credential = Credential.objects.filter(
        integration_type__type=credential_type, environments=environment
    )

    return credential[0] if credential.exists() else None


def get_description_from_tupple(status_tuple, status):
    return {_tuple[0]: _tuple[1] for _tuple in status_tuple}.get(status, None)
