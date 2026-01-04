"""
Create Azure storage account and blob container

Returns sas url to upload data

https://learn.microsoft.com/en-us/azure/developer/python/sdk/examples/azure-sdk-example-storage?tabs=cmd
https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli
https://learn.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob?view=azure-python#azure-storage-blob-generate-blob-sas
https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/storage/azure-storage-blob/samples/blob_samples_authentication.py#L110
"""
import os
import random
import sys
from datetime import datetime, timedelta

# Import the needed management objects from the libraries. The azure.common library
# is installed automatically with the other libraries.
from azure.identity import (
    AzureCliCredential,
    DefaultAzureCredential,
    EnvironmentCredential,
)
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from azure.mgmt.storage.models import IPRule

# Acquire a credential object using CLI-based authentication.
# credential = AzureCliCredential()
# credential = DefaultAzureCredential()  # managed identity
# AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET
credential = EnvironmentCredential()

# Step 0: Settings
# Retrieve subscription ID from environment variable.
subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']

# Constants we need in multiple places: the resource group name and the region
# in which we provision resources. You can change these values however you want.
RESOURCE_GROUP_NAME = 'PythonAzureExample-Storage-rg'
LOCATION = 'eastus'
# You can replace the storage account here with any unique name. A random number is used
# by default, but note that the name changes every time you run this script.
# The name must be 3-24 lower case letters and numbers only.
STORAGE_ACCOUNT_NAME = f'pythonazurestorage{random.randint(1,100000):05}'
CONTAINER_NAME = 'blob-container-01'

# Obtain the management object for resources.
resource_client = ResourceManagementClient(credential, subscription_id)

# Step 1: Provision the resource group.

rg_result = resource_client.resource_groups.create_or_update(
    RESOURCE_GROUP_NAME, {'location': LOCATION}
)

print(f'Provisioned resource group {rg_result.name}')

# For details on the previous code, see Example: Provision a resource group
# at https://docs.microsoft.com/azure/developer/python/azure-sdk-example-resource-group

# Step 2: Provision the storage account, starting with a management object.

storage_client = StorageManagementClient(credential, subscription_id)

# This example uses the CLI profile credentials because we assume the script
# is being used to provision the resource in the same way the Azure CLI would be used.

# Check if the account name is available. Storage account names must be unique across
# Azure because they're used in URLs.
availability_result = storage_client.storage_accounts.check_name_availability(
    {'name': STORAGE_ACCOUNT_NAME}
)

if not availability_result.name_available:
    print(f'Storage name {STORAGE_ACCOUNT_NAME} is already in use. Try another name.')
    sys.exit()

# The name is available, so provision the account
# FIXME! disable public access, enforce few ip
poller = storage_client.storage_accounts.begin_create(
    RESOURCE_GROUP_NAME,
    STORAGE_ACCOUNT_NAME,
    {
        'location': LOCATION,
        'kind': 'StorageV2',
        'sku': {'name': 'Standard_LRS'},
        'tags': {'environment': 'dev', 'engcontact': 'me'},
        # https://learn.microsoft.com/en-us/python/api/azure-mgmt-storage/azure.mgmt.storage.v2020_08_01_preview.models.iprule?view=azure-python
        # https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/storage/azure-mgmt-storage/azure/mgmt/storage/v2022_09_01/models/_models_py3.py#L3130
        # TypeError: IPRule.__init__() takes 1 positional argument but 2 were given
        # https://github.com/Azure/azure-sdk-for-python/issues/27810
        # https://github.com/Azure-Samples/azure-samples-python-management/blob/main/samples/storage/manage_storage_account_public_access.py
        'networkAcls': {
                'ipRules': [
                    {
                        'ip_address_or_range': '1.1.1.1',
                        'action': 'allow'
                    }
                ],
                'virtual_network_rules': [],
                'bypass': 'AzureServices',
                'defaultAction': 'Allow',
        },
        'enable_https_traffic_only': True,
        # https://learn.microsoft.com/en-us/python/api/azure-mgmt-storage/azure.mgmt.storage.v2018_07_01.models.publicaccess?view=azure-python
        # FIXME!
        'public_access': '',
    },
)

# Long-running operations return a poller object; calling poller.result()
# waits for completion.
account_result = poller.result()
print(f'Provisioned storage account {account_result.name}')

# Step 3: Retrieve the account's primary access key and generate a connection string.
keys = storage_client.storage_accounts.list_keys(
    RESOURCE_GROUP_NAME, STORAGE_ACCOUNT_NAME
)

print(f'Primary key for storage account: {keys.keys[0].value}')

conn_string = (
    'DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;'
    f'AccountName={STORAGE_ACCOUNT_NAME};AccountKey={keys.keys[0].value}'
)

print(f'Connection string: {conn_string}')

# Step 4: Provision the blob container in the account (this call is synchronous)
container = storage_client.blob_containers.create(
    RESOURCE_GROUP_NAME, STORAGE_ACCOUNT_NAME, CONTAINER_NAME, {}
)

# The fourth argument is a required BlobContainer object, but because we don't need any
# special values there, so we just pass empty JSON.

print(f'Provisioned blob container {container.name}')

# Step 5: Generate SAS url for upload only
BLOB_NAME = 'FOLDER_NAME'


def get_blob_sas(
    account_name, account_key, container_name, blob_name, blob_permissions
):
    """
    Get a blob sas url with 1h expiry time
    """
    sas_blob = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=account_key,
        # https://learn.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.blobsaspermissions?view=azure-python
        permission=blob_permissions,
        expiry=datetime.now(datetime.UTC) + timedelta(hours=1),
    )
    return sas_blob


# upload sas url
blob = get_blob_sas(
    STORAGE_ACCOUNT_NAME,
    keys.keys[0].value,
    CONTAINER_NAME,
    BLOB_NAME,
    BlobSasPermissions(
        # for upload
        create=True,
        write=True,
        # for reading
        read=False,
        # others
        add=False,
        delete=False,
        delete_previous_version=False,
        tag=False,
    ),
)
sas_url = (
    'https://'
    + STORAGE_ACCOUNT_NAME
    + '.blob.core.windows.net/'
    + CONTAINER_NAME
    + '/'
    + BLOB_NAME
    + '?'
    + blob
)
print(f'Provisioned W sas url {sas_url}')

# read sas url
blob = get_blob_sas(
    STORAGE_ACCOUNT_NAME,
    keys.keys[0].value,
    CONTAINER_NAME,
    BLOB_NAME,
    BlobSasPermissions(
        # for upload
        create=False,
        write=False,
        # for reading
        read=True,
        # others
        add=False,
        delete=False,
        delete_previous_version=False,
        tag=False,
    ),
)
sas_url = (
    'https://'
    + STORAGE_ACCOUNT_NAME
    + '.blob.core.windows.net/'
    + CONTAINER_NAME
    + '/'
    + BLOB_NAME
    + '?'
    + blob
)
print(f'Provisioned RO sas url {sas_url}')
