"""
Main interface for cloudhsmv2 service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloudhsmv2 import (
        Client,
        CloudHSMV2Client,
        DescribeBackupsPaginator,
        DescribeClustersPaginator,
        ListTagsPaginator,
    )

    session = Session()
    client: CloudHSMV2Client = session.client("cloudhsmv2")

    describe_backups_paginator: DescribeBackupsPaginator = client.get_paginator("describe_backups")
    describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
    list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    ```
"""
from .client import CloudHSMV2Client
from .paginator import DescribeBackupsPaginator, DescribeClustersPaginator, ListTagsPaginator

Client = CloudHSMV2Client


__all__ = (
    "Client",
    "CloudHSMV2Client",
    "DescribeBackupsPaginator",
    "DescribeClustersPaginator",
    "ListTagsPaginator",
)
