"""
Type annotations for iot1click-projects service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/type_defs/)

Usage::

    ```python
    from mypy_boto3_iot1click_projects.type_defs import AssociateDeviceWithPlacementRequestRequestTypeDef

    data: AssociateDeviceWithPlacementRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AssociateDeviceWithPlacementRequestRequestTypeDef",
    "CreatePlacementRequestRequestTypeDef",
    "DeletePlacementRequestRequestTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DescribePlacementRequestRequestTypeDef",
    "PlacementDescriptionTypeDef",
    "ResponseMetadataTypeDef",
    "DescribeProjectRequestRequestTypeDef",
    "DeviceTemplateTypeDef",
    "DisassociateDeviceFromPlacementRequestRequestTypeDef",
    "GetDevicesInPlacementRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListPlacementsRequestRequestTypeDef",
    "PlacementSummaryTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ProjectSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdatePlacementRequestRequestTypeDef",
    "DescribePlacementResponseTypeDef",
    "GetDevicesInPlacementResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PlacementTemplateTypeDef",
    "ListPlacementsRequestListPlacementsPaginateTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListPlacementsResponseTypeDef",
    "ListProjectsResponseTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "ProjectDescriptionTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "DescribeProjectResponseTypeDef",
)

AssociateDeviceWithPlacementRequestRequestTypeDef = TypedDict(
    "AssociateDeviceWithPlacementRequestRequestTypeDef",
    {
        "projectName": str,
        "placementName": str,
        "deviceId": str,
        "deviceTemplateName": str,
    },
)

_RequiredCreatePlacementRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePlacementRequestRequestTypeDef",
    {
        "placementName": str,
        "projectName": str,
    },
)
_OptionalCreatePlacementRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePlacementRequestRequestTypeDef",
    {
        "attributes": Mapping[str, str],
    },
    total=False,
)


class CreatePlacementRequestRequestTypeDef(
    _RequiredCreatePlacementRequestRequestTypeDef, _OptionalCreatePlacementRequestRequestTypeDef
):
    pass


DeletePlacementRequestRequestTypeDef = TypedDict(
    "DeletePlacementRequestRequestTypeDef",
    {
        "placementName": str,
        "projectName": str,
    },
)

DeleteProjectRequestRequestTypeDef = TypedDict(
    "DeleteProjectRequestRequestTypeDef",
    {
        "projectName": str,
    },
)

DescribePlacementRequestRequestTypeDef = TypedDict(
    "DescribePlacementRequestRequestTypeDef",
    {
        "placementName": str,
        "projectName": str,
    },
)

PlacementDescriptionTypeDef = TypedDict(
    "PlacementDescriptionTypeDef",
    {
        "projectName": str,
        "placementName": str,
        "attributes": Dict[str, str],
        "createdDate": datetime,
        "updatedDate": datetime,
    },
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

DescribeProjectRequestRequestTypeDef = TypedDict(
    "DescribeProjectRequestRequestTypeDef",
    {
        "projectName": str,
    },
)

DeviceTemplateTypeDef = TypedDict(
    "DeviceTemplateTypeDef",
    {
        "deviceType": str,
        "callbackOverrides": Mapping[str, str],
    },
    total=False,
)

DisassociateDeviceFromPlacementRequestRequestTypeDef = TypedDict(
    "DisassociateDeviceFromPlacementRequestRequestTypeDef",
    {
        "projectName": str,
        "placementName": str,
        "deviceTemplateName": str,
    },
)

GetDevicesInPlacementRequestRequestTypeDef = TypedDict(
    "GetDevicesInPlacementRequestRequestTypeDef",
    {
        "projectName": str,
        "placementName": str,
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

_RequiredListPlacementsRequestRequestTypeDef = TypedDict(
    "_RequiredListPlacementsRequestRequestTypeDef",
    {
        "projectName": str,
    },
)
_OptionalListPlacementsRequestRequestTypeDef = TypedDict(
    "_OptionalListPlacementsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListPlacementsRequestRequestTypeDef(
    _RequiredListPlacementsRequestRequestTypeDef, _OptionalListPlacementsRequestRequestTypeDef
):
    pass


PlacementSummaryTypeDef = TypedDict(
    "PlacementSummaryTypeDef",
    {
        "projectName": str,
        "placementName": str,
        "createdDate": datetime,
        "updatedDate": datetime,
    },
)

ListProjectsRequestRequestTypeDef = TypedDict(
    "ListProjectsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredProjectSummaryTypeDef = TypedDict(
    "_RequiredProjectSummaryTypeDef",
    {
        "projectName": str,
        "createdDate": datetime,
        "updatedDate": datetime,
    },
)
_OptionalProjectSummaryTypeDef = TypedDict(
    "_OptionalProjectSummaryTypeDef",
    {
        "arn": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class ProjectSummaryTypeDef(_RequiredProjectSummaryTypeDef, _OptionalProjectSummaryTypeDef):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdatePlacementRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePlacementRequestRequestTypeDef",
    {
        "placementName": str,
        "projectName": str,
    },
)
_OptionalUpdatePlacementRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePlacementRequestRequestTypeDef",
    {
        "attributes": Mapping[str, str],
    },
    total=False,
)


class UpdatePlacementRequestRequestTypeDef(
    _RequiredUpdatePlacementRequestRequestTypeDef, _OptionalUpdatePlacementRequestRequestTypeDef
):
    pass


DescribePlacementResponseTypeDef = TypedDict(
    "DescribePlacementResponseTypeDef",
    {
        "placement": PlacementDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDevicesInPlacementResponseTypeDef = TypedDict(
    "GetDevicesInPlacementResponseTypeDef",
    {
        "devices": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PlacementTemplateTypeDef = TypedDict(
    "PlacementTemplateTypeDef",
    {
        "defaultAttributes": Mapping[str, str],
        "deviceTemplates": Mapping[str, DeviceTemplateTypeDef],
    },
    total=False,
)

_RequiredListPlacementsRequestListPlacementsPaginateTypeDef = TypedDict(
    "_RequiredListPlacementsRequestListPlacementsPaginateTypeDef",
    {
        "projectName": str,
    },
)
_OptionalListPlacementsRequestListPlacementsPaginateTypeDef = TypedDict(
    "_OptionalListPlacementsRequestListPlacementsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListPlacementsRequestListPlacementsPaginateTypeDef(
    _RequiredListPlacementsRequestListPlacementsPaginateTypeDef,
    _OptionalListPlacementsRequestListPlacementsPaginateTypeDef,
):
    pass


ListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "ListProjectsRequestListProjectsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListPlacementsResponseTypeDef = TypedDict(
    "ListPlacementsResponseTypeDef",
    {
        "placements": List[PlacementSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProjectsResponseTypeDef = TypedDict(
    "ListProjectsResponseTypeDef",
    {
        "projects": List[ProjectSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProjectRequestRequestTypeDef",
    {
        "projectName": str,
    },
)
_OptionalCreateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProjectRequestRequestTypeDef",
    {
        "description": str,
        "placementTemplate": PlacementTemplateTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateProjectRequestRequestTypeDef(
    _RequiredCreateProjectRequestRequestTypeDef, _OptionalCreateProjectRequestRequestTypeDef
):
    pass


_RequiredProjectDescriptionTypeDef = TypedDict(
    "_RequiredProjectDescriptionTypeDef",
    {
        "projectName": str,
        "createdDate": datetime,
        "updatedDate": datetime,
    },
)
_OptionalProjectDescriptionTypeDef = TypedDict(
    "_OptionalProjectDescriptionTypeDef",
    {
        "arn": str,
        "description": str,
        "placementTemplate": PlacementTemplateTypeDef,
        "tags": Dict[str, str],
    },
    total=False,
)


class ProjectDescriptionTypeDef(
    _RequiredProjectDescriptionTypeDef, _OptionalProjectDescriptionTypeDef
):
    pass


_RequiredUpdateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateProjectRequestRequestTypeDef",
    {
        "projectName": str,
    },
)
_OptionalUpdateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateProjectRequestRequestTypeDef",
    {
        "description": str,
        "placementTemplate": PlacementTemplateTypeDef,
    },
    total=False,
)


class UpdateProjectRequestRequestTypeDef(
    _RequiredUpdateProjectRequestRequestTypeDef, _OptionalUpdateProjectRequestRequestTypeDef
):
    pass


DescribeProjectResponseTypeDef = TypedDict(
    "DescribeProjectResponseTypeDef",
    {
        "project": ProjectDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
