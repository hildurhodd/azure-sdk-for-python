import time
from azure.mgmt.resource import ResourceManagementClient
from devtools_testutils import AzureMgmtTestCase
from azure.mgmt.netapp.models import Backup, BackupPatch, VolumePatch
from test_account import delete_account
from test_volume import create_volume, wait_for_volume, delete_volume, delete_pool
from setup import *
import azure.mgmt.netapp.models
import unittest

backups = [TEST_BACKUP_1, TEST_BACKUP_2]


def create_backup(client, backup_name=TEST_BACKUP_1, rg=BACKUP_RG, account_name=TEST_ACC_1, pool_name=TEST_POOL_1,
                  volume_name=TEST_VOL_1, location=BACKUP_LOCATION, backup_only=False, live=False):
    if not backup_only:
        create_volume(client, rg, account_name, pool_name, volume_name, location, vnet=BACKUP_VNET, live=live)
        wait_for_volume(client, rg, account_name, pool_name, volume_name, live)

    vaults = client.vaults.list(rg, account_name)
    volume_patch = VolumePatch(data_protection={
        "backup": {
            "vaultId": vaults.next().id,
            "backupEnabled": True
        }
    })
    client.volumes.begin_update(BACKUP_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, volume_patch).result()
    backup_body = Backup(location=location)
    backup = client.backups.begin_create(rg, account_name, pool_name, volume_name, backup_name, backup_body).result()
    wait_for_backup_created(client, rg, account_name, pool_name, volume_name, backup_name, live)
    return backup


def disable_backup(client, backup_name=TEST_BACKUP_1, rg=BACKUP_RG, account_name=TEST_ACC_1, pool_name=TEST_POOL_1,
                   volume_name=TEST_VOL_1, live=False):
    vaults = client.vaults.list(rg, account_name)
    volume_patch = VolumePatch(data_protection={
        "backup": {
            "vaultId": vaults.next().id,
            "backupEnabled": False
        }
    })
    client.volumes.begin_update(BACKUP_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, volume_patch).wait()
    wait_for_no_backup(client, rg, account_name, pool_name, volume_name, backup_name, live)


def delete_backup(client, backup_name=TEST_BACKUP_1, rg=BACKUP_RG, account_name=TEST_ACC_1, pool_name=TEST_POOL_1,
                  volume_name=TEST_VOL_1, live=False):
    client.backups.begin_delete(rg, account_name, pool_name, volume_name, backup_name).wait()
    wait_for_no_backup(client, rg, account_name, pool_name, volume_name, backup_name, live)


def get_backup(client, backup_name=TEST_BACKUP_1, rg=BACKUP_RG, account_name=TEST_ACC_1, pool_name=TEST_POOL_1, volume_name=TEST_VOL_1):
    return client.backups.get(rg, account_name, pool_name, volume_name, backup_name)


def get_backup_list(client, rg=BACKUP_RG, account_name=TEST_ACC_1, pool_name=TEST_POOL_1, volume_name=TEST_VOL_1):
    return client.backups.list(rg, account_name, pool_name, volume_name)


def wait_for_no_backup(client, rg, account_name, pool_name, volume_name, backup_name, live=False):
    # a workaround for the async nature of certain ARM processes
    co = 0
    while co < 10:
        co += 1
        if live:
            time.sleep(2)
        try:
            client.backups.get(rg, account_name, pool_name, volume_name, backup_name)
        except:
            # not found is an exception case (status code 200 expected)
            # and is actually what we are waiting for
            break

def wait_for_backup_created(client, rg, account_name, pool_name, volume_name, backup_name, live=False):
    co = 0
    while co < 40:
        co += 1
        if live:
            time.sleep(10)
        backup = client.backups.get(rg, account_name, pool_name, volume_name, backup_name)
        if backup.provisioning_state == "Succeeded":
            break


class NetAppAccountTestCase(AzureMgmtTestCase):
    def setUp(self):
        super(NetAppAccountTestCase, self).setUp()
        self.client = self.create_mgmt_client(azure.mgmt.netapp.NetAppManagementClient)

    def test_create_delete_backup(self):
        # Create 2 backups since delete backups can only be used when volume has multiple backups
        create_backup(self.client, live=self.is_live)

        create_backup(self.client, backup_name=TEST_BACKUP_2, backup_only=True, live=self.is_live)
        backup_list = get_backup_list(self.client)
        self.assertEqual(len(list(backup_list)), 2)

        # delete the older backup since we are not able to delete the newest one with delete backup service
        delete_backup(self.client, live=self.is_live)

        # check if backup was deleted
        backup_list = get_backup_list(self.client)
        self.assertEqual(len(list(backup_list)), 1)

        # automaticaly delete the second backup by disable backups on volume
        disable_backup(self.client, live=self.is_live)

        backup_list = get_backup_list(self.client)
        self.assertEqual(len(list(backup_list)), 0)

        delete_volume(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
        delete_pool(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, live=self.is_live)
        delete_account(self.client, BACKUP_RG, TEST_ACC_1, live=self.is_live)

    def test_list_backup(self):
        create_backup(self.client, live=self.is_live)
        create_backup(self.client, backup_name=TEST_BACKUP_2, backup_only=True, live=self.is_live)

        backup_list = get_backup_list(self.client)
        self.assertEqual(len(list(backup_list)), 2)
        idx = 0
        for backup in backup_list:
            self.assertEqual(backup.name, backups[idx])
            idx += 1

        disable_backup(self.client, live=self.is_live)
        disable_backup(self.client, backup_name=TEST_BACKUP_2, live=self.is_live)

        backup_list = get_backup_list(self.client)
        self.assertEqual(len(list(backup_list)), 0)

        delete_volume(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
        delete_pool(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, live=self.is_live)
        delete_account(self.client, BACKUP_RG, TEST_ACC_1, live=self.is_live)

    def test_get_backup_by_name(self):
        create_backup(self.client, live=self.is_live)

        backup = get_backup(self.client, TEST_BACKUP_1)
        self.assertEqual(backup.name, TEST_ACC_1 + "/" + TEST_POOL_1 + "/" + TEST_VOL_1 + "/" + TEST_BACKUP_1)

        disable_backup(self.client, TEST_BACKUP_1, live=self.is_live)
        delete_volume(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
        delete_pool(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, live=self.is_live)
        delete_account(self.client, BACKUP_RG, TEST_ACC_1, live=self.is_live)

    def test_update_backup(self):
        create_backup(self.client, live=self.is_live)

        backup_body = BackupPatch(location=BACKUP_LOCATION, use_existing_snapshot=True)
        self.client.backups.begin_update(BACKUP_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, TEST_BACKUP_1, backup_body).wait()

        backup = get_backup(self.client)
        self.assertTrue(backup.useExistingSnapshot)

        disable_backup(self.client, live=self.is_live)
        delete_volume(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
        delete_pool(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, live=self.is_live)
        delete_account(self.client, BACKUP_RG, TEST_ACC_1, live=self.is_live)

    def test_get_backup_status(self):
        create_backup(self.client, live=self.is_live)

        backup_status = self.client.backups.get_status(BACKUP_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, TEST_BACKUP_1)
        self.assertTrue(backup_status.healthy)
        self.assertEqual(backup_status.mirrorState, "Mirrored")

        disable_backup(self.client, live=self.is_live)
        delete_volume(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
        delete_pool(self.client, BACKUP_RG, TEST_ACC_1, TEST_POOL_1, live=self.is_live)
        delete_account(self.client, BACKUP_RG, TEST_ACC_1, live=self.is_live)
