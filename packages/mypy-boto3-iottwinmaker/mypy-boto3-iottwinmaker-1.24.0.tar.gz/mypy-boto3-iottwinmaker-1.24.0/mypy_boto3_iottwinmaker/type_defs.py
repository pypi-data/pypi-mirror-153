"""
Type annotations for iottwinmaker service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/type_defs/)

Usage::

    ```python
    from mypy_boto3_iottwinmaker.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    ComponentUpdateTypeType,
    ErrorCodeType,
    OrderByTimeType,
    ParentEntityUpdateTypeType,
    PropertyUpdateTypeType,
    ScopeType,
    StateType,
    TypeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ResponseMetadataTypeDef",
    "PropertyDefinitionRequestTypeDef",
    "CreateSceneRequestRequestTypeDef",
    "CreateWorkspaceRequestRequestTypeDef",
    "LambdaFunctionTypeDef",
    "RelationshipTypeDef",
    "RelationshipValueTypeDef",
    "DeleteComponentTypeRequestRequestTypeDef",
    "DeleteEntityRequestRequestTypeDef",
    "DeleteSceneRequestRequestTypeDef",
    "DeleteWorkspaceRequestRequestTypeDef",
    "EntityPropertyReferenceTypeDef",
    "ErrorDetailsTypeDef",
    "GetComponentTypeRequestRequestTypeDef",
    "PropertyDefinitionResponseTypeDef",
    "GetEntityRequestRequestTypeDef",
    "InterpolationParametersTypeDef",
    "PropertyFilterTypeDef",
    "GetPropertyValueRequestRequestTypeDef",
    "GetSceneRequestRequestTypeDef",
    "GetWorkspaceRequestRequestTypeDef",
    "ListComponentTypesFilterTypeDef",
    "ListEntitiesFilterTypeDef",
    "ListScenesRequestRequestTypeDef",
    "SceneSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWorkspacesRequestRequestTypeDef",
    "WorkspaceSummaryTypeDef",
    "ParentEntityUpdateRequestTypeDef",
    "PropertyValueTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateSceneRequestRequestTypeDef",
    "UpdateWorkspaceRequestRequestTypeDef",
    "CreateComponentTypeResponseTypeDef",
    "CreateEntityResponseTypeDef",
    "CreateSceneResponseTypeDef",
    "CreateWorkspaceResponseTypeDef",
    "DeleteComponentTypeResponseTypeDef",
    "DeleteEntityResponseTypeDef",
    "GetSceneResponseTypeDef",
    "GetWorkspaceResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateComponentTypeResponseTypeDef",
    "UpdateEntityResponseTypeDef",
    "UpdateSceneResponseTypeDef",
    "UpdateWorkspaceResponseTypeDef",
    "PropertyRequestTypeDef",
    "DataConnectorTypeDef",
    "DataTypeTypeDef",
    "DataValueTypeDef",
    "PropertyLatestValueTypeDef",
    "StatusTypeDef",
    "PropertyResponseTypeDef",
    "GetPropertyValueHistoryRequestRequestTypeDef",
    "ListComponentTypesRequestRequestTypeDef",
    "ListEntitiesRequestRequestTypeDef",
    "ListScenesResponseTypeDef",
    "ListWorkspacesResponseTypeDef",
    "PropertyValueEntryTypeDef",
    "PropertyValueHistoryTypeDef",
    "ComponentRequestTypeDef",
    "ComponentUpdateRequestTypeDef",
    "FunctionRequestTypeDef",
    "FunctionResponseTypeDef",
    "GetPropertyValueResponseTypeDef",
    "ComponentTypeSummaryTypeDef",
    "EntitySummaryTypeDef",
    "ComponentResponseTypeDef",
    "BatchPutPropertyErrorTypeDef",
    "BatchPutPropertyValuesRequestRequestTypeDef",
    "GetPropertyValueHistoryResponseTypeDef",
    "CreateEntityRequestRequestTypeDef",
    "UpdateEntityRequestRequestTypeDef",
    "CreateComponentTypeRequestRequestTypeDef",
    "UpdateComponentTypeRequestRequestTypeDef",
    "GetComponentTypeResponseTypeDef",
    "ListComponentTypesResponseTypeDef",
    "ListEntitiesResponseTypeDef",
    "GetEntityResponseTypeDef",
    "BatchPutPropertyErrorEntryTypeDef",
    "BatchPutPropertyValuesResponseTypeDef",
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

PropertyDefinitionRequestTypeDef = TypedDict(
    "PropertyDefinitionRequestTypeDef",
    {
        "configuration": Mapping[str, str],
        "dataType": "DataTypeTypeDef",
        "defaultValue": "DataValueTypeDef",
        "isExternalId": bool,
        "isRequiredInEntity": bool,
        "isStoredExternally": bool,
        "isTimeSeries": bool,
    },
    total=False,
)

_RequiredCreateSceneRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSceneRequestRequestTypeDef",
    {
        "contentLocation": str,
        "sceneId": str,
        "workspaceId": str,
    },
)
_OptionalCreateSceneRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSceneRequestRequestTypeDef",
    {
        "capabilities": Sequence[str],
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateSceneRequestRequestTypeDef(
    _RequiredCreateSceneRequestRequestTypeDef, _OptionalCreateSceneRequestRequestTypeDef
):
    pass


_RequiredCreateWorkspaceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWorkspaceRequestRequestTypeDef",
    {
        "role": str,
        "s3Location": str,
        "workspaceId": str,
    },
)
_OptionalCreateWorkspaceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWorkspaceRequestRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateWorkspaceRequestRequestTypeDef(
    _RequiredCreateWorkspaceRequestRequestTypeDef, _OptionalCreateWorkspaceRequestRequestTypeDef
):
    pass


LambdaFunctionTypeDef = TypedDict(
    "LambdaFunctionTypeDef",
    {
        "arn": str,
    },
)

RelationshipTypeDef = TypedDict(
    "RelationshipTypeDef",
    {
        "relationshipType": str,
        "targetComponentTypeId": str,
    },
    total=False,
)

RelationshipValueTypeDef = TypedDict(
    "RelationshipValueTypeDef",
    {
        "targetComponentName": str,
        "targetEntityId": str,
    },
    total=False,
)

DeleteComponentTypeRequestRequestTypeDef = TypedDict(
    "DeleteComponentTypeRequestRequestTypeDef",
    {
        "componentTypeId": str,
        "workspaceId": str,
    },
)

_RequiredDeleteEntityRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteEntityRequestRequestTypeDef",
    {
        "entityId": str,
        "workspaceId": str,
    },
)
_OptionalDeleteEntityRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteEntityRequestRequestTypeDef",
    {
        "isRecursive": bool,
    },
    total=False,
)


class DeleteEntityRequestRequestTypeDef(
    _RequiredDeleteEntityRequestRequestTypeDef, _OptionalDeleteEntityRequestRequestTypeDef
):
    pass


DeleteSceneRequestRequestTypeDef = TypedDict(
    "DeleteSceneRequestRequestTypeDef",
    {
        "sceneId": str,
        "workspaceId": str,
    },
)

DeleteWorkspaceRequestRequestTypeDef = TypedDict(
    "DeleteWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)

_RequiredEntityPropertyReferenceTypeDef = TypedDict(
    "_RequiredEntityPropertyReferenceTypeDef",
    {
        "propertyName": str,
    },
)
_OptionalEntityPropertyReferenceTypeDef = TypedDict(
    "_OptionalEntityPropertyReferenceTypeDef",
    {
        "componentName": str,
        "entityId": str,
        "externalIdProperty": Mapping[str, str],
    },
    total=False,
)


class EntityPropertyReferenceTypeDef(
    _RequiredEntityPropertyReferenceTypeDef, _OptionalEntityPropertyReferenceTypeDef
):
    pass


ErrorDetailsTypeDef = TypedDict(
    "ErrorDetailsTypeDef",
    {
        "code": ErrorCodeType,
        "message": str,
    },
    total=False,
)

GetComponentTypeRequestRequestTypeDef = TypedDict(
    "GetComponentTypeRequestRequestTypeDef",
    {
        "componentTypeId": str,
        "workspaceId": str,
    },
)

_RequiredPropertyDefinitionResponseTypeDef = TypedDict(
    "_RequiredPropertyDefinitionResponseTypeDef",
    {
        "dataType": "DataTypeTypeDef",
        "isExternalId": bool,
        "isFinal": bool,
        "isImported": bool,
        "isInherited": bool,
        "isRequiredInEntity": bool,
        "isStoredExternally": bool,
        "isTimeSeries": bool,
    },
)
_OptionalPropertyDefinitionResponseTypeDef = TypedDict(
    "_OptionalPropertyDefinitionResponseTypeDef",
    {
        "configuration": Dict[str, str],
        "defaultValue": "DataValueTypeDef",
    },
    total=False,
)


class PropertyDefinitionResponseTypeDef(
    _RequiredPropertyDefinitionResponseTypeDef, _OptionalPropertyDefinitionResponseTypeDef
):
    pass


GetEntityRequestRequestTypeDef = TypedDict(
    "GetEntityRequestRequestTypeDef",
    {
        "entityId": str,
        "workspaceId": str,
    },
)

InterpolationParametersTypeDef = TypedDict(
    "InterpolationParametersTypeDef",
    {
        "interpolationType": Literal["LINEAR"],
        "intervalInSeconds": int,
    },
    total=False,
)

PropertyFilterTypeDef = TypedDict(
    "PropertyFilterTypeDef",
    {
        "operator": str,
        "propertyName": str,
        "value": "DataValueTypeDef",
    },
    total=False,
)

_RequiredGetPropertyValueRequestRequestTypeDef = TypedDict(
    "_RequiredGetPropertyValueRequestRequestTypeDef",
    {
        "selectedProperties": Sequence[str],
        "workspaceId": str,
    },
)
_OptionalGetPropertyValueRequestRequestTypeDef = TypedDict(
    "_OptionalGetPropertyValueRequestRequestTypeDef",
    {
        "componentName": str,
        "componentTypeId": str,
        "entityId": str,
    },
    total=False,
)


class GetPropertyValueRequestRequestTypeDef(
    _RequiredGetPropertyValueRequestRequestTypeDef, _OptionalGetPropertyValueRequestRequestTypeDef
):
    pass


GetSceneRequestRequestTypeDef = TypedDict(
    "GetSceneRequestRequestTypeDef",
    {
        "sceneId": str,
        "workspaceId": str,
    },
)

GetWorkspaceRequestRequestTypeDef = TypedDict(
    "GetWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)

ListComponentTypesFilterTypeDef = TypedDict(
    "ListComponentTypesFilterTypeDef",
    {
        "extendsFrom": str,
        "isAbstract": bool,
        "namespace": str,
    },
    total=False,
)

ListEntitiesFilterTypeDef = TypedDict(
    "ListEntitiesFilterTypeDef",
    {
        "componentTypeId": str,
        "externalId": str,
        "parentEntityId": str,
    },
    total=False,
)

_RequiredListScenesRequestRequestTypeDef = TypedDict(
    "_RequiredListScenesRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalListScenesRequestRequestTypeDef = TypedDict(
    "_OptionalListScenesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListScenesRequestRequestTypeDef(
    _RequiredListScenesRequestRequestTypeDef, _OptionalListScenesRequestRequestTypeDef
):
    pass


_RequiredSceneSummaryTypeDef = TypedDict(
    "_RequiredSceneSummaryTypeDef",
    {
        "arn": str,
        "contentLocation": str,
        "creationDateTime": datetime,
        "sceneId": str,
        "updateDateTime": datetime,
    },
)
_OptionalSceneSummaryTypeDef = TypedDict(
    "_OptionalSceneSummaryTypeDef",
    {
        "description": str,
    },
    total=False,
)


class SceneSummaryTypeDef(_RequiredSceneSummaryTypeDef, _OptionalSceneSummaryTypeDef):
    pass


_RequiredListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestRequestTypeDef",
    {
        "resourceARN": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListTagsForResourceRequestRequestTypeDef(
    _RequiredListTagsForResourceRequestRequestTypeDef,
    _OptionalListTagsForResourceRequestRequestTypeDef,
):
    pass


ListWorkspacesRequestRequestTypeDef = TypedDict(
    "ListWorkspacesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredWorkspaceSummaryTypeDef = TypedDict(
    "_RequiredWorkspaceSummaryTypeDef",
    {
        "arn": str,
        "creationDateTime": datetime,
        "updateDateTime": datetime,
        "workspaceId": str,
    },
)
_OptionalWorkspaceSummaryTypeDef = TypedDict(
    "_OptionalWorkspaceSummaryTypeDef",
    {
        "description": str,
    },
    total=False,
)


class WorkspaceSummaryTypeDef(_RequiredWorkspaceSummaryTypeDef, _OptionalWorkspaceSummaryTypeDef):
    pass


_RequiredParentEntityUpdateRequestTypeDef = TypedDict(
    "_RequiredParentEntityUpdateRequestTypeDef",
    {
        "updateType": ParentEntityUpdateTypeType,
    },
)
_OptionalParentEntityUpdateRequestTypeDef = TypedDict(
    "_OptionalParentEntityUpdateRequestTypeDef",
    {
        "parentEntityId": str,
    },
    total=False,
)


class ParentEntityUpdateRequestTypeDef(
    _RequiredParentEntityUpdateRequestTypeDef, _OptionalParentEntityUpdateRequestTypeDef
):
    pass


_RequiredPropertyValueTypeDef = TypedDict(
    "_RequiredPropertyValueTypeDef",
    {
        "value": "DataValueTypeDef",
    },
)
_OptionalPropertyValueTypeDef = TypedDict(
    "_OptionalPropertyValueTypeDef",
    {
        "time": str,
        "timestamp": Union[datetime, str],
    },
    total=False,
)


class PropertyValueTypeDef(_RequiredPropertyValueTypeDef, _OptionalPropertyValueTypeDef):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceARN": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceARN": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateSceneRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSceneRequestRequestTypeDef",
    {
        "sceneId": str,
        "workspaceId": str,
    },
)
_OptionalUpdateSceneRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSceneRequestRequestTypeDef",
    {
        "capabilities": Sequence[str],
        "contentLocation": str,
        "description": str,
    },
    total=False,
)


class UpdateSceneRequestRequestTypeDef(
    _RequiredUpdateSceneRequestRequestTypeDef, _OptionalUpdateSceneRequestRequestTypeDef
):
    pass


_RequiredUpdateWorkspaceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalUpdateWorkspaceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWorkspaceRequestRequestTypeDef",
    {
        "description": str,
        "role": str,
    },
    total=False,
)


class UpdateWorkspaceRequestRequestTypeDef(
    _RequiredUpdateWorkspaceRequestRequestTypeDef, _OptionalUpdateWorkspaceRequestRequestTypeDef
):
    pass


CreateComponentTypeResponseTypeDef = TypedDict(
    "CreateComponentTypeResponseTypeDef",
    {
        "arn": str,
        "creationDateTime": datetime,
        "state": StateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEntityResponseTypeDef = TypedDict(
    "CreateEntityResponseTypeDef",
    {
        "arn": str,
        "creationDateTime": datetime,
        "entityId": str,
        "state": StateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSceneResponseTypeDef = TypedDict(
    "CreateSceneResponseTypeDef",
    {
        "arn": str,
        "creationDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateWorkspaceResponseTypeDef = TypedDict(
    "CreateWorkspaceResponseTypeDef",
    {
        "arn": str,
        "creationDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteComponentTypeResponseTypeDef = TypedDict(
    "DeleteComponentTypeResponseTypeDef",
    {
        "state": StateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteEntityResponseTypeDef = TypedDict(
    "DeleteEntityResponseTypeDef",
    {
        "state": StateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSceneResponseTypeDef = TypedDict(
    "GetSceneResponseTypeDef",
    {
        "arn": str,
        "capabilities": List[str],
        "contentLocation": str,
        "creationDateTime": datetime,
        "description": str,
        "sceneId": str,
        "updateDateTime": datetime,
        "workspaceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetWorkspaceResponseTypeDef = TypedDict(
    "GetWorkspaceResponseTypeDef",
    {
        "arn": str,
        "creationDateTime": datetime,
        "description": str,
        "role": str,
        "s3Location": str,
        "updateDateTime": datetime,
        "workspaceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "nextToken": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateComponentTypeResponseTypeDef = TypedDict(
    "UpdateComponentTypeResponseTypeDef",
    {
        "arn": str,
        "componentTypeId": str,
        "state": StateType,
        "workspaceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEntityResponseTypeDef = TypedDict(
    "UpdateEntityResponseTypeDef",
    {
        "state": StateType,
        "updateDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSceneResponseTypeDef = TypedDict(
    "UpdateSceneResponseTypeDef",
    {
        "updateDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateWorkspaceResponseTypeDef = TypedDict(
    "UpdateWorkspaceResponseTypeDef",
    {
        "updateDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PropertyRequestTypeDef = TypedDict(
    "PropertyRequestTypeDef",
    {
        "definition": PropertyDefinitionRequestTypeDef,
        "updateType": PropertyUpdateTypeType,
        "value": "DataValueTypeDef",
    },
    total=False,
)

DataConnectorTypeDef = TypedDict(
    "DataConnectorTypeDef",
    {
        "isNative": bool,
        "lambda": LambdaFunctionTypeDef,
    },
    total=False,
)

_RequiredDataTypeTypeDef = TypedDict(
    "_RequiredDataTypeTypeDef",
    {
        "type": TypeType,
    },
)
_OptionalDataTypeTypeDef = TypedDict(
    "_OptionalDataTypeTypeDef",
    {
        "allowedValues": Sequence["DataValueTypeDef"],
        "nestedType": Dict[str, Any],
        "relationship": RelationshipTypeDef,
        "unitOfMeasure": str,
    },
    total=False,
)


class DataTypeTypeDef(_RequiredDataTypeTypeDef, _OptionalDataTypeTypeDef):
    pass


DataValueTypeDef = TypedDict(
    "DataValueTypeDef",
    {
        "booleanValue": bool,
        "doubleValue": float,
        "expression": str,
        "integerValue": int,
        "listValue": Sequence[Dict[str, Any]],
        "longValue": int,
        "mapValue": Mapping[str, Dict[str, Any]],
        "relationshipValue": RelationshipValueTypeDef,
        "stringValue": str,
    },
    total=False,
)

_RequiredPropertyLatestValueTypeDef = TypedDict(
    "_RequiredPropertyLatestValueTypeDef",
    {
        "propertyReference": EntityPropertyReferenceTypeDef,
    },
)
_OptionalPropertyLatestValueTypeDef = TypedDict(
    "_OptionalPropertyLatestValueTypeDef",
    {
        "propertyValue": "DataValueTypeDef",
    },
    total=False,
)


class PropertyLatestValueTypeDef(
    _RequiredPropertyLatestValueTypeDef, _OptionalPropertyLatestValueTypeDef
):
    pass


StatusTypeDef = TypedDict(
    "StatusTypeDef",
    {
        "error": ErrorDetailsTypeDef,
        "state": StateType,
    },
    total=False,
)

PropertyResponseTypeDef = TypedDict(
    "PropertyResponseTypeDef",
    {
        "definition": PropertyDefinitionResponseTypeDef,
        "value": "DataValueTypeDef",
    },
    total=False,
)

_RequiredGetPropertyValueHistoryRequestRequestTypeDef = TypedDict(
    "_RequiredGetPropertyValueHistoryRequestRequestTypeDef",
    {
        "selectedProperties": Sequence[str],
        "workspaceId": str,
    },
)
_OptionalGetPropertyValueHistoryRequestRequestTypeDef = TypedDict(
    "_OptionalGetPropertyValueHistoryRequestRequestTypeDef",
    {
        "componentName": str,
        "componentTypeId": str,
        "endDateTime": Union[datetime, str],
        "endTime": str,
        "entityId": str,
        "interpolation": InterpolationParametersTypeDef,
        "maxResults": int,
        "nextToken": str,
        "orderByTime": OrderByTimeType,
        "propertyFilters": Sequence[PropertyFilterTypeDef],
        "startDateTime": Union[datetime, str],
        "startTime": str,
    },
    total=False,
)


class GetPropertyValueHistoryRequestRequestTypeDef(
    _RequiredGetPropertyValueHistoryRequestRequestTypeDef,
    _OptionalGetPropertyValueHistoryRequestRequestTypeDef,
):
    pass


_RequiredListComponentTypesRequestRequestTypeDef = TypedDict(
    "_RequiredListComponentTypesRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalListComponentTypesRequestRequestTypeDef = TypedDict(
    "_OptionalListComponentTypesRequestRequestTypeDef",
    {
        "filters": Sequence[ListComponentTypesFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListComponentTypesRequestRequestTypeDef(
    _RequiredListComponentTypesRequestRequestTypeDef,
    _OptionalListComponentTypesRequestRequestTypeDef,
):
    pass


_RequiredListEntitiesRequestRequestTypeDef = TypedDict(
    "_RequiredListEntitiesRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalListEntitiesRequestRequestTypeDef = TypedDict(
    "_OptionalListEntitiesRequestRequestTypeDef",
    {
        "filters": Sequence[ListEntitiesFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListEntitiesRequestRequestTypeDef(
    _RequiredListEntitiesRequestRequestTypeDef, _OptionalListEntitiesRequestRequestTypeDef
):
    pass


ListScenesResponseTypeDef = TypedDict(
    "ListScenesResponseTypeDef",
    {
        "nextToken": str,
        "sceneSummaries": List[SceneSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWorkspacesResponseTypeDef = TypedDict(
    "ListWorkspacesResponseTypeDef",
    {
        "nextToken": str,
        "workspaceSummaries": List[WorkspaceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPropertyValueEntryTypeDef = TypedDict(
    "_RequiredPropertyValueEntryTypeDef",
    {
        "entityPropertyReference": EntityPropertyReferenceTypeDef,
    },
)
_OptionalPropertyValueEntryTypeDef = TypedDict(
    "_OptionalPropertyValueEntryTypeDef",
    {
        "propertyValues": Sequence[PropertyValueTypeDef],
    },
    total=False,
)


class PropertyValueEntryTypeDef(
    _RequiredPropertyValueEntryTypeDef, _OptionalPropertyValueEntryTypeDef
):
    pass


_RequiredPropertyValueHistoryTypeDef = TypedDict(
    "_RequiredPropertyValueHistoryTypeDef",
    {
        "entityPropertyReference": EntityPropertyReferenceTypeDef,
    },
)
_OptionalPropertyValueHistoryTypeDef = TypedDict(
    "_OptionalPropertyValueHistoryTypeDef",
    {
        "values": List[PropertyValueTypeDef],
    },
    total=False,
)


class PropertyValueHistoryTypeDef(
    _RequiredPropertyValueHistoryTypeDef, _OptionalPropertyValueHistoryTypeDef
):
    pass


ComponentRequestTypeDef = TypedDict(
    "ComponentRequestTypeDef",
    {
        "componentTypeId": str,
        "description": str,
        "properties": Mapping[str, PropertyRequestTypeDef],
    },
    total=False,
)

ComponentUpdateRequestTypeDef = TypedDict(
    "ComponentUpdateRequestTypeDef",
    {
        "componentTypeId": str,
        "description": str,
        "propertyUpdates": Mapping[str, PropertyRequestTypeDef],
        "updateType": ComponentUpdateTypeType,
    },
    total=False,
)

FunctionRequestTypeDef = TypedDict(
    "FunctionRequestTypeDef",
    {
        "implementedBy": DataConnectorTypeDef,
        "requiredProperties": Sequence[str],
        "scope": ScopeType,
    },
    total=False,
)

FunctionResponseTypeDef = TypedDict(
    "FunctionResponseTypeDef",
    {
        "implementedBy": DataConnectorTypeDef,
        "isInherited": bool,
        "requiredProperties": List[str],
        "scope": ScopeType,
    },
    total=False,
)

GetPropertyValueResponseTypeDef = TypedDict(
    "GetPropertyValueResponseTypeDef",
    {
        "propertyValues": Dict[str, PropertyLatestValueTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredComponentTypeSummaryTypeDef = TypedDict(
    "_RequiredComponentTypeSummaryTypeDef",
    {
        "arn": str,
        "componentTypeId": str,
        "creationDateTime": datetime,
        "updateDateTime": datetime,
    },
)
_OptionalComponentTypeSummaryTypeDef = TypedDict(
    "_OptionalComponentTypeSummaryTypeDef",
    {
        "description": str,
        "status": StatusTypeDef,
    },
    total=False,
)


class ComponentTypeSummaryTypeDef(
    _RequiredComponentTypeSummaryTypeDef, _OptionalComponentTypeSummaryTypeDef
):
    pass


_RequiredEntitySummaryTypeDef = TypedDict(
    "_RequiredEntitySummaryTypeDef",
    {
        "arn": str,
        "creationDateTime": datetime,
        "entityId": str,
        "entityName": str,
        "status": StatusTypeDef,
        "updateDateTime": datetime,
    },
)
_OptionalEntitySummaryTypeDef = TypedDict(
    "_OptionalEntitySummaryTypeDef",
    {
        "description": str,
        "hasChildEntities": bool,
        "parentEntityId": str,
    },
    total=False,
)


class EntitySummaryTypeDef(_RequiredEntitySummaryTypeDef, _OptionalEntitySummaryTypeDef):
    pass


ComponentResponseTypeDef = TypedDict(
    "ComponentResponseTypeDef",
    {
        "componentName": str,
        "componentTypeId": str,
        "definedIn": str,
        "description": str,
        "properties": Dict[str, PropertyResponseTypeDef],
        "status": StatusTypeDef,
    },
    total=False,
)

BatchPutPropertyErrorTypeDef = TypedDict(
    "BatchPutPropertyErrorTypeDef",
    {
        "entry": PropertyValueEntryTypeDef,
        "errorCode": str,
        "errorMessage": str,
    },
)

BatchPutPropertyValuesRequestRequestTypeDef = TypedDict(
    "BatchPutPropertyValuesRequestRequestTypeDef",
    {
        "entries": Sequence[PropertyValueEntryTypeDef],
        "workspaceId": str,
    },
)

GetPropertyValueHistoryResponseTypeDef = TypedDict(
    "GetPropertyValueHistoryResponseTypeDef",
    {
        "nextToken": str,
        "propertyValues": List[PropertyValueHistoryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateEntityRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEntityRequestRequestTypeDef",
    {
        "entityName": str,
        "workspaceId": str,
    },
)
_OptionalCreateEntityRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEntityRequestRequestTypeDef",
    {
        "components": Mapping[str, ComponentRequestTypeDef],
        "description": str,
        "entityId": str,
        "parentEntityId": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateEntityRequestRequestTypeDef(
    _RequiredCreateEntityRequestRequestTypeDef, _OptionalCreateEntityRequestRequestTypeDef
):
    pass


_RequiredUpdateEntityRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateEntityRequestRequestTypeDef",
    {
        "entityId": str,
        "workspaceId": str,
    },
)
_OptionalUpdateEntityRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateEntityRequestRequestTypeDef",
    {
        "componentUpdates": Mapping[str, ComponentUpdateRequestTypeDef],
        "description": str,
        "entityName": str,
        "parentEntityUpdate": ParentEntityUpdateRequestTypeDef,
    },
    total=False,
)


class UpdateEntityRequestRequestTypeDef(
    _RequiredUpdateEntityRequestRequestTypeDef, _OptionalUpdateEntityRequestRequestTypeDef
):
    pass


_RequiredCreateComponentTypeRequestRequestTypeDef = TypedDict(
    "_RequiredCreateComponentTypeRequestRequestTypeDef",
    {
        "componentTypeId": str,
        "workspaceId": str,
    },
)
_OptionalCreateComponentTypeRequestRequestTypeDef = TypedDict(
    "_OptionalCreateComponentTypeRequestRequestTypeDef",
    {
        "description": str,
        "extendsFrom": Sequence[str],
        "functions": Mapping[str, FunctionRequestTypeDef],
        "isSingleton": bool,
        "propertyDefinitions": Mapping[str, PropertyDefinitionRequestTypeDef],
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateComponentTypeRequestRequestTypeDef(
    _RequiredCreateComponentTypeRequestRequestTypeDef,
    _OptionalCreateComponentTypeRequestRequestTypeDef,
):
    pass


_RequiredUpdateComponentTypeRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateComponentTypeRequestRequestTypeDef",
    {
        "componentTypeId": str,
        "workspaceId": str,
    },
)
_OptionalUpdateComponentTypeRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateComponentTypeRequestRequestTypeDef",
    {
        "description": str,
        "extendsFrom": Sequence[str],
        "functions": Mapping[str, FunctionRequestTypeDef],
        "isSingleton": bool,
        "propertyDefinitions": Mapping[str, PropertyDefinitionRequestTypeDef],
    },
    total=False,
)


class UpdateComponentTypeRequestRequestTypeDef(
    _RequiredUpdateComponentTypeRequestRequestTypeDef,
    _OptionalUpdateComponentTypeRequestRequestTypeDef,
):
    pass


GetComponentTypeResponseTypeDef = TypedDict(
    "GetComponentTypeResponseTypeDef",
    {
        "arn": str,
        "componentTypeId": str,
        "creationDateTime": datetime,
        "description": str,
        "extendsFrom": List[str],
        "functions": Dict[str, FunctionResponseTypeDef],
        "isAbstract": bool,
        "isSchemaInitialized": bool,
        "isSingleton": bool,
        "propertyDefinitions": Dict[str, PropertyDefinitionResponseTypeDef],
        "status": StatusTypeDef,
        "updateDateTime": datetime,
        "workspaceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListComponentTypesResponseTypeDef = TypedDict(
    "ListComponentTypesResponseTypeDef",
    {
        "componentTypeSummaries": List[ComponentTypeSummaryTypeDef],
        "maxResults": int,
        "nextToken": str,
        "workspaceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEntitiesResponseTypeDef = TypedDict(
    "ListEntitiesResponseTypeDef",
    {
        "entitySummaries": List[EntitySummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEntityResponseTypeDef = TypedDict(
    "GetEntityResponseTypeDef",
    {
        "arn": str,
        "components": Dict[str, ComponentResponseTypeDef],
        "creationDateTime": datetime,
        "description": str,
        "entityId": str,
        "entityName": str,
        "hasChildEntities": bool,
        "parentEntityId": str,
        "status": StatusTypeDef,
        "updateDateTime": datetime,
        "workspaceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchPutPropertyErrorEntryTypeDef = TypedDict(
    "BatchPutPropertyErrorEntryTypeDef",
    {
        "errors": List[BatchPutPropertyErrorTypeDef],
    },
)

BatchPutPropertyValuesResponseTypeDef = TypedDict(
    "BatchPutPropertyValuesResponseTypeDef",
    {
        "errorEntries": List[BatchPutPropertyErrorEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
