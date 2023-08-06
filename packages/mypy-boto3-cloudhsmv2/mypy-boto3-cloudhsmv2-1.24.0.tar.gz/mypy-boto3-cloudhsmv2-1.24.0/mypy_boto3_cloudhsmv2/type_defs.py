"""
Type annotations for cloudhsmv2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloudhsmv2.type_defs import BackupRetentionPolicyTypeDef

    data: BackupRetentionPolicyTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import BackupStateType, ClusterStateType, HsmStateType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "BackupRetentionPolicyTypeDef",
    "TagTypeDef",
    "CertificatesTypeDef",
    "HsmTypeDef",
    "DestinationBackupTypeDef",
    "ResponseMetadataTypeDef",
    "CreateHsmRequestRequestTypeDef",
    "DeleteBackupRequestRequestTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteHsmRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeBackupsRequestRequestTypeDef",
    "DescribeClustersRequestRequestTypeDef",
    "InitializeClusterRequestRequestTypeDef",
    "ListTagsRequestRequestTypeDef",
    "ModifyBackupAttributesRequestRequestTypeDef",
    "RestoreBackupRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "ModifyClusterRequestRequestTypeDef",
    "BackupTypeDef",
    "CopyBackupToRegionRequestRequestTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ClusterTypeDef",
    "CopyBackupToRegionResponseTypeDef",
    "CreateHsmResponseTypeDef",
    "DeleteHsmResponseTypeDef",
    "InitializeClusterResponseTypeDef",
    "ListTagsResponseTypeDef",
    "DescribeBackupsRequestDescribeBackupsPaginateTypeDef",
    "DescribeClustersRequestDescribeClustersPaginateTypeDef",
    "ListTagsRequestListTagsPaginateTypeDef",
    "DeleteBackupResponseTypeDef",
    "DescribeBackupsResponseTypeDef",
    "ModifyBackupAttributesResponseTypeDef",
    "RestoreBackupResponseTypeDef",
    "CreateClusterResponseTypeDef",
    "DeleteClusterResponseTypeDef",
    "DescribeClustersResponseTypeDef",
    "ModifyClusterResponseTypeDef",
)

BackupRetentionPolicyTypeDef = TypedDict(
    "BackupRetentionPolicyTypeDef",
    {
        "Type": Literal["DAYS"],
        "Value": str,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

CertificatesTypeDef = TypedDict(
    "CertificatesTypeDef",
    {
        "ClusterCsr": str,
        "HsmCertificate": str,
        "AwsHardwareCertificate": str,
        "ManufacturerHardwareCertificate": str,
        "ClusterCertificate": str,
    },
    total=False,
)

_RequiredHsmTypeDef = TypedDict(
    "_RequiredHsmTypeDef",
    {
        "HsmId": str,
    },
)
_OptionalHsmTypeDef = TypedDict(
    "_OptionalHsmTypeDef",
    {
        "AvailabilityZone": str,
        "ClusterId": str,
        "SubnetId": str,
        "EniId": str,
        "EniIp": str,
        "State": HsmStateType,
        "StateMessage": str,
    },
    total=False,
)


class HsmTypeDef(_RequiredHsmTypeDef, _OptionalHsmTypeDef):
    pass


DestinationBackupTypeDef = TypedDict(
    "DestinationBackupTypeDef",
    {
        "CreateTimestamp": datetime,
        "SourceRegion": str,
        "SourceBackup": str,
        "SourceCluster": str,
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

_RequiredCreateHsmRequestRequestTypeDef = TypedDict(
    "_RequiredCreateHsmRequestRequestTypeDef",
    {
        "ClusterId": str,
        "AvailabilityZone": str,
    },
)
_OptionalCreateHsmRequestRequestTypeDef = TypedDict(
    "_OptionalCreateHsmRequestRequestTypeDef",
    {
        "IpAddress": str,
    },
    total=False,
)


class CreateHsmRequestRequestTypeDef(
    _RequiredCreateHsmRequestRequestTypeDef, _OptionalCreateHsmRequestRequestTypeDef
):
    pass


DeleteBackupRequestRequestTypeDef = TypedDict(
    "DeleteBackupRequestRequestTypeDef",
    {
        "BackupId": str,
    },
)

DeleteClusterRequestRequestTypeDef = TypedDict(
    "DeleteClusterRequestRequestTypeDef",
    {
        "ClusterId": str,
    },
)

_RequiredDeleteHsmRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteHsmRequestRequestTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalDeleteHsmRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteHsmRequestRequestTypeDef",
    {
        "HsmId": str,
        "EniId": str,
        "EniIp": str,
    },
    total=False,
)


class DeleteHsmRequestRequestTypeDef(
    _RequiredDeleteHsmRequestRequestTypeDef, _OptionalDeleteHsmRequestRequestTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

DescribeBackupsRequestRequestTypeDef = TypedDict(
    "DescribeBackupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Mapping[str, Sequence[str]],
        "SortAscending": bool,
    },
    total=False,
)

DescribeClustersRequestRequestTypeDef = TypedDict(
    "DescribeClustersRequestRequestTypeDef",
    {
        "Filters": Mapping[str, Sequence[str]],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

InitializeClusterRequestRequestTypeDef = TypedDict(
    "InitializeClusterRequestRequestTypeDef",
    {
        "ClusterId": str,
        "SignedCert": str,
        "TrustAnchor": str,
    },
)

_RequiredListTagsRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)
_OptionalListTagsRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListTagsRequestRequestTypeDef(
    _RequiredListTagsRequestRequestTypeDef, _OptionalListTagsRequestRequestTypeDef
):
    pass


ModifyBackupAttributesRequestRequestTypeDef = TypedDict(
    "ModifyBackupAttributesRequestRequestTypeDef",
    {
        "BackupId": str,
        "NeverExpires": bool,
    },
)

RestoreBackupRequestRequestTypeDef = TypedDict(
    "RestoreBackupRequestRequestTypeDef",
    {
        "BackupId": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceId": str,
        "TagKeyList": Sequence[str],
    },
)

ModifyClusterRequestRequestTypeDef = TypedDict(
    "ModifyClusterRequestRequestTypeDef",
    {
        "BackupRetentionPolicy": BackupRetentionPolicyTypeDef,
        "ClusterId": str,
    },
)

_RequiredBackupTypeDef = TypedDict(
    "_RequiredBackupTypeDef",
    {
        "BackupId": str,
    },
)
_OptionalBackupTypeDef = TypedDict(
    "_OptionalBackupTypeDef",
    {
        "BackupState": BackupStateType,
        "ClusterId": str,
        "CreateTimestamp": datetime,
        "CopyTimestamp": datetime,
        "NeverExpires": bool,
        "SourceRegion": str,
        "SourceBackup": str,
        "SourceCluster": str,
        "DeleteTimestamp": datetime,
        "TagList": List[TagTypeDef],
    },
    total=False,
)


class BackupTypeDef(_RequiredBackupTypeDef, _OptionalBackupTypeDef):
    pass


_RequiredCopyBackupToRegionRequestRequestTypeDef = TypedDict(
    "_RequiredCopyBackupToRegionRequestRequestTypeDef",
    {
        "DestinationRegion": str,
        "BackupId": str,
    },
)
_OptionalCopyBackupToRegionRequestRequestTypeDef = TypedDict(
    "_OptionalCopyBackupToRegionRequestRequestTypeDef",
    {
        "TagList": Sequence[TagTypeDef],
    },
    total=False,
)


class CopyBackupToRegionRequestRequestTypeDef(
    _RequiredCopyBackupToRegionRequestRequestTypeDef,
    _OptionalCopyBackupToRegionRequestRequestTypeDef,
):
    pass


_RequiredCreateClusterRequestRequestTypeDef = TypedDict(
    "_RequiredCreateClusterRequestRequestTypeDef",
    {
        "HsmType": str,
        "SubnetIds": Sequence[str],
    },
)
_OptionalCreateClusterRequestRequestTypeDef = TypedDict(
    "_OptionalCreateClusterRequestRequestTypeDef",
    {
        "BackupRetentionPolicy": BackupRetentionPolicyTypeDef,
        "SourceBackupId": str,
        "TagList": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateClusterRequestRequestTypeDef(
    _RequiredCreateClusterRequestRequestTypeDef, _OptionalCreateClusterRequestRequestTypeDef
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceId": str,
        "TagList": Sequence[TagTypeDef],
    },
)

ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "BackupPolicy": Literal["DEFAULT"],
        "BackupRetentionPolicy": BackupRetentionPolicyTypeDef,
        "ClusterId": str,
        "CreateTimestamp": datetime,
        "Hsms": List[HsmTypeDef],
        "HsmType": str,
        "PreCoPassword": str,
        "SecurityGroup": str,
        "SourceBackupId": str,
        "State": ClusterStateType,
        "StateMessage": str,
        "SubnetMapping": Dict[str, str],
        "VpcId": str,
        "Certificates": CertificatesTypeDef,
        "TagList": List[TagTypeDef],
    },
    total=False,
)

CopyBackupToRegionResponseTypeDef = TypedDict(
    "CopyBackupToRegionResponseTypeDef",
    {
        "DestinationBackup": DestinationBackupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateHsmResponseTypeDef = TypedDict(
    "CreateHsmResponseTypeDef",
    {
        "Hsm": HsmTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteHsmResponseTypeDef = TypedDict(
    "DeleteHsmResponseTypeDef",
    {
        "HsmId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InitializeClusterResponseTypeDef = TypedDict(
    "InitializeClusterResponseTypeDef",
    {
        "State": ClusterStateType,
        "StateMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsResponseTypeDef = TypedDict(
    "ListTagsResponseTypeDef",
    {
        "TagList": List[TagTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBackupsRequestDescribeBackupsPaginateTypeDef = TypedDict(
    "DescribeBackupsRequestDescribeBackupsPaginateTypeDef",
    {
        "Filters": Mapping[str, Sequence[str]],
        "SortAscending": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeClustersRequestDescribeClustersPaginateTypeDef = TypedDict(
    "DescribeClustersRequestDescribeClustersPaginateTypeDef",
    {
        "Filters": Mapping[str, Sequence[str]],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListTagsRequestListTagsPaginateTypeDef = TypedDict(
    "_RequiredListTagsRequestListTagsPaginateTypeDef",
    {
        "ResourceId": str,
    },
)
_OptionalListTagsRequestListTagsPaginateTypeDef = TypedDict(
    "_OptionalListTagsRequestListTagsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTagsRequestListTagsPaginateTypeDef(
    _RequiredListTagsRequestListTagsPaginateTypeDef, _OptionalListTagsRequestListTagsPaginateTypeDef
):
    pass


DeleteBackupResponseTypeDef = TypedDict(
    "DeleteBackupResponseTypeDef",
    {
        "Backup": BackupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBackupsResponseTypeDef = TypedDict(
    "DescribeBackupsResponseTypeDef",
    {
        "Backups": List[BackupTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyBackupAttributesResponseTypeDef = TypedDict(
    "ModifyBackupAttributesResponseTypeDef",
    {
        "Backup": BackupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreBackupResponseTypeDef = TypedDict(
    "RestoreBackupResponseTypeDef",
    {
        "Backup": BackupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateClusterResponseTypeDef = TypedDict(
    "CreateClusterResponseTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteClusterResponseTypeDef = TypedDict(
    "DeleteClusterResponseTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeClustersResponseTypeDef = TypedDict(
    "DescribeClustersResponseTypeDef",
    {
        "Clusters": List[ClusterTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyClusterResponseTypeDef = TypedDict(
    "ModifyClusterResponseTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
