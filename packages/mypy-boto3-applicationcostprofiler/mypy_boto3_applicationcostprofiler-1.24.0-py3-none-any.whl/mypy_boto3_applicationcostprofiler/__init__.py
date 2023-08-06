"""
Main interface for applicationcostprofiler service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_applicationcostprofiler import (
        ApplicationCostProfilerClient,
        Client,
        ListReportDefinitionsPaginator,
    )

    session = Session()
    client: ApplicationCostProfilerClient = session.client("applicationcostprofiler")

    list_report_definitions_paginator: ListReportDefinitionsPaginator = client.get_paginator("list_report_definitions")
    ```
"""
from .client import ApplicationCostProfilerClient
from .paginator import ListReportDefinitionsPaginator

Client = ApplicationCostProfilerClient


__all__ = ("ApplicationCostProfilerClient", "Client", "ListReportDefinitionsPaginator")
