"""
Main interface for route53domains service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_route53domains import (
        Client,
        ListDomainsPaginator,
        ListOperationsPaginator,
        ListPricesPaginator,
        Route53DomainsClient,
        ViewBillingPaginator,
    )

    session = Session()
    client: Route53DomainsClient = session.client("route53domains")

    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_operations_paginator: ListOperationsPaginator = client.get_paginator("list_operations")
    list_prices_paginator: ListPricesPaginator = client.get_paginator("list_prices")
    view_billing_paginator: ViewBillingPaginator = client.get_paginator("view_billing")
    ```
"""
from .client import Route53DomainsClient
from .paginator import (
    ListDomainsPaginator,
    ListOperationsPaginator,
    ListPricesPaginator,
    ViewBillingPaginator,
)

Client = Route53DomainsClient


__all__ = (
    "Client",
    "ListDomainsPaginator",
    "ListOperationsPaginator",
    "ListPricesPaginator",
    "Route53DomainsClient",
    "ViewBillingPaginator",
)
