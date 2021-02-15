# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.service_client import SDKClient
from msrest import Serializer, Deserializer

from ._configuration import AzureNetAppFilesManagementClientConfiguration
from .operations import Operations
from .operations import NetAppResourceOperations
from .operations import AccountsOperations
from .operations import PoolsOperations
from .operations import VolumesOperations
from .operations import SnapshotsOperations
from .operations import SnapshotPoliciesOperations
from .operations import AccountBackupsOperations
from .operations import BackupsOperations
from .operations import BackupPoliciesOperations
from .operations import VaultsOperations
from . import models


class AzureNetAppFilesManagementClient(SDKClient):
    """Microsoft NetApp Azure Resource Provider specification

    :ivar config: Configuration for client.
    :vartype config: AzureNetAppFilesManagementClientConfiguration

    :ivar operations: Operations operations
    :vartype operations: azure.mgmt.netapp.operations.Operations
    :ivar net_app_resource: NetAppResource operations
    :vartype net_app_resource: azure.mgmt.netapp.operations.NetAppResourceOperations
    :ivar accounts: Accounts operations
    :vartype accounts: azure.mgmt.netapp.operations.AccountsOperations
    :ivar pools: Pools operations
    :vartype pools: azure.mgmt.netapp.operations.PoolsOperations
    :ivar volumes: Volumes operations
    :vartype volumes: azure.mgmt.netapp.operations.VolumesOperations
    :ivar snapshots: Snapshots operations
    :vartype snapshots: azure.mgmt.netapp.operations.SnapshotsOperations
    :ivar snapshot_policies: SnapshotPolicies operations
    :vartype snapshot_policies: azure.mgmt.netapp.operations.SnapshotPoliciesOperations
    :ivar account_backups: AccountBackups operations
    :vartype account_backups: azure.mgmt.netapp.operations.AccountBackupsOperations
    :ivar backups: Backups operations
    :vartype backups: azure.mgmt.netapp.operations.BackupsOperations
    :ivar backup_policies: BackupPolicies operations
    :vartype backup_policies: azure.mgmt.netapp.operations.BackupPoliciesOperations
    :ivar vaults: Vaults operations
    :vartype vaults: azure.mgmt.netapp.operations.VaultsOperations

    :param credentials: Credentials needed for the client to connect to Azure.
    :type credentials: :mod:`A msrestazure Credentials
     object<msrestazure.azure_active_directory>`
    :param subscription_id: Subscription credentials which uniquely identify
     Microsoft Azure subscription. The subscription ID forms part of the URI
     for every service call.
    :type subscription_id: str
    :param str base_url: Service URL
    """

    def __init__(
            self, credentials, subscription_id, base_url=None):

        self.config = AzureNetAppFilesManagementClientConfiguration(credentials, subscription_id, base_url)
        super(AzureNetAppFilesManagementClient, self).__init__(self.config.credentials, self.config)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self.api_version = '2020-11-01'
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        self.operations = Operations(
            self._client, self.config, self._serialize, self._deserialize)
        self.net_app_resource = NetAppResourceOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.accounts = AccountsOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.pools = PoolsOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.volumes = VolumesOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.snapshots = SnapshotsOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.snapshot_policies = SnapshotPoliciesOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.account_backups = AccountBackupsOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.backups = BackupsOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.backup_policies = BackupPoliciesOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.vaults = VaultsOperations(
            self._client, self.config, self._serialize, self._deserialize)
