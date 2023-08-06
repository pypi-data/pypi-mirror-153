# -*- coding: utf-8 -*-
ACL_API_EXCEPTION = Exception(
    'ACL API error, please check the logs!'
)

ACL_API_JOB_MISSING_EXCEPTION = Exception(
    "The AclApi is not working properly: ['job'] key is missing on response"
)

MAXIMUM_RETRIES_EXCEPTION = Exception(
    "Maximum number of retries reached!"
)
