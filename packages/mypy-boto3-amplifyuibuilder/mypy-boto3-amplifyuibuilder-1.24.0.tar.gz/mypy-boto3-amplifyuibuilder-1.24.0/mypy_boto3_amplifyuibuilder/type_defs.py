"""
Type annotations for amplifyuibuilder service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/type_defs/)

Usage::

    ```python
    from mypy_boto3_amplifyuibuilder.type_defs import MutationActionSetStateParameterTypeDef

    data: MutationActionSetStateParameterTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence

from .literals import SortDirectionType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "MutationActionSetStateParameterTypeDef",
    "ComponentBindingPropertiesValuePropertiesTypeDef",
    "ComponentConditionPropertyTypeDef",
    "SortPropertyTypeDef",
    "ComponentPropertyBindingPropertiesTypeDef",
    "FormBindingElementTypeDef",
    "ComponentSummaryTypeDef",
    "ComponentVariantTypeDef",
    "ResponseMetadataTypeDef",
    "CreateThemeDataTypeDef",
    "ThemeTypeDef",
    "DeleteComponentRequestRequestTypeDef",
    "DeleteThemeRequestRequestTypeDef",
    "ExchangeCodeForTokenRequestBodyTypeDef",
    "PaginatorConfigTypeDef",
    "ExportComponentsRequestRequestTypeDef",
    "ExportThemesRequestRequestTypeDef",
    "GetComponentRequestRequestTypeDef",
    "GetThemeRequestRequestTypeDef",
    "ListComponentsRequestRequestTypeDef",
    "ListThemesRequestRequestTypeDef",
    "ThemeSummaryTypeDef",
    "PredicateTypeDef",
    "RefreshTokenRequestBodyTypeDef",
    "ThemeValueTypeDef",
    "ThemeValuesTypeDef",
    "UpdateThemeDataTypeDef",
    "ActionParametersTypeDef",
    "ComponentBindingPropertiesValueTypeDef",
    "ComponentDataConfigurationTypeDef",
    "ComponentPropertyTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExchangeCodeForTokenResponseTypeDef",
    "ListComponentsResponseTypeDef",
    "RefreshTokenResponseTypeDef",
    "CreateThemeRequestRequestTypeDef",
    "CreateThemeResponseTypeDef",
    "ExportThemesResponseTypeDef",
    "GetThemeResponseTypeDef",
    "UpdateThemeResponseTypeDef",
    "ExchangeCodeForTokenRequestRequestTypeDef",
    "ExportComponentsRequestExportComponentsPaginateTypeDef",
    "ExportThemesRequestExportThemesPaginateTypeDef",
    "ListComponentsRequestListComponentsPaginateTypeDef",
    "ListThemesRequestListThemesPaginateTypeDef",
    "ListThemesResponseTypeDef",
    "RefreshTokenRequestRequestTypeDef",
    "UpdateThemeRequestRequestTypeDef",
    "ComponentEventTypeDef",
    "ComponentChildTypeDef",
    "ComponentTypeDef",
    "CreateComponentDataTypeDef",
    "UpdateComponentDataTypeDef",
    "CreateComponentResponseTypeDef",
    "ExportComponentsResponseTypeDef",
    "GetComponentResponseTypeDef",
    "UpdateComponentResponseTypeDef",
    "CreateComponentRequestRequestTypeDef",
    "UpdateComponentRequestRequestTypeDef",
)

MutationActionSetStateParameterTypeDef = TypedDict(
    "MutationActionSetStateParameterTypeDef",
    {
        "componentName": str,
        "property": str,
        "set": "ComponentPropertyTypeDef",
    },
)

ComponentBindingPropertiesValuePropertiesTypeDef = TypedDict(
    "ComponentBindingPropertiesValuePropertiesTypeDef",
    {
        "bucket": str,
        "defaultValue": str,
        "field": str,
        "key": str,
        "model": str,
        "predicates": Sequence["PredicateTypeDef"],
        "userAttribute": str,
    },
    total=False,
)

ComponentConditionPropertyTypeDef = TypedDict(
    "ComponentConditionPropertyTypeDef",
    {
        "else": Dict[str, Any],
        "field": str,
        "operand": str,
        "operandType": str,
        "operator": str,
        "property": str,
        "then": Dict[str, Any],
    },
    total=False,
)

SortPropertyTypeDef = TypedDict(
    "SortPropertyTypeDef",
    {
        "direction": SortDirectionType,
        "field": str,
    },
)

_RequiredComponentPropertyBindingPropertiesTypeDef = TypedDict(
    "_RequiredComponentPropertyBindingPropertiesTypeDef",
    {
        "property": str,
    },
)
_OptionalComponentPropertyBindingPropertiesTypeDef = TypedDict(
    "_OptionalComponentPropertyBindingPropertiesTypeDef",
    {
        "field": str,
    },
    total=False,
)


class ComponentPropertyBindingPropertiesTypeDef(
    _RequiredComponentPropertyBindingPropertiesTypeDef,
    _OptionalComponentPropertyBindingPropertiesTypeDef,
):
    pass


FormBindingElementTypeDef = TypedDict(
    "FormBindingElementTypeDef",
    {
        "element": str,
        "property": str,
    },
)

ComponentSummaryTypeDef = TypedDict(
    "ComponentSummaryTypeDef",
    {
        "appId": str,
        "componentType": str,
        "environmentName": str,
        "id": str,
        "name": str,
    },
)

ComponentVariantTypeDef = TypedDict(
    "ComponentVariantTypeDef",
    {
        "overrides": Mapping[str, Mapping[str, str]],
        "variantValues": Mapping[str, str],
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

_RequiredCreateThemeDataTypeDef = TypedDict(
    "_RequiredCreateThemeDataTypeDef",
    {
        "name": str,
        "values": Sequence["ThemeValuesTypeDef"],
    },
)
_OptionalCreateThemeDataTypeDef = TypedDict(
    "_OptionalCreateThemeDataTypeDef",
    {
        "overrides": Sequence["ThemeValuesTypeDef"],
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateThemeDataTypeDef(_RequiredCreateThemeDataTypeDef, _OptionalCreateThemeDataTypeDef):
    pass


_RequiredThemeTypeDef = TypedDict(
    "_RequiredThemeTypeDef",
    {
        "appId": str,
        "createdAt": datetime,
        "environmentName": str,
        "id": str,
        "name": str,
        "values": List["ThemeValuesTypeDef"],
    },
)
_OptionalThemeTypeDef = TypedDict(
    "_OptionalThemeTypeDef",
    {
        "modifiedAt": datetime,
        "overrides": List["ThemeValuesTypeDef"],
        "tags": Dict[str, str],
    },
    total=False,
)


class ThemeTypeDef(_RequiredThemeTypeDef, _OptionalThemeTypeDef):
    pass


DeleteComponentRequestRequestTypeDef = TypedDict(
    "DeleteComponentRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
    },
)

DeleteThemeRequestRequestTypeDef = TypedDict(
    "DeleteThemeRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
    },
)

ExchangeCodeForTokenRequestBodyTypeDef = TypedDict(
    "ExchangeCodeForTokenRequestBodyTypeDef",
    {
        "code": str,
        "redirectUri": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredExportComponentsRequestRequestTypeDef = TypedDict(
    "_RequiredExportComponentsRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
    },
)
_OptionalExportComponentsRequestRequestTypeDef = TypedDict(
    "_OptionalExportComponentsRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ExportComponentsRequestRequestTypeDef(
    _RequiredExportComponentsRequestRequestTypeDef, _OptionalExportComponentsRequestRequestTypeDef
):
    pass


_RequiredExportThemesRequestRequestTypeDef = TypedDict(
    "_RequiredExportThemesRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
    },
)
_OptionalExportThemesRequestRequestTypeDef = TypedDict(
    "_OptionalExportThemesRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ExportThemesRequestRequestTypeDef(
    _RequiredExportThemesRequestRequestTypeDef, _OptionalExportThemesRequestRequestTypeDef
):
    pass


GetComponentRequestRequestTypeDef = TypedDict(
    "GetComponentRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
    },
)

GetThemeRequestRequestTypeDef = TypedDict(
    "GetThemeRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
    },
)

_RequiredListComponentsRequestRequestTypeDef = TypedDict(
    "_RequiredListComponentsRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
    },
)
_OptionalListComponentsRequestRequestTypeDef = TypedDict(
    "_OptionalListComponentsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListComponentsRequestRequestTypeDef(
    _RequiredListComponentsRequestRequestTypeDef, _OptionalListComponentsRequestRequestTypeDef
):
    pass


_RequiredListThemesRequestRequestTypeDef = TypedDict(
    "_RequiredListThemesRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
    },
)
_OptionalListThemesRequestRequestTypeDef = TypedDict(
    "_OptionalListThemesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListThemesRequestRequestTypeDef(
    _RequiredListThemesRequestRequestTypeDef, _OptionalListThemesRequestRequestTypeDef
):
    pass


ThemeSummaryTypeDef = TypedDict(
    "ThemeSummaryTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
        "name": str,
    },
)

PredicateTypeDef = TypedDict(
    "PredicateTypeDef",
    {
        "and": Sequence[Dict[str, Any]],
        "field": str,
        "operand": str,
        "operator": str,
        "or": Sequence[Dict[str, Any]],
    },
    total=False,
)

RefreshTokenRequestBodyTypeDef = TypedDict(
    "RefreshTokenRequestBodyTypeDef",
    {
        "token": str,
    },
)

ThemeValueTypeDef = TypedDict(
    "ThemeValueTypeDef",
    {
        "children": Sequence[Dict[str, Any]],
        "value": str,
    },
    total=False,
)

ThemeValuesTypeDef = TypedDict(
    "ThemeValuesTypeDef",
    {
        "key": str,
        "value": Dict[str, Any],
    },
    total=False,
)

_RequiredUpdateThemeDataTypeDef = TypedDict(
    "_RequiredUpdateThemeDataTypeDef",
    {
        "values": Sequence["ThemeValuesTypeDef"],
    },
)
_OptionalUpdateThemeDataTypeDef = TypedDict(
    "_OptionalUpdateThemeDataTypeDef",
    {
        "id": str,
        "name": str,
        "overrides": Sequence["ThemeValuesTypeDef"],
    },
    total=False,
)


class UpdateThemeDataTypeDef(_RequiredUpdateThemeDataTypeDef, _OptionalUpdateThemeDataTypeDef):
    pass


ActionParametersTypeDef = TypedDict(
    "ActionParametersTypeDef",
    {
        "anchor": "ComponentPropertyTypeDef",
        "fields": Mapping[str, "ComponentPropertyTypeDef"],
        "global": "ComponentPropertyTypeDef",
        "id": "ComponentPropertyTypeDef",
        "model": str,
        "state": MutationActionSetStateParameterTypeDef,
        "target": "ComponentPropertyTypeDef",
        "type": "ComponentPropertyTypeDef",
        "url": "ComponentPropertyTypeDef",
    },
    total=False,
)

ComponentBindingPropertiesValueTypeDef = TypedDict(
    "ComponentBindingPropertiesValueTypeDef",
    {
        "bindingProperties": ComponentBindingPropertiesValuePropertiesTypeDef,
        "defaultValue": str,
        "type": str,
    },
    total=False,
)

_RequiredComponentDataConfigurationTypeDef = TypedDict(
    "_RequiredComponentDataConfigurationTypeDef",
    {
        "model": str,
    },
)
_OptionalComponentDataConfigurationTypeDef = TypedDict(
    "_OptionalComponentDataConfigurationTypeDef",
    {
        "identifiers": Sequence[str],
        "predicate": "PredicateTypeDef",
        "sort": Sequence[SortPropertyTypeDef],
    },
    total=False,
)


class ComponentDataConfigurationTypeDef(
    _RequiredComponentDataConfigurationTypeDef, _OptionalComponentDataConfigurationTypeDef
):
    pass


ComponentPropertyTypeDef = TypedDict(
    "ComponentPropertyTypeDef",
    {
        "bindingProperties": ComponentPropertyBindingPropertiesTypeDef,
        "bindings": Mapping[str, FormBindingElementTypeDef],
        "collectionBindingProperties": ComponentPropertyBindingPropertiesTypeDef,
        "componentName": str,
        "concat": Sequence[Dict[str, Any]],
        "condition": Dict[str, Any],
        "configured": bool,
        "defaultValue": str,
        "event": str,
        "importedValue": str,
        "model": str,
        "property": str,
        "type": str,
        "userAttribute": str,
        "value": str,
    },
    total=False,
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExchangeCodeForTokenResponseTypeDef = TypedDict(
    "ExchangeCodeForTokenResponseTypeDef",
    {
        "accessToken": str,
        "expiresIn": int,
        "refreshToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListComponentsResponseTypeDef = TypedDict(
    "ListComponentsResponseTypeDef",
    {
        "entities": List[ComponentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RefreshTokenResponseTypeDef = TypedDict(
    "RefreshTokenResponseTypeDef",
    {
        "accessToken": str,
        "expiresIn": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateThemeRequestRequestTypeDef = TypedDict(
    "_RequiredCreateThemeRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "themeToCreate": CreateThemeDataTypeDef,
    },
)
_OptionalCreateThemeRequestRequestTypeDef = TypedDict(
    "_OptionalCreateThemeRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class CreateThemeRequestRequestTypeDef(
    _RequiredCreateThemeRequestRequestTypeDef, _OptionalCreateThemeRequestRequestTypeDef
):
    pass


CreateThemeResponseTypeDef = TypedDict(
    "CreateThemeResponseTypeDef",
    {
        "entity": ThemeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportThemesResponseTypeDef = TypedDict(
    "ExportThemesResponseTypeDef",
    {
        "entities": List[ThemeTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetThemeResponseTypeDef = TypedDict(
    "GetThemeResponseTypeDef",
    {
        "theme": ThemeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateThemeResponseTypeDef = TypedDict(
    "UpdateThemeResponseTypeDef",
    {
        "entity": ThemeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExchangeCodeForTokenRequestRequestTypeDef = TypedDict(
    "ExchangeCodeForTokenRequestRequestTypeDef",
    {
        "provider": Literal["figma"],
        "request": ExchangeCodeForTokenRequestBodyTypeDef,
    },
)

_RequiredExportComponentsRequestExportComponentsPaginateTypeDef = TypedDict(
    "_RequiredExportComponentsRequestExportComponentsPaginateTypeDef",
    {
        "appId": str,
        "environmentName": str,
    },
)
_OptionalExportComponentsRequestExportComponentsPaginateTypeDef = TypedDict(
    "_OptionalExportComponentsRequestExportComponentsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ExportComponentsRequestExportComponentsPaginateTypeDef(
    _RequiredExportComponentsRequestExportComponentsPaginateTypeDef,
    _OptionalExportComponentsRequestExportComponentsPaginateTypeDef,
):
    pass


_RequiredExportThemesRequestExportThemesPaginateTypeDef = TypedDict(
    "_RequiredExportThemesRequestExportThemesPaginateTypeDef",
    {
        "appId": str,
        "environmentName": str,
    },
)
_OptionalExportThemesRequestExportThemesPaginateTypeDef = TypedDict(
    "_OptionalExportThemesRequestExportThemesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ExportThemesRequestExportThemesPaginateTypeDef(
    _RequiredExportThemesRequestExportThemesPaginateTypeDef,
    _OptionalExportThemesRequestExportThemesPaginateTypeDef,
):
    pass


_RequiredListComponentsRequestListComponentsPaginateTypeDef = TypedDict(
    "_RequiredListComponentsRequestListComponentsPaginateTypeDef",
    {
        "appId": str,
        "environmentName": str,
    },
)
_OptionalListComponentsRequestListComponentsPaginateTypeDef = TypedDict(
    "_OptionalListComponentsRequestListComponentsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListComponentsRequestListComponentsPaginateTypeDef(
    _RequiredListComponentsRequestListComponentsPaginateTypeDef,
    _OptionalListComponentsRequestListComponentsPaginateTypeDef,
):
    pass


_RequiredListThemesRequestListThemesPaginateTypeDef = TypedDict(
    "_RequiredListThemesRequestListThemesPaginateTypeDef",
    {
        "appId": str,
        "environmentName": str,
    },
)
_OptionalListThemesRequestListThemesPaginateTypeDef = TypedDict(
    "_OptionalListThemesRequestListThemesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListThemesRequestListThemesPaginateTypeDef(
    _RequiredListThemesRequestListThemesPaginateTypeDef,
    _OptionalListThemesRequestListThemesPaginateTypeDef,
):
    pass


ListThemesResponseTypeDef = TypedDict(
    "ListThemesResponseTypeDef",
    {
        "entities": List[ThemeSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RefreshTokenRequestRequestTypeDef = TypedDict(
    "RefreshTokenRequestRequestTypeDef",
    {
        "provider": Literal["figma"],
        "refreshTokenBody": RefreshTokenRequestBodyTypeDef,
    },
)

_RequiredUpdateThemeRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateThemeRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
        "updatedTheme": UpdateThemeDataTypeDef,
    },
)
_OptionalUpdateThemeRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateThemeRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class UpdateThemeRequestRequestTypeDef(
    _RequiredUpdateThemeRequestRequestTypeDef, _OptionalUpdateThemeRequestRequestTypeDef
):
    pass


ComponentEventTypeDef = TypedDict(
    "ComponentEventTypeDef",
    {
        "action": str,
        "bindingEvent": str,
        "parameters": ActionParametersTypeDef,
    },
    total=False,
)

_RequiredComponentChildTypeDef = TypedDict(
    "_RequiredComponentChildTypeDef",
    {
        "componentType": str,
        "name": str,
        "properties": Mapping[str, "ComponentPropertyTypeDef"],
    },
)
_OptionalComponentChildTypeDef = TypedDict(
    "_OptionalComponentChildTypeDef",
    {
        "children": Sequence[Dict[str, Any]],
        "events": Mapping[str, ComponentEventTypeDef],
        "sourceId": str,
    },
    total=False,
)


class ComponentChildTypeDef(_RequiredComponentChildTypeDef, _OptionalComponentChildTypeDef):
    pass


_RequiredComponentTypeDef = TypedDict(
    "_RequiredComponentTypeDef",
    {
        "appId": str,
        "bindingProperties": Dict[str, ComponentBindingPropertiesValueTypeDef],
        "componentType": str,
        "createdAt": datetime,
        "environmentName": str,
        "id": str,
        "name": str,
        "overrides": Dict[str, Dict[str, str]],
        "properties": Dict[str, "ComponentPropertyTypeDef"],
        "variants": List[ComponentVariantTypeDef],
    },
)
_OptionalComponentTypeDef = TypedDict(
    "_OptionalComponentTypeDef",
    {
        "children": List["ComponentChildTypeDef"],
        "collectionProperties": Dict[str, ComponentDataConfigurationTypeDef],
        "events": Dict[str, ComponentEventTypeDef],
        "modifiedAt": datetime,
        "schemaVersion": str,
        "sourceId": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class ComponentTypeDef(_RequiredComponentTypeDef, _OptionalComponentTypeDef):
    pass


_RequiredCreateComponentDataTypeDef = TypedDict(
    "_RequiredCreateComponentDataTypeDef",
    {
        "bindingProperties": Mapping[str, ComponentBindingPropertiesValueTypeDef],
        "componentType": str,
        "name": str,
        "overrides": Mapping[str, Mapping[str, str]],
        "properties": Mapping[str, "ComponentPropertyTypeDef"],
        "variants": Sequence[ComponentVariantTypeDef],
    },
)
_OptionalCreateComponentDataTypeDef = TypedDict(
    "_OptionalCreateComponentDataTypeDef",
    {
        "children": Sequence["ComponentChildTypeDef"],
        "collectionProperties": Mapping[str, ComponentDataConfigurationTypeDef],
        "events": Mapping[str, ComponentEventTypeDef],
        "schemaVersion": str,
        "sourceId": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateComponentDataTypeDef(
    _RequiredCreateComponentDataTypeDef, _OptionalCreateComponentDataTypeDef
):
    pass


UpdateComponentDataTypeDef = TypedDict(
    "UpdateComponentDataTypeDef",
    {
        "bindingProperties": Mapping[str, ComponentBindingPropertiesValueTypeDef],
        "children": Sequence["ComponentChildTypeDef"],
        "collectionProperties": Mapping[str, ComponentDataConfigurationTypeDef],
        "componentType": str,
        "events": Mapping[str, ComponentEventTypeDef],
        "id": str,
        "name": str,
        "overrides": Mapping[str, Mapping[str, str]],
        "properties": Mapping[str, "ComponentPropertyTypeDef"],
        "schemaVersion": str,
        "sourceId": str,
        "variants": Sequence[ComponentVariantTypeDef],
    },
    total=False,
)

CreateComponentResponseTypeDef = TypedDict(
    "CreateComponentResponseTypeDef",
    {
        "entity": ComponentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportComponentsResponseTypeDef = TypedDict(
    "ExportComponentsResponseTypeDef",
    {
        "entities": List[ComponentTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetComponentResponseTypeDef = TypedDict(
    "GetComponentResponseTypeDef",
    {
        "component": ComponentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateComponentResponseTypeDef = TypedDict(
    "UpdateComponentResponseTypeDef",
    {
        "entity": ComponentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateComponentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateComponentRequestRequestTypeDef",
    {
        "appId": str,
        "componentToCreate": CreateComponentDataTypeDef,
        "environmentName": str,
    },
)
_OptionalCreateComponentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateComponentRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class CreateComponentRequestRequestTypeDef(
    _RequiredCreateComponentRequestRequestTypeDef, _OptionalCreateComponentRequestRequestTypeDef
):
    pass


_RequiredUpdateComponentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateComponentRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
        "updatedComponent": UpdateComponentDataTypeDef,
    },
)
_OptionalUpdateComponentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateComponentRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class UpdateComponentRequestRequestTypeDef(
    _RequiredUpdateComponentRequestRequestTypeDef, _OptionalUpdateComponentRequestRequestTypeDef
):
    pass
