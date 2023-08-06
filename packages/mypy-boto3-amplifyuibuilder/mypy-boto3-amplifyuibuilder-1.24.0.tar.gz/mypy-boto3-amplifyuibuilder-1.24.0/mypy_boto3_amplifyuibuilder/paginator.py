"""
Type annotations for amplifyuibuilder service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_amplifyuibuilder.client import AmplifyUIBuilderClient
    from mypy_boto3_amplifyuibuilder.paginator import (
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
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ExportComponentsResponseTypeDef,
    ExportThemesResponseTypeDef,
    ListComponentsResponseTypeDef,
    ListThemesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ExportComponentsPaginator",
    "ExportThemesPaginator",
    "ListComponentsPaginator",
    "ListThemesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ExportComponentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Paginator.ExportComponents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#exportcomponentspaginator)
    """

    def paginate(
        self, *, appId: str, environmentName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ExportComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Paginator.ExportComponents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#exportcomponentspaginator)
        """


class ExportThemesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Paginator.ExportThemes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#exportthemespaginator)
    """

    def paginate(
        self, *, appId: str, environmentName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ExportThemesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Paginator.ExportThemes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#exportthemespaginator)
        """


class ListComponentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Paginator.ListComponents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#listcomponentspaginator)
    """

    def paginate(
        self, *, appId: str, environmentName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Paginator.ListComponents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#listcomponentspaginator)
        """


class ListThemesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Paginator.ListThemes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#listthemespaginator)
    """

    def paginate(
        self, *, appId: str, environmentName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThemesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Paginator.ListThemes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#listthemespaginator)
        """
