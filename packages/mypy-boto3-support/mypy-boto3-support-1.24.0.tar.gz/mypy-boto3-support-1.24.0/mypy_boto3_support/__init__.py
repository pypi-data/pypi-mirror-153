"""
Main interface for support service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_support import (
        Client,
        DescribeCasesPaginator,
        DescribeCommunicationsPaginator,
        SupportClient,
    )

    session = Session()
    client: SupportClient = session.client("support")

    describe_cases_paginator: DescribeCasesPaginator = client.get_paginator("describe_cases")
    describe_communications_paginator: DescribeCommunicationsPaginator = client.get_paginator("describe_communications")
    ```
"""
from .client import SupportClient
from .paginator import DescribeCasesPaginator, DescribeCommunicationsPaginator

Client = SupportClient


__all__ = ("Client", "DescribeCasesPaginator", "DescribeCommunicationsPaginator", "SupportClient")
