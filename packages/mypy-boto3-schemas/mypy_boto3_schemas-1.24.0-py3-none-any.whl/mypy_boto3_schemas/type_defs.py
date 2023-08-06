"""
Type annotations for schemas service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_schemas/type_defs/)

Usage::

    ```python
    from mypy_boto3_schemas.type_defs import CreateDiscovererRequestRequestTypeDef

    data: CreateDiscovererRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from botocore.response import StreamingBody

from .literals import CodeGenerationStatusType, DiscovererStateType, TypeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CreateDiscovererRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateRegistryRequestRequestTypeDef",
    "CreateSchemaRequestRequestTypeDef",
    "DeleteDiscovererRequestRequestTypeDef",
    "DeleteRegistryRequestRequestTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeleteSchemaRequestRequestTypeDef",
    "DeleteSchemaVersionRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeCodeBindingRequestRequestTypeDef",
    "DescribeDiscovererRequestRequestTypeDef",
    "DescribeRegistryRequestRequestTypeDef",
    "DescribeSchemaRequestRequestTypeDef",
    "DiscovererSummaryTypeDef",
    "ExportSchemaRequestRequestTypeDef",
    "GetCodeBindingSourceRequestRequestTypeDef",
    "GetDiscoveredSchemaRequestRequestTypeDef",
    "GetResourcePolicyRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListDiscoverersRequestRequestTypeDef",
    "ListRegistriesRequestRequestTypeDef",
    "RegistrySummaryTypeDef",
    "ListSchemaVersionsRequestRequestTypeDef",
    "SchemaVersionSummaryTypeDef",
    "ListSchemasRequestRequestTypeDef",
    "SchemaSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PutCodeBindingRequestRequestTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "SearchSchemaVersionSummaryTypeDef",
    "SearchSchemasRequestRequestTypeDef",
    "StartDiscovererRequestRequestTypeDef",
    "StopDiscovererRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDiscovererRequestRequestTypeDef",
    "UpdateRegistryRequestRequestTypeDef",
    "UpdateSchemaRequestRequestTypeDef",
    "CreateDiscovererResponseTypeDef",
    "CreateRegistryResponseTypeDef",
    "CreateSchemaResponseTypeDef",
    "DescribeCodeBindingResponseTypeDef",
    "DescribeDiscovererResponseTypeDef",
    "DescribeRegistryResponseTypeDef",
    "DescribeSchemaResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExportSchemaResponseTypeDef",
    "GetCodeBindingSourceResponseTypeDef",
    "GetDiscoveredSchemaResponseTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutCodeBindingResponseTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "StartDiscovererResponseTypeDef",
    "StopDiscovererResponseTypeDef",
    "UpdateDiscovererResponseTypeDef",
    "UpdateRegistryResponseTypeDef",
    "UpdateSchemaResponseTypeDef",
    "DescribeCodeBindingRequestCodeBindingExistsWaitTypeDef",
    "ListDiscoverersResponseTypeDef",
    "ListDiscoverersRequestListDiscoverersPaginateTypeDef",
    "ListRegistriesRequestListRegistriesPaginateTypeDef",
    "ListSchemaVersionsRequestListSchemaVersionsPaginateTypeDef",
    "ListSchemasRequestListSchemasPaginateTypeDef",
    "SearchSchemasRequestSearchSchemasPaginateTypeDef",
    "ListRegistriesResponseTypeDef",
    "ListSchemaVersionsResponseTypeDef",
    "ListSchemasResponseTypeDef",
    "SearchSchemaSummaryTypeDef",
    "SearchSchemasResponseTypeDef",
)

_RequiredCreateDiscovererRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDiscovererRequestRequestTypeDef",
    {
        "SourceArn": str,
    },
)
_OptionalCreateDiscovererRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDiscovererRequestRequestTypeDef",
    {
        "Description": str,
        "CrossAccount": bool,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateDiscovererRequestRequestTypeDef(
    _RequiredCreateDiscovererRequestRequestTypeDef, _OptionalCreateDiscovererRequestRequestTypeDef
):
    pass


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

_RequiredCreateRegistryRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRegistryRequestRequestTypeDef",
    {
        "RegistryName": str,
    },
)
_OptionalCreateRegistryRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRegistryRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateRegistryRequestRequestTypeDef(
    _RequiredCreateRegistryRequestRequestTypeDef, _OptionalCreateRegistryRequestRequestTypeDef
):
    pass


_RequiredCreateSchemaRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSchemaRequestRequestTypeDef",
    {
        "Content": str,
        "RegistryName": str,
        "SchemaName": str,
        "Type": TypeType,
    },
)
_OptionalCreateSchemaRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSchemaRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateSchemaRequestRequestTypeDef(
    _RequiredCreateSchemaRequestRequestTypeDef, _OptionalCreateSchemaRequestRequestTypeDef
):
    pass


DeleteDiscovererRequestRequestTypeDef = TypedDict(
    "DeleteDiscovererRequestRequestTypeDef",
    {
        "DiscovererId": str,
    },
)

DeleteRegistryRequestRequestTypeDef = TypedDict(
    "DeleteRegistryRequestRequestTypeDef",
    {
        "RegistryName": str,
    },
)

DeleteResourcePolicyRequestRequestTypeDef = TypedDict(
    "DeleteResourcePolicyRequestRequestTypeDef",
    {
        "RegistryName": str,
    },
    total=False,
)

DeleteSchemaRequestRequestTypeDef = TypedDict(
    "DeleteSchemaRequestRequestTypeDef",
    {
        "RegistryName": str,
        "SchemaName": str,
    },
)

DeleteSchemaVersionRequestRequestTypeDef = TypedDict(
    "DeleteSchemaVersionRequestRequestTypeDef",
    {
        "RegistryName": str,
        "SchemaName": str,
        "SchemaVersion": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

_RequiredDescribeCodeBindingRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeCodeBindingRequestRequestTypeDef",
    {
        "Language": str,
        "RegistryName": str,
        "SchemaName": str,
    },
)
_OptionalDescribeCodeBindingRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeCodeBindingRequestRequestTypeDef",
    {
        "SchemaVersion": str,
    },
    total=False,
)


class DescribeCodeBindingRequestRequestTypeDef(
    _RequiredDescribeCodeBindingRequestRequestTypeDef,
    _OptionalDescribeCodeBindingRequestRequestTypeDef,
):
    pass


DescribeDiscovererRequestRequestTypeDef = TypedDict(
    "DescribeDiscovererRequestRequestTypeDef",
    {
        "DiscovererId": str,
    },
)

DescribeRegistryRequestRequestTypeDef = TypedDict(
    "DescribeRegistryRequestRequestTypeDef",
    {
        "RegistryName": str,
    },
)

_RequiredDescribeSchemaRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeSchemaRequestRequestTypeDef",
    {
        "RegistryName": str,
        "SchemaName": str,
    },
)
_OptionalDescribeSchemaRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeSchemaRequestRequestTypeDef",
    {
        "SchemaVersion": str,
    },
    total=False,
)


class DescribeSchemaRequestRequestTypeDef(
    _RequiredDescribeSchemaRequestRequestTypeDef, _OptionalDescribeSchemaRequestRequestTypeDef
):
    pass


DiscovererSummaryTypeDef = TypedDict(
    "DiscovererSummaryTypeDef",
    {
        "DiscovererArn": str,
        "DiscovererId": str,
        "SourceArn": str,
        "State": DiscovererStateType,
        "CrossAccount": bool,
        "Tags": Dict[str, str],
    },
    total=False,
)

_RequiredExportSchemaRequestRequestTypeDef = TypedDict(
    "_RequiredExportSchemaRequestRequestTypeDef",
    {
        "RegistryName": str,
        "SchemaName": str,
        "Type": str,
    },
)
_OptionalExportSchemaRequestRequestTypeDef = TypedDict(
    "_OptionalExportSchemaRequestRequestTypeDef",
    {
        "SchemaVersion": str,
    },
    total=False,
)


class ExportSchemaRequestRequestTypeDef(
    _RequiredExportSchemaRequestRequestTypeDef, _OptionalExportSchemaRequestRequestTypeDef
):
    pass


_RequiredGetCodeBindingSourceRequestRequestTypeDef = TypedDict(
    "_RequiredGetCodeBindingSourceRequestRequestTypeDef",
    {
        "Language": str,
        "RegistryName": str,
        "SchemaName": str,
    },
)
_OptionalGetCodeBindingSourceRequestRequestTypeDef = TypedDict(
    "_OptionalGetCodeBindingSourceRequestRequestTypeDef",
    {
        "SchemaVersion": str,
    },
    total=False,
)


class GetCodeBindingSourceRequestRequestTypeDef(
    _RequiredGetCodeBindingSourceRequestRequestTypeDef,
    _OptionalGetCodeBindingSourceRequestRequestTypeDef,
):
    pass


GetDiscoveredSchemaRequestRequestTypeDef = TypedDict(
    "GetDiscoveredSchemaRequestRequestTypeDef",
    {
        "Events": Sequence[str],
        "Type": TypeType,
    },
)

GetResourcePolicyRequestRequestTypeDef = TypedDict(
    "GetResourcePolicyRequestRequestTypeDef",
    {
        "RegistryName": str,
    },
    total=False,
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

ListDiscoverersRequestRequestTypeDef = TypedDict(
    "ListDiscoverersRequestRequestTypeDef",
    {
        "DiscovererIdPrefix": str,
        "Limit": int,
        "NextToken": str,
        "SourceArnPrefix": str,
    },
    total=False,
)

ListRegistriesRequestRequestTypeDef = TypedDict(
    "ListRegistriesRequestRequestTypeDef",
    {
        "Limit": int,
        "NextToken": str,
        "RegistryNamePrefix": str,
        "Scope": str,
    },
    total=False,
)

RegistrySummaryTypeDef = TypedDict(
    "RegistrySummaryTypeDef",
    {
        "RegistryArn": str,
        "RegistryName": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

_RequiredListSchemaVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListSchemaVersionsRequestRequestTypeDef",
    {
        "RegistryName": str,
        "SchemaName": str,
    },
)
_OptionalListSchemaVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListSchemaVersionsRequestRequestTypeDef",
    {
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)


class ListSchemaVersionsRequestRequestTypeDef(
    _RequiredListSchemaVersionsRequestRequestTypeDef,
    _OptionalListSchemaVersionsRequestRequestTypeDef,
):
    pass


SchemaVersionSummaryTypeDef = TypedDict(
    "SchemaVersionSummaryTypeDef",
    {
        "SchemaArn": str,
        "SchemaName": str,
        "SchemaVersion": str,
        "Type": TypeType,
    },
    total=False,
)

_RequiredListSchemasRequestRequestTypeDef = TypedDict(
    "_RequiredListSchemasRequestRequestTypeDef",
    {
        "RegistryName": str,
    },
)
_OptionalListSchemasRequestRequestTypeDef = TypedDict(
    "_OptionalListSchemasRequestRequestTypeDef",
    {
        "Limit": int,
        "NextToken": str,
        "SchemaNamePrefix": str,
    },
    total=False,
)


class ListSchemasRequestRequestTypeDef(
    _RequiredListSchemasRequestRequestTypeDef, _OptionalListSchemasRequestRequestTypeDef
):
    pass


SchemaSummaryTypeDef = TypedDict(
    "SchemaSummaryTypeDef",
    {
        "LastModified": datetime,
        "SchemaArn": str,
        "SchemaName": str,
        "Tags": Dict[str, str],
        "VersionCount": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredPutCodeBindingRequestRequestTypeDef = TypedDict(
    "_RequiredPutCodeBindingRequestRequestTypeDef",
    {
        "Language": str,
        "RegistryName": str,
        "SchemaName": str,
    },
)
_OptionalPutCodeBindingRequestRequestTypeDef = TypedDict(
    "_OptionalPutCodeBindingRequestRequestTypeDef",
    {
        "SchemaVersion": str,
    },
    total=False,
)


class PutCodeBindingRequestRequestTypeDef(
    _RequiredPutCodeBindingRequestRequestTypeDef, _OptionalPutCodeBindingRequestRequestTypeDef
):
    pass


_RequiredPutResourcePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredPutResourcePolicyRequestRequestTypeDef",
    {
        "Policy": str,
    },
)
_OptionalPutResourcePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalPutResourcePolicyRequestRequestTypeDef",
    {
        "RegistryName": str,
        "RevisionId": str,
    },
    total=False,
)


class PutResourcePolicyRequestRequestTypeDef(
    _RequiredPutResourcePolicyRequestRequestTypeDef, _OptionalPutResourcePolicyRequestRequestTypeDef
):
    pass


SearchSchemaVersionSummaryTypeDef = TypedDict(
    "SearchSchemaVersionSummaryTypeDef",
    {
        "CreatedDate": datetime,
        "SchemaVersion": str,
        "Type": TypeType,
    },
    total=False,
)

_RequiredSearchSchemasRequestRequestTypeDef = TypedDict(
    "_RequiredSearchSchemasRequestRequestTypeDef",
    {
        "Keywords": str,
        "RegistryName": str,
    },
)
_OptionalSearchSchemasRequestRequestTypeDef = TypedDict(
    "_OptionalSearchSchemasRequestRequestTypeDef",
    {
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)


class SearchSchemasRequestRequestTypeDef(
    _RequiredSearchSchemasRequestRequestTypeDef, _OptionalSearchSchemasRequestRequestTypeDef
):
    pass


StartDiscovererRequestRequestTypeDef = TypedDict(
    "StartDiscovererRequestRequestTypeDef",
    {
        "DiscovererId": str,
    },
)

StopDiscovererRequestRequestTypeDef = TypedDict(
    "StopDiscovererRequestRequestTypeDef",
    {
        "DiscovererId": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateDiscovererRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDiscovererRequestRequestTypeDef",
    {
        "DiscovererId": str,
    },
)
_OptionalUpdateDiscovererRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDiscovererRequestRequestTypeDef",
    {
        "Description": str,
        "CrossAccount": bool,
    },
    total=False,
)


class UpdateDiscovererRequestRequestTypeDef(
    _RequiredUpdateDiscovererRequestRequestTypeDef, _OptionalUpdateDiscovererRequestRequestTypeDef
):
    pass


_RequiredUpdateRegistryRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRegistryRequestRequestTypeDef",
    {
        "RegistryName": str,
    },
)
_OptionalUpdateRegistryRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRegistryRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class UpdateRegistryRequestRequestTypeDef(
    _RequiredUpdateRegistryRequestRequestTypeDef, _OptionalUpdateRegistryRequestRequestTypeDef
):
    pass


_RequiredUpdateSchemaRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSchemaRequestRequestTypeDef",
    {
        "RegistryName": str,
        "SchemaName": str,
    },
)
_OptionalUpdateSchemaRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSchemaRequestRequestTypeDef",
    {
        "ClientTokenId": str,
        "Content": str,
        "Description": str,
        "Type": TypeType,
    },
    total=False,
)


class UpdateSchemaRequestRequestTypeDef(
    _RequiredUpdateSchemaRequestRequestTypeDef, _OptionalUpdateSchemaRequestRequestTypeDef
):
    pass


CreateDiscovererResponseTypeDef = TypedDict(
    "CreateDiscovererResponseTypeDef",
    {
        "Description": str,
        "DiscovererArn": str,
        "DiscovererId": str,
        "SourceArn": str,
        "State": DiscovererStateType,
        "CrossAccount": bool,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRegistryResponseTypeDef = TypedDict(
    "CreateRegistryResponseTypeDef",
    {
        "Description": str,
        "RegistryArn": str,
        "RegistryName": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSchemaResponseTypeDef = TypedDict(
    "CreateSchemaResponseTypeDef",
    {
        "Description": str,
        "LastModified": datetime,
        "SchemaArn": str,
        "SchemaName": str,
        "SchemaVersion": str,
        "Tags": Dict[str, str],
        "Type": str,
        "VersionCreatedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCodeBindingResponseTypeDef = TypedDict(
    "DescribeCodeBindingResponseTypeDef",
    {
        "CreationDate": datetime,
        "LastModified": datetime,
        "SchemaVersion": str,
        "Status": CodeGenerationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDiscovererResponseTypeDef = TypedDict(
    "DescribeDiscovererResponseTypeDef",
    {
        "Description": str,
        "DiscovererArn": str,
        "DiscovererId": str,
        "SourceArn": str,
        "State": DiscovererStateType,
        "CrossAccount": bool,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRegistryResponseTypeDef = TypedDict(
    "DescribeRegistryResponseTypeDef",
    {
        "Description": str,
        "RegistryArn": str,
        "RegistryName": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSchemaResponseTypeDef = TypedDict(
    "DescribeSchemaResponseTypeDef",
    {
        "Content": str,
        "Description": str,
        "LastModified": datetime,
        "SchemaArn": str,
        "SchemaName": str,
        "SchemaVersion": str,
        "Tags": Dict[str, str],
        "Type": str,
        "VersionCreatedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportSchemaResponseTypeDef = TypedDict(
    "ExportSchemaResponseTypeDef",
    {
        "Content": str,
        "SchemaArn": str,
        "SchemaName": str,
        "SchemaVersion": str,
        "Type": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCodeBindingSourceResponseTypeDef = TypedDict(
    "GetCodeBindingSourceResponseTypeDef",
    {
        "Body": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDiscoveredSchemaResponseTypeDef = TypedDict(
    "GetDiscoveredSchemaResponseTypeDef",
    {
        "Content": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResourcePolicyResponseTypeDef = TypedDict(
    "GetResourcePolicyResponseTypeDef",
    {
        "Policy": str,
        "RevisionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutCodeBindingResponseTypeDef = TypedDict(
    "PutCodeBindingResponseTypeDef",
    {
        "CreationDate": datetime,
        "LastModified": datetime,
        "SchemaVersion": str,
        "Status": CodeGenerationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutResourcePolicyResponseTypeDef = TypedDict(
    "PutResourcePolicyResponseTypeDef",
    {
        "Policy": str,
        "RevisionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDiscovererResponseTypeDef = TypedDict(
    "StartDiscovererResponseTypeDef",
    {
        "DiscovererId": str,
        "State": DiscovererStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopDiscovererResponseTypeDef = TypedDict(
    "StopDiscovererResponseTypeDef",
    {
        "DiscovererId": str,
        "State": DiscovererStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDiscovererResponseTypeDef = TypedDict(
    "UpdateDiscovererResponseTypeDef",
    {
        "Description": str,
        "DiscovererArn": str,
        "DiscovererId": str,
        "SourceArn": str,
        "State": DiscovererStateType,
        "CrossAccount": bool,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRegistryResponseTypeDef = TypedDict(
    "UpdateRegistryResponseTypeDef",
    {
        "Description": str,
        "RegistryArn": str,
        "RegistryName": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSchemaResponseTypeDef = TypedDict(
    "UpdateSchemaResponseTypeDef",
    {
        "Description": str,
        "LastModified": datetime,
        "SchemaArn": str,
        "SchemaName": str,
        "SchemaVersion": str,
        "Tags": Dict[str, str],
        "Type": str,
        "VersionCreatedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDescribeCodeBindingRequestCodeBindingExistsWaitTypeDef = TypedDict(
    "_RequiredDescribeCodeBindingRequestCodeBindingExistsWaitTypeDef",
    {
        "Language": str,
        "RegistryName": str,
        "SchemaName": str,
    },
)
_OptionalDescribeCodeBindingRequestCodeBindingExistsWaitTypeDef = TypedDict(
    "_OptionalDescribeCodeBindingRequestCodeBindingExistsWaitTypeDef",
    {
        "SchemaVersion": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeCodeBindingRequestCodeBindingExistsWaitTypeDef(
    _RequiredDescribeCodeBindingRequestCodeBindingExistsWaitTypeDef,
    _OptionalDescribeCodeBindingRequestCodeBindingExistsWaitTypeDef,
):
    pass


ListDiscoverersResponseTypeDef = TypedDict(
    "ListDiscoverersResponseTypeDef",
    {
        "Discoverers": List[DiscovererSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDiscoverersRequestListDiscoverersPaginateTypeDef = TypedDict(
    "ListDiscoverersRequestListDiscoverersPaginateTypeDef",
    {
        "DiscovererIdPrefix": str,
        "SourceArnPrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListRegistriesRequestListRegistriesPaginateTypeDef = TypedDict(
    "ListRegistriesRequestListRegistriesPaginateTypeDef",
    {
        "RegistryNamePrefix": str,
        "Scope": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListSchemaVersionsRequestListSchemaVersionsPaginateTypeDef = TypedDict(
    "_RequiredListSchemaVersionsRequestListSchemaVersionsPaginateTypeDef",
    {
        "RegistryName": str,
        "SchemaName": str,
    },
)
_OptionalListSchemaVersionsRequestListSchemaVersionsPaginateTypeDef = TypedDict(
    "_OptionalListSchemaVersionsRequestListSchemaVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListSchemaVersionsRequestListSchemaVersionsPaginateTypeDef(
    _RequiredListSchemaVersionsRequestListSchemaVersionsPaginateTypeDef,
    _OptionalListSchemaVersionsRequestListSchemaVersionsPaginateTypeDef,
):
    pass


_RequiredListSchemasRequestListSchemasPaginateTypeDef = TypedDict(
    "_RequiredListSchemasRequestListSchemasPaginateTypeDef",
    {
        "RegistryName": str,
    },
)
_OptionalListSchemasRequestListSchemasPaginateTypeDef = TypedDict(
    "_OptionalListSchemasRequestListSchemasPaginateTypeDef",
    {
        "SchemaNamePrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListSchemasRequestListSchemasPaginateTypeDef(
    _RequiredListSchemasRequestListSchemasPaginateTypeDef,
    _OptionalListSchemasRequestListSchemasPaginateTypeDef,
):
    pass


_RequiredSearchSchemasRequestSearchSchemasPaginateTypeDef = TypedDict(
    "_RequiredSearchSchemasRequestSearchSchemasPaginateTypeDef",
    {
        "Keywords": str,
        "RegistryName": str,
    },
)
_OptionalSearchSchemasRequestSearchSchemasPaginateTypeDef = TypedDict(
    "_OptionalSearchSchemasRequestSearchSchemasPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class SearchSchemasRequestSearchSchemasPaginateTypeDef(
    _RequiredSearchSchemasRequestSearchSchemasPaginateTypeDef,
    _OptionalSearchSchemasRequestSearchSchemasPaginateTypeDef,
):
    pass


ListRegistriesResponseTypeDef = TypedDict(
    "ListRegistriesResponseTypeDef",
    {
        "NextToken": str,
        "Registries": List[RegistrySummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSchemaVersionsResponseTypeDef = TypedDict(
    "ListSchemaVersionsResponseTypeDef",
    {
        "NextToken": str,
        "SchemaVersions": List[SchemaVersionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSchemasResponseTypeDef = TypedDict(
    "ListSchemasResponseTypeDef",
    {
        "NextToken": str,
        "Schemas": List[SchemaSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchSchemaSummaryTypeDef = TypedDict(
    "SearchSchemaSummaryTypeDef",
    {
        "RegistryName": str,
        "SchemaArn": str,
        "SchemaName": str,
        "SchemaVersions": List[SearchSchemaVersionSummaryTypeDef],
    },
    total=False,
)

SearchSchemasResponseTypeDef = TypedDict(
    "SearchSchemasResponseTypeDef",
    {
        "NextToken": str,
        "Schemas": List[SearchSchemaSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
