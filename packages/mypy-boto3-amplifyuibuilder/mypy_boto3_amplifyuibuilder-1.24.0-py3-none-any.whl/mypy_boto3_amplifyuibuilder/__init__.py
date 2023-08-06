"""
Main interface for amplifyuibuilder service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_amplifyuibuilder import (
        AmplifyUIBuilderClient,
        Client,
        ExportComponentsPaginator,
        ExportThemesPaginator,
        ListComponentsPaginator,
        ListThemesPaginator,
    )

    session = Session()
    client: AmplifyUIBuilderClient = session.client("amplifyuibuilder")

    export_components_paginator: ExportComponentsPaginator = client.get_paginator("export_components")
    export_themes_paginator: ExportThemesPaginator = client.get_paginator("export_themes")
    list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
    list_themes_paginator: ListThemesPaginator = client.get_paginator("list_themes")
    ```
"""
from .client import AmplifyUIBuilderClient
from .paginator import (
    ExportComponentsPaginator,
    ExportThemesPaginator,
    ListComponentsPaginator,
    ListThemesPaginator,
)

Client = AmplifyUIBuilderClient


__all__ = (
    "AmplifyUIBuilderClient",
    "Client",
    "ExportComponentsPaginator",
    "ExportThemesPaginator",
    "ListComponentsPaginator",
    "ListThemesPaginator",
)
