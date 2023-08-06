# Copyright 2021 VMware, Inc.
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

from vmware_nsxlib.v3.policy import core_defs

AVI_AUTH_TOKEN_PATH = "infra/alb-auth-token"


class AlbAuthTokenProvider(object):

    def __init__(self, policy_api):
        self.policy_api = policy_api

    def get_avi_lb_auth_token(self, username, hours=1):
        body = {'username': username, 'hours': hours}
        return self.policy_api.update(AVI_AUTH_TOKEN_PATH, body)

    def get_avi_endpoint_info(self):
        enforcement_point_path = (core_defs.AVI_ENDPOINT_PATTERN % 'infra')
        return self.policy_api.get(enforcement_point_path)
