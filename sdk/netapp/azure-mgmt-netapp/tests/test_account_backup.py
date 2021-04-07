import time
from azure.mgmt.resource import ResourceManagementClient
from devtools_testutils import AzureMgmtTestCase
from azure.mgmt.netapp.models import Backup, VolumePatch
from test_account import delete_account
from test_volume import create_volume, wait_for_volume, delete_volume, delete_pool
from test_backup import create_backup, disable_backup
from setup import *
import azure.mgmt.netapp.models
import unittest

BACKUP_VNET = 'bprgpythonsdktestvnet464'
BACKUP_RG = 'bp_rg_python_sdk_test'
TEST_BACKUP_1 = 'sdk-py-tests-backup-1'
TEST_BACKUP_2 = 'sdk-py-tests-backup-2'
BACKUP_LOCATION = 'southcentralusstage'
backups = [TEST_BACKUP_1, TEST_BACKUP_2]

#list get delete
def test_list_account_backups(self):
    create_backup(self.client, backup_name=TEST_BACKUP_1, live=self.is_live)
    create_backup(self.client, backup_name=TEST_BACKUP_2, backup_only=True, live=self.is_live)

    account_backup_list = self.client.account_backups.list(BACKUP_RG, TEST_ACC_1)
    self.assertEqual(len(list(account_backup_list)), 2)

    idx = 0
    for backup in account_backup_list:
        self.assertEqual(backup.name, backups[idx])
        idx += 1

    disable_backup(self.client, live=self.is_live)
    disable_backup(self.client, backup_name=TEST_BACKUP_2, live=self.is_live)

    account_backup_list = self.client.account_backups.list(BACKUP_RG, TEST_ACC_1)
    self.assertEqual(len(list(account_backup_list)), 0)

    delete_volume(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
    delete_pool(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, live=self.is_live)
    delete_account(self.client, BACKUP_RG, TEST_ACC_1, live=self.is_live)


def test_get_account_backups(self):
    create_backup(self.client, backup_name=TEST_BACKUP_1, live=self.is_live)

    account_backup = self.client.account_backups.get(BACKUP_RG, TEST_ACC_1, TEST_BACKUP_1)
    self.assertEqual(account_backup.name, TEST_ACC_1 + "/" + TEST_POOL_1 + "/" + TEST_VOL_1 + "/" + TEST_BACKUP_1)

    disable_backup(self.client, TEST_BACKUP_1, live=self.is_live)
    delete_volume(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
    delete_pool(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, live=self.is_live)
    delete_account(self.client, BACKUP_RG, TEST_ACC_1, live=self.is_live)


def test_delete_account_backups(self):
    create_backup(self.client, backup_name=TEST_BACKUP_1, live=self.is_live)

    account_backup_list = self.client.account_backups.list(BACKUP_RG, TEST_ACC_1)
    self.assertEqual(len(list(account_backup_list)), 1)

    delete_volume(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
    self.client.account_backups.begin_delete(BACKUP_RG, TEST_ACC_1, TEST_BACKUP_1).wait()

    account_backup_list = self.client.account_backups.list(BACKUP_RG, TEST_ACC_1)
    self.assertEqual(len(list(account_backup_list)), 0)

    delete_pool(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, live=self.is_live)
    delete_account(self.client, BACKUP_RG, TEST_ACC_1, live=self.is_live)
