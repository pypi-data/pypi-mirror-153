# Copyright 2020 VMware, Inc.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

from collections import namedtuple
import logging
import traceback

from urllib3.util.retry import Retry

log = logging.getLogger(__name__)

RequestHistory = namedtuple(
    "RequestHistory", ["method", "url", "error", "status", "redirect_location"]
)


class RetryDebug(Retry):
    """Class that adds debugging capabilities of Retry"""
    def __init__(self, *args, **kw):
        super(RetryDebug, self).__init__(*args, **kw)

    def increment(self, method=None, url=None, response=None, error=None,
                  _pool=None, _stacktrace=None, ):
        if method == 'PUT':
            log.info("Retry Increment %s", traceback.format_stack())
            log.info("Retry url: %s, response: %s, error: %s,"
                     "_stacktrace: %s", url, response, error, _stacktrace)
        else:
            log.debug("Retry Increment %s", traceback.format_stack())
            log.debug("Retry method: %s, url: %s, response: %s, error: %s,"
                      " _stacktrace: %s", method, url, response, error,
                      _stacktrace)
        return super(RetryDebug, self).increment(method, url, response,
                                                 error, _pool, _stacktrace)
