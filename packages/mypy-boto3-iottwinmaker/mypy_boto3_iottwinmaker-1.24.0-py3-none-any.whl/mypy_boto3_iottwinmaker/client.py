"""
Type annotations for iottwinmaker service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iottwinmaker.client import IoTTwinMakerClient

    session = Session()
    client: IoTTwinMakerClient = session.client("iottwinmaker")
    ```
"""
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union

from botocore.client import BaseClient, ClientMeta

from .literals import OrderByTimeType
from .type_defs import (
    BatchPutPropertyValuesResponseTypeDef,
    ComponentRequestTypeDef,
    ComponentUpdateRequestTypeDef,
    CreateComponentTypeResponseTypeDef,
    CreateEntityResponseTypeDef,
    CreateSceneResponseTypeDef,
    CreateWorkspaceResponseTypeDef,
    DeleteComponentTypeResponseTypeDef,
    DeleteEntityResponseTypeDef,
    FunctionRequestTypeDef,
    GetComponentTypeResponseTypeDef,
    GetEntityResponseTypeDef,
    GetPropertyValueHistoryResponseTypeDef,
    GetPropertyValueResponseTypeDef,
    GetSceneResponseTypeDef,
    GetWorkspaceResponseTypeDef,
    InterpolationParametersTypeDef,
    ListComponentTypesFilterTypeDef,
    ListComponentTypesResponseTypeDef,
    ListEntitiesFilterTypeDef,
    ListEntitiesResponseTypeDef,
    ListScenesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorkspacesResponseTypeDef,
    ParentEntityUpdateRequestTypeDef,
    PropertyDefinitionRequestTypeDef,
    PropertyFilterTypeDef,
    PropertyValueEntryTypeDef,
    UpdateComponentTypeResponseTypeDef,
    UpdateEntityResponseTypeDef,
    UpdateSceneResponseTypeDef,
    UpdateWorkspaceResponseTypeDef,
)

