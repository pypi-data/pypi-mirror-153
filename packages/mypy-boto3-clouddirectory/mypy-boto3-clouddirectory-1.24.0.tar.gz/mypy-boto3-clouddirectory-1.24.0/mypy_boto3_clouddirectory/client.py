"""
Type annotations for clouddirectory service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_clouddirectory.client import CloudDirectoryClient

    session = Session()
    client: CloudDirectoryClient = session.client("clouddirectory")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import ConsistencyLevelType, DirectoryStateType, FacetStyleType, ObjectTypeType
from .paginator import (
    ListAppliedSchemaArnsPaginator,
    ListAttachedIndicesPaginator,
    ListDevelopmentSchemaArnsPaginator,
    ListDirectoriesPaginator,
    ListFacetAttributesPaginator,
    ListFacetNamesPaginator,
    ListIncomingTypedLinksPaginator,
    ListIndexPaginator,
    ListManagedSchemaArnsPaginator,
    ListObjectAttributesPaginator,
    ListObjectParentPathsPaginator,
    ListObjectPoliciesPaginator,
    ListOutgoingTypedLinksPaginator,
    ListPolicyAttachmentsPaginator,
    ListPublishedSchemaArnsPaginator,
    ListTagsForResourcePaginator,
    ListTypedLinkFacetAttributesPaginator,
    ListTypedLinkFacetNamesPaginator,
    LookupPolicyPaginator,
)
from .type_defs import (
    ApplySchemaResponseTypeDef,
    AttachObjectResponseTypeDef,
    AttachToIndexResponseTypeDef,
    AttachTypedLinkResponseTypeDef,
    AttributeKeyAndValueTypeDef,
    AttributeKeyTypeDef,
    AttributeNameAndValueTypeDef,
    BatchReadOperationTypeDef,
    BatchReadResponseTypeDef,
    BatchWriteOperationTypeDef,
    BatchWriteResponseTypeDef,
    CreateDirectoryResponseTypeDef,
    CreateIndexResponseTypeDef,
    CreateObjectResponseTypeDef,
    CreateSchemaResponseTypeDef,
    DeleteDirectoryResponseTypeDef,
    DeleteSchemaResponseTypeDef,
    DetachFromIndexResponseTypeDef,
    DetachObjectResponseTypeDef,
    DisableDirectoryResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableDirectoryResponseTypeDef,
    FacetAttributeTypeDef,
    FacetAttributeUpdateTypeDef,
    GetAppliedSchemaVersionResponseTypeDef,
    GetDirectoryResponseTypeDef,
    GetFacetResponseTypeDef,
    GetLinkAttributesResponseTypeDef,
    GetObjectAttributesResponseTypeDef,
    GetObjectInformationResponseTypeDef,
    GetSchemaAsJsonResponseTypeDef,
    GetTypedLinkFacetInformationResponseTypeDef,
    LinkAttributeUpdateTypeDef,
    ListAppliedSchemaArnsResponseTypeDef,
    ListAttachedIndicesResponseTypeDef,
    ListDevelopmentSchemaArnsResponseTypeDef,
    ListDirectoriesResponseTypeDef,
    ListFacetAttributesResponseTypeDef,
    ListFacetNamesResponseTypeDef,
    ListIncomingTypedLinksResponseTypeDef,
    ListIndexResponseTypeDef,
    ListManagedSchemaArnsResponseTypeDef,
    ListObjectAttributesResponseTypeDef,
    ListObjectChildrenResponseTypeDef,
    ListObjectParentPathsResponseTypeDef,
    ListObjectParentsResponseTypeDef,
    ListObjectPoliciesResponseTypeDef,
    ListOutgoingTypedLinksResponseTypeDef,
    ListPolicyAttachmentsResponseTypeDef,
    ListPublishedSchemaArnsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTypedLinkFacetAttributesResponseTypeDef,
    ListTypedLinkFacetNamesResponseTypeDef,
    LookupPolicyResponseTypeDef,
    ObjectAttributeRangeTypeDef,
    ObjectAttributeUpdateTypeDef,
    ObjectReferenceTypeDef,
    PublishSchemaResponseTypeDef,
    PutSchemaFromJsonResponseTypeDef,
    SchemaFacetTypeDef,
    TagTypeDef,
    TypedLinkAttributeRangeTypeDef,
    TypedLinkFacetAttributeUpdateTypeDef,
    TypedLinkFacetTypeDef,
    TypedLinkSchemaAndFacetNameTypeDef,
    TypedLinkSpecifierTypeDef,
    UpdateObjectAttributesResponseTypeDef,
    UpdateSchemaResponseTypeDef,
    UpgradeAppliedSchemaResponseTypeDef,
    UpgradePublishedSchemaResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CloudDirectoryClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BatchWriteException: Type[BotocoreClientError]
    CannotListParentOfRootException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DirectoryAlreadyExistsException: Type[BotocoreClientError]
    DirectoryDeletedException: Type[BotocoreClientError]
    DirectoryNotDisabledException: Type[BotocoreClientError]
    DirectoryNotEnabledException: Type[BotocoreClientError]
    FacetAlreadyExistsException: Type[BotocoreClientError]
    FacetInUseException: Type[BotocoreClientError]
    FacetNotFoundException: Type[BotocoreClientError]
    FacetValidationException: Type[BotocoreClientError]
    IncompatibleSchemaException: Type[BotocoreClientError]
    IndexedAttributeMissingException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidArnException: Type[BotocoreClientError]
    InvalidAttachmentException: Type[BotocoreClientError]
    InvalidFacetUpdateException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidRuleException: Type[BotocoreClientError]
    InvalidSchemaDocException: Type[BotocoreClientError]
    InvalidTaggingRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    LinkNameAlreadyInUseException: Type[BotocoreClientError]
    NotIndexException: Type[BotocoreClientError]
    NotNodeException: Type[BotocoreClientError]
    NotPolicyException: Type[BotocoreClientError]
    ObjectAlreadyDetachedException: Type[BotocoreClientError]
    ObjectNotDetachedException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    RetryableConflictException: Type[BotocoreClientError]
    SchemaAlreadyExistsException: Type[BotocoreClientError]
    SchemaAlreadyPublishedException: Type[BotocoreClientError]
    StillContainsLinksException: Type[BotocoreClientError]
    UnsupportedIndexTypeException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CloudDirectoryClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudDirectoryClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#exceptions)
        """

    def add_facet_to_object(
        self,
        *,
        DirectoryArn: str,
        SchemaFacet: SchemaFacetTypeDef,
        ObjectReference: ObjectReferenceTypeDef,
        ObjectAttributeList: Sequence[AttributeKeyAndValueTypeDef] = ...
    ) -> Dict[str, Any]:
        """
        Adds a new  Facet to an object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.add_facet_to_object)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#add_facet_to_object)
        """

    def apply_schema(
        self, *, PublishedSchemaArn: str, DirectoryArn: str
    ) -> ApplySchemaResponseTypeDef:
        """
        Copies the input published schema, at the specified version, into the  Directory
        with the same name and version as that of the published schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.apply_schema)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#apply_schema)
        """

    def attach_object(
        self,
        *,
        DirectoryArn: str,
        ParentReference: ObjectReferenceTypeDef,
        ChildReference: ObjectReferenceTypeDef,
        LinkName: str
    ) -> AttachObjectResponseTypeDef:
        """
        Attaches an existing object to another object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.attach_object)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#attach_object)
        """

    def attach_policy(
        self,
        *,
        DirectoryArn: str,
        PolicyReference: ObjectReferenceTypeDef,
        ObjectReference: ObjectReferenceTypeDef
    ) -> Dict[str, Any]:
        """
        Attaches a policy object to a regular object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.attach_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#attach_policy)
        """

    def attach_to_index(
        self,
        *,
        DirectoryArn: str,
        IndexReference: ObjectReferenceTypeDef,
        TargetReference: ObjectReferenceTypeDef
    ) -> AttachToIndexResponseTypeDef:
        """
        Attaches the specified object to the specified index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.attach_to_index)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#attach_to_index)
        """

    def attach_typed_link(
        self,
        *,
        DirectoryArn: str,
        SourceObjectReference: ObjectReferenceTypeDef,
        TargetObjectReference: ObjectReferenceTypeDef,
        TypedLinkFacet: TypedLinkSchemaAndFacetNameTypeDef,
        Attributes: Sequence[AttributeNameAndValueTypeDef]
    ) -> AttachTypedLinkResponseTypeDef:
        """
        Attaches a typed link to a specified source and target object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.attach_typed_link)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#attach_typed_link)
        """

    def batch_read(
        self,
        *,
        DirectoryArn: str,
        Operations: Sequence[BatchReadOperationTypeDef],
        ConsistencyLevel: ConsistencyLevelType = ...
    ) -> BatchReadResponseTypeDef:
        """
        Performs all the read operations in a batch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.batch_read)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#batch_read)
        """

    def batch_write(
        self, *, DirectoryArn: str, Operations: Sequence[BatchWriteOperationTypeDef]
    ) -> BatchWriteResponseTypeDef:
        """
        Performs all the write operations in a batch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.batch_write)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#batch_write)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#can_paginate)
        """

    def create_directory(self, *, Name: str, SchemaArn: str) -> CreateDirectoryResponseTypeDef:
        """
        Creates a  Directory by copying the published schema into the directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.create_directory)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#create_directory)
        """

    def create_facet(
        self,
        *,
        SchemaArn: str,
        Name: str,
        Attributes: Sequence[FacetAttributeTypeDef] = ...,
        ObjectType: ObjectTypeType = ...,
        FacetStyle: FacetStyleType = ...
    ) -> Dict[str, Any]:
        """
        Creates a new  Facet in a schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.create_facet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#create_facet)
        """

    def create_index(
        self,
        *,
        DirectoryArn: str,
        OrderedIndexedAttributeList: Sequence[AttributeKeyTypeDef],
        IsUnique: bool,
        ParentReference: ObjectReferenceTypeDef = ...,
        LinkName: str = ...
    ) -> CreateIndexResponseTypeDef:
        """
        Creates an index object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.create_index)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#create_index)
        """

    def create_object(
        self,
        *,
        DirectoryArn: str,
        SchemaFacets: Sequence[SchemaFacetTypeDef],
        ObjectAttributeList: Sequence[AttributeKeyAndValueTypeDef] = ...,
        ParentReference: ObjectReferenceTypeDef = ...,
        LinkName: str = ...
    ) -> CreateObjectResponseTypeDef:
        """
        Creates an object in a  Directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.create_object)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#create_object)
        """

    def create_schema(self, *, Name: str) -> CreateSchemaResponseTypeDef:
        """
        Creates a new schema in a development state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.create_schema)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#create_schema)
        """

    def create_typed_link_facet(
        self, *, SchemaArn: str, Facet: TypedLinkFacetTypeDef
    ) -> Dict[str, Any]:
        """
        Creates a  TypedLinkFacet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.create_typed_link_facet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#create_typed_link_facet)
        """

    def delete_directory(self, *, DirectoryArn: str) -> DeleteDirectoryResponseTypeDef:
        """
        Deletes a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.delete_directory)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#delete_directory)
        """

    def delete_facet(self, *, SchemaArn: str, Name: str) -> Dict[str, Any]:
        """
        Deletes a given  Facet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.delete_facet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#delete_facet)
        """

    def delete_object(
        self, *, DirectoryArn: str, ObjectReference: ObjectReferenceTypeDef
    ) -> Dict[str, Any]:
        """
        Deletes an object and its associated attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.delete_object)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#delete_object)
        """

    def delete_schema(self, *, SchemaArn: str) -> DeleteSchemaResponseTypeDef:
        """
        Deletes a given schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.delete_schema)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#delete_schema)
        """

    def delete_typed_link_facet(self, *, SchemaArn: str, Name: str) -> Dict[str, Any]:
        """
        Deletes a  TypedLinkFacet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.delete_typed_link_facet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#delete_typed_link_facet)
        """

    def detach_from_index(
        self,
        *,
        DirectoryArn: str,
        IndexReference: ObjectReferenceTypeDef,
        TargetReference: ObjectReferenceTypeDef
    ) -> DetachFromIndexResponseTypeDef:
        """
        Detaches the specified object from the specified index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.detach_from_index)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#detach_from_index)
        """

    def detach_object(
        self, *, DirectoryArn: str, ParentReference: ObjectReferenceTypeDef, LinkName: str
    ) -> DetachObjectResponseTypeDef:
        """
        Detaches a given object from the parent object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.detach_object)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#detach_object)
        """

    def detach_policy(
        self,
        *,
        DirectoryArn: str,
        PolicyReference: ObjectReferenceTypeDef,
        ObjectReference: ObjectReferenceTypeDef
    ) -> Dict[str, Any]:
        """
        Detaches a policy from an object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.detach_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#detach_policy)
        """

    def detach_typed_link(
        self, *, DirectoryArn: str, TypedLinkSpecifier: TypedLinkSpecifierTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        Detaches a typed link from a specified source and target object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.detach_typed_link)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#detach_typed_link)
        """

    def disable_directory(self, *, DirectoryArn: str) -> DisableDirectoryResponseTypeDef:
        """
        Disables the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.disable_directory)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#disable_directory)
        """

    def enable_directory(self, *, DirectoryArn: str) -> EnableDirectoryResponseTypeDef:
        """
        Enables the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.enable_directory)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#enable_directory)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#generate_presigned_url)
        """

    def get_applied_schema_version(
        self, *, SchemaArn: str
    ) -> GetAppliedSchemaVersionResponseTypeDef:
        """
        Returns current applied schema version ARN, including the minor version in use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_applied_schema_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_applied_schema_version)
        """

    def get_directory(self, *, DirectoryArn: str) -> GetDirectoryResponseTypeDef:
        """
        Retrieves metadata about a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_directory)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_directory)
        """

    def get_facet(self, *, SchemaArn: str, Name: str) -> GetFacetResponseTypeDef:
        """
        Gets details of the  Facet , such as facet name, attributes,  Rule s, or
        `ObjectType`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_facet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_facet)
        """

    def get_link_attributes(
        self,
        *,
        DirectoryArn: str,
        TypedLinkSpecifier: TypedLinkSpecifierTypeDef,
        AttributeNames: Sequence[str],
        ConsistencyLevel: ConsistencyLevelType = ...
    ) -> GetLinkAttributesResponseTypeDef:
        """
        Retrieves attributes that are associated with a typed link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_link_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_link_attributes)
        """

    def get_object_attributes(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: ObjectReferenceTypeDef,
        SchemaFacet: SchemaFacetTypeDef,
        AttributeNames: Sequence[str],
        ConsistencyLevel: ConsistencyLevelType = ...
    ) -> GetObjectAttributesResponseTypeDef:
        """
        Retrieves attributes within a facet that are associated with an object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_object_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_object_attributes)
        """

    def get_object_information(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: ObjectReferenceTypeDef,
        ConsistencyLevel: ConsistencyLevelType = ...
    ) -> GetObjectInformationResponseTypeDef:
        """
        Retrieves metadata about an object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_object_information)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_object_information)
        """

    def get_schema_as_json(self, *, SchemaArn: str) -> GetSchemaAsJsonResponseTypeDef:
        """
        Retrieves a JSON representation of the schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_schema_as_json)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_schema_as_json)
        """

    def get_typed_link_facet_information(
        self, *, SchemaArn: str, Name: str
    ) -> GetTypedLinkFacetInformationResponseTypeDef:
        """
        Returns the identity attribute order for a specific  TypedLinkFacet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_typed_link_facet_information)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_typed_link_facet_information)
        """

    def list_applied_schema_arns(
        self,
        *,
        DirectoryArn: str,
        SchemaArn: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListAppliedSchemaArnsResponseTypeDef:
        """
        Lists schema major versions applied to a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_applied_schema_arns)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_applied_schema_arns)
        """

    def list_attached_indices(
        self,
        *,
        DirectoryArn: str,
        TargetReference: ObjectReferenceTypeDef,
        NextToken: str = ...,
        MaxResults: int = ...,
        ConsistencyLevel: ConsistencyLevelType = ...
    ) -> ListAttachedIndicesResponseTypeDef:
        """
        Lists indices attached to the specified object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_attached_indices)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_attached_indices)
        """

    def list_development_schema_arns(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDevelopmentSchemaArnsResponseTypeDef:
        """
        Retrieves each Amazon Resource Name (ARN) of schemas in the development state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_development_schema_arns)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_development_schema_arns)
        """

    def list_directories(
        self, *, NextToken: str = ..., MaxResults: int = ..., state: DirectoryStateType = ...
    ) -> ListDirectoriesResponseTypeDef:
        """
        Lists directories created within an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_directories)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_directories)
        """

    def list_facet_attributes(
        self, *, SchemaArn: str, Name: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListFacetAttributesResponseTypeDef:
        """
        Retrieves attributes attached to the facet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_facet_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_facet_attributes)
        """

    def list_facet_names(
        self, *, SchemaArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListFacetNamesResponseTypeDef:
        """
        Retrieves the names of facets that exist in a schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_facet_names)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_facet_names)
        """

    def list_incoming_typed_links(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: ObjectReferenceTypeDef,
        FilterAttributeRanges: Sequence[TypedLinkAttributeRangeTypeDef] = ...,
        FilterTypedLink: TypedLinkSchemaAndFacetNameTypeDef = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        ConsistencyLevel: ConsistencyLevelType = ...
    ) -> ListIncomingTypedLinksResponseTypeDef:
        """
        Returns a paginated list of all the incoming  TypedLinkSpecifier information for
        an object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_incoming_typed_links)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_incoming_typed_links)
        """

    def list_index(
        self,
        *,
        DirectoryArn: str,
        IndexReference: ObjectReferenceTypeDef,
        RangesOnIndexedValues: Sequence[ObjectAttributeRangeTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        ConsistencyLevel: ConsistencyLevelType = ...
    ) -> ListIndexResponseTypeDef:
        """
        Lists objects attached to the specified index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_index)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_index)
        """

    def list_managed_schema_arns(
        self, *, SchemaArn: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListManagedSchemaArnsResponseTypeDef:
        """
        Lists the major version families of each managed schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_managed_schema_arns)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_managed_schema_arns)
        """

    def list_object_attributes(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: ObjectReferenceTypeDef,
        NextToken: str = ...,
        MaxResults: int = ...,
        ConsistencyLevel: ConsistencyLevelType = ...,
        FacetFilter: SchemaFacetTypeDef = ...
    ) -> ListObjectAttributesResponseTypeDef:
        """
        Lists all attributes that are associated with an object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_object_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_object_attributes)
        """

    def list_object_children(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: ObjectReferenceTypeDef,
        NextToken: str = ...,
        MaxResults: int = ...,
        ConsistencyLevel: ConsistencyLevelType = ...
    ) -> ListObjectChildrenResponseTypeDef:
        """
        Returns a paginated list of child objects that are associated with a given
        object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_object_children)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_object_children)
        """

    def list_object_parent_paths(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: ObjectReferenceTypeDef,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListObjectParentPathsResponseTypeDef:
        """
        Retrieves all available parent paths for any object type such as node, leaf
        node, policy node, and index node objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_object_parent_paths)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_object_parent_paths)
        """

    def list_object_parents(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: ObjectReferenceTypeDef,
        NextToken: str = ...,
        MaxResults: int = ...,
        ConsistencyLevel: ConsistencyLevelType = ...,
        IncludeAllLinksToEachParent: bool = ...
    ) -> ListObjectParentsResponseTypeDef:
        """
        Lists parent objects that are associated with a given object in pagination
        fashion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_object_parents)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_object_parents)
        """

    def list_object_policies(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: ObjectReferenceTypeDef,
        NextToken: str = ...,
        MaxResults: int = ...,
        ConsistencyLevel: ConsistencyLevelType = ...
    ) -> ListObjectPoliciesResponseTypeDef:
        """
        Returns policies attached to an object in pagination fashion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_object_policies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_object_policies)
        """

    def list_outgoing_typed_links(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: ObjectReferenceTypeDef,
        FilterAttributeRanges: Sequence[TypedLinkAttributeRangeTypeDef] = ...,
        FilterTypedLink: TypedLinkSchemaAndFacetNameTypeDef = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        ConsistencyLevel: ConsistencyLevelType = ...
    ) -> ListOutgoingTypedLinksResponseTypeDef:
        """
        Returns a paginated list of all the outgoing  TypedLinkSpecifier information for
        an object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_outgoing_typed_links)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_outgoing_typed_links)
        """

    def list_policy_attachments(
        self,
        *,
        DirectoryArn: str,
        PolicyReference: ObjectReferenceTypeDef,
        NextToken: str = ...,
        MaxResults: int = ...,
        ConsistencyLevel: ConsistencyLevelType = ...
    ) -> ListPolicyAttachmentsResponseTypeDef:
        """
        Returns all of the `ObjectIdentifiers` to which a given policy is attached.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_policy_attachments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_policy_attachments)
        """

    def list_published_schema_arns(
        self, *, SchemaArn: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListPublishedSchemaArnsResponseTypeDef:
        """
        Lists the major version families of each published schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_published_schema_arns)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_published_schema_arns)
        """

    def list_tags_for_resource(
        self, *, ResourceArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_tags_for_resource)
        """

    def list_typed_link_facet_attributes(
        self, *, SchemaArn: str, Name: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListTypedLinkFacetAttributesResponseTypeDef:
        """
        Returns a paginated list of all attribute definitions for a particular
        TypedLinkFacet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_typed_link_facet_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_typed_link_facet_attributes)
        """

    def list_typed_link_facet_names(
        self, *, SchemaArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListTypedLinkFacetNamesResponseTypeDef:
        """
        Returns a paginated list of `TypedLink` facet names for a particular schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.list_typed_link_facet_names)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#list_typed_link_facet_names)
        """

    def lookup_policy(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: ObjectReferenceTypeDef,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> LookupPolicyResponseTypeDef:
        """
        Lists all policies from the root of the  Directory to the object specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.lookup_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#lookup_policy)
        """

    def publish_schema(
        self, *, DevelopmentSchemaArn: str, Version: str, MinorVersion: str = ..., Name: str = ...
    ) -> PublishSchemaResponseTypeDef:
        """
        Publishes a development schema with a major version and a recommended minor
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.publish_schema)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#publish_schema)
        """

    def put_schema_from_json(
        self, *, SchemaArn: str, Document: str
    ) -> PutSchemaFromJsonResponseTypeDef:
        """
        Allows a schema to be updated using JSON upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.put_schema_from_json)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#put_schema_from_json)
        """

    def remove_facet_from_object(
        self,
        *,
        DirectoryArn: str,
        SchemaFacet: SchemaFacetTypeDef,
        ObjectReference: ObjectReferenceTypeDef
    ) -> Dict[str, Any]:
        """
        Removes the specified facet from the specified object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.remove_facet_from_object)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#remove_facet_from_object)
        """

    def tag_resource(self, *, ResourceArn: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        An API operation for adding tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        An API operation for removing tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#untag_resource)
        """

    def update_facet(
        self,
        *,
        SchemaArn: str,
        Name: str,
        AttributeUpdates: Sequence[FacetAttributeUpdateTypeDef] = ...,
        ObjectType: ObjectTypeType = ...
    ) -> Dict[str, Any]:
        """
        Does the following * Adds new `Attributes` , `Rules` , or `ObjectTypes` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.update_facet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#update_facet)
        """

    def update_link_attributes(
        self,
        *,
        DirectoryArn: str,
        TypedLinkSpecifier: TypedLinkSpecifierTypeDef,
        AttributeUpdates: Sequence[LinkAttributeUpdateTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a given typed link’s attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.update_link_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#update_link_attributes)
        """

    def update_object_attributes(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: ObjectReferenceTypeDef,
        AttributeUpdates: Sequence[ObjectAttributeUpdateTypeDef]
    ) -> UpdateObjectAttributesResponseTypeDef:
        """
        Updates a given object's attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.update_object_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#update_object_attributes)
        """

    def update_schema(self, *, SchemaArn: str, Name: str) -> UpdateSchemaResponseTypeDef:
        """
        Updates the schema name with a new name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.update_schema)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#update_schema)
        """

    def update_typed_link_facet(
        self,
        *,
        SchemaArn: str,
        Name: str,
        AttributeUpdates: Sequence[TypedLinkFacetAttributeUpdateTypeDef],
        IdentityAttributeOrder: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Updates a  TypedLinkFacet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.update_typed_link_facet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#update_typed_link_facet)
        """

    def upgrade_applied_schema(
        self, *, PublishedSchemaArn: str, DirectoryArn: str, DryRun: bool = ...
    ) -> UpgradeAppliedSchemaResponseTypeDef:
        """
        Upgrades a single directory in-place using the `PublishedSchemaArn` with schema
        updates found in `MinorVersion`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.upgrade_applied_schema)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#upgrade_applied_schema)
        """

    def upgrade_published_schema(
        self,
        *,
        DevelopmentSchemaArn: str,
        PublishedSchemaArn: str,
        MinorVersion: str,
        DryRun: bool = ...
    ) -> UpgradePublishedSchemaResponseTypeDef:
        """
        Upgrades a published schema under a new minor version revision using the current
        contents of `DevelopmentSchemaArn` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.upgrade_published_schema)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#upgrade_published_schema)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_applied_schema_arns"]
    ) -> ListAppliedSchemaArnsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_attached_indices"]
    ) -> ListAttachedIndicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_development_schema_arns"]
    ) -> ListDevelopmentSchemaArnsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_directories"]
    ) -> ListDirectoriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_facet_attributes"]
    ) -> ListFacetAttributesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_facet_names"]) -> ListFacetNamesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_incoming_typed_links"]
    ) -> ListIncomingTypedLinksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_index"]) -> ListIndexPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_managed_schema_arns"]
    ) -> ListManagedSchemaArnsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_object_attributes"]
    ) -> ListObjectAttributesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_object_parent_paths"]
    ) -> ListObjectParentPathsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_object_policies"]
    ) -> ListObjectPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_outgoing_typed_links"]
    ) -> ListOutgoingTypedLinksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_policy_attachments"]
    ) -> ListPolicyAttachmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_published_schema_arns"]
    ) -> ListPublishedSchemaArnsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_typed_link_facet_attributes"]
    ) -> ListTypedLinkFacetAttributesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_typed_link_facet_names"]
    ) -> ListTypedLinkFacetNamesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["lookup_policy"]) -> LookupPolicyPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/client/#get_paginator)
        """
