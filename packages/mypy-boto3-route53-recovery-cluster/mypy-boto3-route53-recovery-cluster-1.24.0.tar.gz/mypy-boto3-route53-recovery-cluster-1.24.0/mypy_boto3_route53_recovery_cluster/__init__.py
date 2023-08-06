"""
Main interface for route53-recovery-cluster service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_route53_recovery_cluster import (
        Client,
        ListRoutingControlsPaginator,
        Route53RecoveryClusterClient,
    )

    session = Session()
    client: Route53RecoveryClusterClient = session.client("route53-recovery-cluster")

    list_routing_controls_paginator: ListRoutingControlsPaginator = client.get_paginator("list_routing_controls")
    ```
"""
from .client import Route53RecoveryClusterClient
from .paginator import ListRoutingControlsPaginator

Client = Route53RecoveryClusterClient


__all__ = ("Client", "ListRoutingControlsPaginator", "Route53RecoveryClusterClient")
