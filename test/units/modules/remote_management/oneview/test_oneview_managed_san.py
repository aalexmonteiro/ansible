# Copyright (c) 2016-2017 Hewlett Packard Enterprise Development LP
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import pytest

from ansible.compat.tests import mock
from oneview_module_loader import OneViewModuleBase
from ansible.modules.remote_management.oneview.oneview_managed_san import ManagedSanModule
from hpe_test_utils import OneViewBaseTest

MANAGED_SAN = dict(
    name='SAN1_0',
    uri='/rest/fc-sans/managed-sans/a374d517-0369-4c48-b34e-409213642978',
    sanPolicy=dict(zoningPolicy='SingleInitiatorAllTargets',
                   zoneNameFormat='{hostName}_{initiatorWwn}',
                   enableAliasing=True,
                   initiatorNameFormat='{hostName}_{initiatorWwn}',
                   targetNameFormat='{storageSystemName}_{targetName}',
                   targetGroupNameFormat='{storageSystemName}_{targetGroupName}'))

PARAMS_FOR_PRESENT_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name='SAN1_0',
              sanPolicy=dict(zoningPolicy='SingleInitiatorSingleTarget'))
)

PARAMS_FOR_REFRESH = dict(config='config.json',
    state='refresh_state_set',
    data=dict(name='SAN1_0',
              refreshStateData=dict(refreshState='RefreshPending'))
)

PARAMS_TO_CREATE_ENDPOINTS_CSV_FILE = dict(
    config='config.json',
    state='endpoints_csv_file_created',
    data=dict(name='SAN1_0')
)

PARAMS_TO_CREATE_ISSUES_REPORT = dict(
    config='config.json',
    state='issues_report_created',
    data=dict(name='SAN1_0')
)


@pytest.mark.resource(name='managed_sans')
class TestManagedSanModule(OneViewBaseTest):
    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by_name.return_value = MANAGED_SAN
        self.mock_ansible_module.params =  dict(config='config.json', state='present', data=dict(name='SAN1_0', sanPolicy=dict(MANAGED_SAN['sanPolicy'])))

        ManagedSanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ManagedSanModule.MSG_NO_CHANGES_PROVIDED,
            ansible_facts=dict(managed_san=MANAGED_SAN)
        )

    def test_update_when_data_has_modified_attributes(self):
        self.resource.get_by_name.return_value = MANAGED_SAN
        self.resource.update.return_value = MANAGED_SAN
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT_WITH_CHANGES

        ManagedSanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ManagedSanModule.MSG_UPDATED,
            ansible_facts=dict(managed_san=MANAGED_SAN)
        )

    def test_should_fail_when_managed_san_not_found_on_present_state(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT_WITH_CHANGES

        ManagedSanModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=ManagedSanModule.MSG_NOT_FOUND)

    def test_update_refresh_state(self):
        self.resource.get_by_name.return_value = MANAGED_SAN
        self.resource.update.return_value = MANAGED_SAN
        self.mock_ansible_module.params = PARAMS_FOR_REFRESH

        ManagedSanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ManagedSanModule.MSG_REFRESH_STATE_UPDATED,
            ansible_facts=dict(managed_san=MANAGED_SAN)
        )

    def test_should_fail_when_managed_san_not_found_to_refresh(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_FOR_REFRESH

        ManagedSanModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=ManagedSanModule.MSG_NOT_FOUND)

    def test_create_endpoints_csv_file(self):
        endpoints_csv_file = {"csvFileName": "ci-005056a65f14-172.18.15.1-SAN1_0-endpoints-2016_09_21_05_55_24.csv.gz"}
        self.resource.get_by_name.return_value = MANAGED_SAN
        self.resource.create_endpoints_csv_file.return_value = endpoints_csv_file
        self.mock_ansible_module.params = PARAMS_TO_CREATE_ENDPOINTS_CSV_FILE

        ManagedSanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ManagedSanModule.MSG_ENDPOINTS_CSV_FILE_CREATED,
            ansible_facts=dict(managed_san_endpoints=endpoints_csv_file)
        )

    def test_should_fail_when_managed_san_not_found_to_create_csv_file(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_TO_CREATE_ENDPOINTS_CSV_FILE

        ManagedSanModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=ManagedSanModule.MSG_NOT_FOUND)

    def test_create_issues_report(self):
        issues_report = {"status": "report status"}
        self.resource.get_by_name.return_value = MANAGED_SAN
        self.resource.create_issues_report.return_value = issues_report
        self.mock_ansible_module.params = PARAMS_TO_CREATE_ISSUES_REPORT

        ManagedSanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ManagedSanModule.MSG_ISSUES_REPORT_CREATED,
            ansible_facts=dict(managed_san_issues=issues_report)
        )

    def test_should_fail_when_managed_san_not_found_to_create_issues_report(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_TO_CREATE_ISSUES_REPORT

        ManagedSanModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=ManagedSanModule.MSG_NOT_FOUND)


if __name__ == '__main__':
    pytest.main([__file__])
