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

from unittest import mock

from vmware_nsxlib.tests.unit.v3.policy import test_resources
from vmware_nsxlib.v3.policy import core_defs


class TestAlbAuthTokenProvider(test_resources.NsxPolicyLibTestCase):

    def test_get_avi_lb_auth_token(self):
        avi_api = self.policy_lib.alb_token_provider
        with mock.patch.object(self.policy_lib.client, 'update') as update:
            avi_api.get_avi_lb_auth_token('avi_user')
            update.assert_called_with('infra/alb-auth-token',
                                      {'username': 'avi_user', 'hours': 1})

    def test_get_avi_endpoint_info(self):
        avi_api = self.policy_lib.alb_token_provider
        with mock.patch.object(self.policy_lib.client, 'get') as get:
            avi_api.get_avi_endpoint_info()
            get.assert_called_with(
                (core_defs.AVI_ENDPOINT_PATTERN % 'infra'))