__all__ = ("IoTTwinMakerClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ConnectorFailureException: Type[BotocoreClientError]
    ConnectorTimeoutException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class IoTTwinMakerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTTwinMakerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#exceptions)
        """

    def batch_put_property_values(
        self, *, entries: Sequence[PropertyValueEntryTypeDef], workspaceId: str
    ) -> BatchPutPropertyValuesResponseTypeDef:
        """
        Sets values for multiple time series properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.batch_put_property_values)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#batch_put_property_values)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#can_paginate)
        """

    def create_component_type(
        self,
        *,
        componentTypeId: str,
        workspaceId: str,
        description: str = ...,
        extendsFrom: Sequence[str] = ...,
        functions: Mapping[str, FunctionRequestTypeDef] = ...,
        isSingleton: bool = ...,
        propertyDefinitions: Mapping[str, PropertyDefinitionRequestTypeDef] = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateComponentTypeResponseTypeDef:
        """
        Creates a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.create_component_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#create_component_type)
        """

    def create_entity(
        self,
        *,
        entityName: str,
        workspaceId: str,
        components: Mapping[str, ComponentRequestTypeDef] = ...,
        description: str = ...,
        entityId: str = ...,
        parentEntityId: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateEntityResponseTypeDef:
        """
        Creates an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.create_entity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#create_entity)
        """

    def create_scene(
        self,
        *,
        contentLocation: str,
        sceneId: str,
        workspaceId: str,
        capabilities: Sequence[str] = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateSceneResponseTypeDef:
        """
        Creates a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.create_scene)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#create_scene)
        """

    def create_workspace(
        self,
        *,
        role: str,
        s3Location: str,
        workspaceId: str,
        description: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateWorkspaceResponseTypeDef:
        """
        Creates a workplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.create_workspace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#create_workspace)
        """

    def delete_component_type(
        self, *, componentTypeId: str, workspaceId: str
    ) -> DeleteComponentTypeResponseTypeDef:
        """
        Deletes a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.delete_component_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#delete_component_type)
        """

    def delete_entity(
        self, *, entityId: str, workspaceId: str, isRecursive: bool = ...
    ) -> DeleteEntityResponseTypeDef:
        """
        Deletes an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.delete_entity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#delete_entity)
        """

    def delete_scene(self, *, sceneId: str, workspaceId: str) -> Dict[str, Any]:
        """
        Deletes a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.delete_scene)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#delete_scene)
        """

    def delete_workspace(self, *, workspaceId: str) -> Dict[str, Any]:
        """
        Deletes a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.delete_workspace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#delete_workspace)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#generate_presigned_url)
        """

    def get_component_type(
        self, *, componentTypeId: str, workspaceId: str
    ) -> GetComponentTypeResponseTypeDef:
        """
        Retrieves information about a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_component_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#get_component_type)
        """

    def get_entity(self, *, entityId: str, workspaceId: str) -> GetEntityResponseTypeDef:
        """
        Retrieves information about an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_entity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#get_entity)
        """

    def get_property_value(
        self,
        *,
        selectedProperties: Sequence[str],
        workspaceId: str,
        componentName: str = ...,
        componentTypeId: str = ...,
        entityId: str = ...
    ) -> GetPropertyValueResponseTypeDef:
        """
        Gets the property values for a component, component type, entity, or workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_property_value)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#get_property_value)
        """

    def get_property_value_history(
        self,
        *,
        selectedProperties: Sequence[str],
        workspaceId: str,
        componentName: str = ...,
        componentTypeId: str = ...,
        endDateTime: Union[datetime, str] = ...,
        endTime: str = ...,
        entityId: str = ...,
        interpolation: InterpolationParametersTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        orderByTime: OrderByTimeType = ...,
        propertyFilters: Sequence[PropertyFilterTypeDef] = ...,
        startDateTime: Union[datetime, str] = ...,
        startTime: str = ...
    ) -> GetPropertyValueHistoryResponseTypeDef:
        """
        Retrieves information about the history of a time series property value for a
        component, component type, entity, or workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_property_value_history)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#get_property_value_history)
        """

    def get_scene(self, *, sceneId: str, workspaceId: str) -> GetSceneResponseTypeDef:
        """
        Retrieves information about a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_scene)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#get_scene)
        """

    def get_workspace(self, *, workspaceId: str) -> GetWorkspaceResponseTypeDef:
        """
        Retrieves information about a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_workspace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#get_workspace)
        """

    def list_component_types(
        self,
        *,
        workspaceId: str,
        filters: Sequence[ListComponentTypesFilterTypeDef] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListComponentTypesResponseTypeDef:
        """
        Lists all component types in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_component_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#list_component_types)
        """

    def list_entities(
        self,
        *,
        workspaceId: str,
        filters: Sequence[ListEntitiesFilterTypeDef] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListEntitiesResponseTypeDef:
        """
        Lists all entities in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_entities)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#list_entities)
        """

    def list_scenes(
        self, *, workspaceId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListScenesResponseTypeDef:
        """
        Lists all scenes in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_scenes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#list_scenes)
        """

    def list_tags_for_resource(
        self, *, resourceARN: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags associated with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#list_tags_for_resource)
        """

    def list_workspaces(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListWorkspacesResponseTypeDef:
        """
        Retrieves information about workspaces in the current account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_workspaces)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#list_workspaces)
        """

    def tag_resource(self, *, resourceARN: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#tag_resource)
        """

    def untag_resource(self, *, resourceARN: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#untag_resource)
        """

    def update_component_type(
        self,
        *,
        componentTypeId: str,
        workspaceId: str,
        description: str = ...,
        extendsFrom: Sequence[str] = ...,
        functions: Mapping[str, FunctionRequestTypeDef] = ...,
        isSingleton: bool = ...,
        propertyDefinitions: Mapping[str, PropertyDefinitionRequestTypeDef] = ...
    ) -> UpdateComponentTypeResponseTypeDef:
        """
        Updates information in a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.update_component_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#update_component_type)
        """

    def update_entity(
        self,
        *,
        entityId: str,
        workspaceId: str,
        componentUpdates: Mapping[str, ComponentUpdateRequestTypeDef] = ...,
        description: str = ...,
        entityName: str = ...,
        parentEntityUpdate: ParentEntityUpdateRequestTypeDef = ...
    ) -> UpdateEntityResponseTypeDef:
        """
        Updates an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.update_entity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#update_entity)
        """

    def update_scene(
        self,
        *,
        sceneId: str,
        workspaceId: str,
        capabilities: Sequence[str] = ...,
        contentLocation: str = ...,
        description: str = ...
    ) -> UpdateSceneResponseTypeDef:
        """
        Updates a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.update_scene)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#update_scene)
        """

    def update_workspace(
        self, *, workspaceId: str, description: str = ..., role: str = ...
    ) -> UpdateWorkspaceResponseTypeDef:
        """
        Updates a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.update_workspace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#update_workspace)
        """
