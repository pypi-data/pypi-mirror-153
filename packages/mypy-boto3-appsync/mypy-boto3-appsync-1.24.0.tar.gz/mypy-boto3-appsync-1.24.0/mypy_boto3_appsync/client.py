"""
Type annotations for appsync service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_appsync.client import AppSyncClient

    session = Session()
    client: AppSyncClient = session.client("appsync")
    ```
"""
import sys
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta
from botocore.response import StreamingBody

from .literals import (
    ApiCacheTypeType,
    ApiCachingBehaviorType,
    AuthenticationTypeType,
    DataSourceTypeType,
    OutputTypeType,
    ResolverKindType,
    TypeDefinitionFormatType,
)
from .paginator import (
    ListApiKeysPaginator,
    ListDataSourcesPaginator,
    ListFunctionsPaginator,
    ListGraphqlApisPaginator,
    ListResolversByFunctionPaginator,
    ListResolversPaginator,
    ListTypesPaginator,
)
from .type_defs import (
    AdditionalAuthenticationProviderTypeDef,
    AssociateApiResponseTypeDef,
    CachingConfigTypeDef,
    CreateApiCacheResponseTypeDef,
    CreateApiKeyResponseTypeDef,
    CreateDataSourceResponseTypeDef,
    CreateDomainNameResponseTypeDef,
    CreateFunctionResponseTypeDef,
    CreateGraphqlApiResponseTypeDef,
    CreateResolverResponseTypeDef,
    CreateTypeResponseTypeDef,
    DynamodbDataSourceConfigTypeDef,
    ElasticsearchDataSourceConfigTypeDef,
    GetApiAssociationResponseTypeDef,
    GetApiCacheResponseTypeDef,
    GetDataSourceResponseTypeDef,
    GetDomainNameResponseTypeDef,
    GetFunctionResponseTypeDef,
    GetGraphqlApiResponseTypeDef,
    GetIntrospectionSchemaResponseTypeDef,
    GetResolverResponseTypeDef,
    GetSchemaCreationStatusResponseTypeDef,
    GetTypeResponseTypeDef,
    HttpDataSourceConfigTypeDef,
    LambdaAuthorizerConfigTypeDef,
    LambdaDataSourceConfigTypeDef,
    ListApiKeysResponseTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDomainNamesResponseTypeDef,
    ListFunctionsResponseTypeDef,
    ListGraphqlApisResponseTypeDef,
    ListResolversByFunctionResponseTypeDef,
    ListResolversResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTypesResponseTypeDef,
    LogConfigTypeDef,
    OpenIDConnectConfigTypeDef,
    OpenSearchServiceDataSourceConfigTypeDef,
    PipelineConfigTypeDef,
    RelationalDatabaseDataSourceConfigTypeDef,
    StartSchemaCreationResponseTypeDef,
    SyncConfigTypeDef,
    UpdateApiCacheResponseTypeDef,
    UpdateApiKeyResponseTypeDef,
    UpdateDataSourceResponseTypeDef,
    UpdateDomainNameResponseTypeDef,
    UpdateFunctionResponseTypeDef,
    UpdateGraphqlApiResponseTypeDef,
    UpdateResolverResponseTypeDef,
    UpdateTypeResponseTypeDef,
    UserPoolConfigTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AppSyncClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ApiKeyLimitExceededException: Type[BotocoreClientError]
    ApiKeyValidityOutOfBoundsException: Type[BotocoreClientError]
    ApiLimitExceededException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    GraphQLSchemaException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class AppSyncClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppSyncClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#exceptions)
        """

    def associate_api(self, *, domainName: str, apiId: str) -> AssociateApiResponseTypeDef:
        """
        Maps an endpoint to your custom domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.associate_api)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#associate_api)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#can_paginate)
        """

    def create_api_cache(
        self,
        *,
        apiId: str,
        ttl: int,
        apiCachingBehavior: ApiCachingBehaviorType,
        type: ApiCacheTypeType,
        transitEncryptionEnabled: bool = ...,
        atRestEncryptionEnabled: bool = ...
    ) -> CreateApiCacheResponseTypeDef:
        """
        Creates a cache for the GraphQL API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_api_cache)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#create_api_cache)
        """

    def create_api_key(
        self, *, apiId: str, description: str = ..., expires: int = ...
    ) -> CreateApiKeyResponseTypeDef:
        """
        Creates a unique key that you can distribute to clients who invoke your API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_api_key)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#create_api_key)
        """

    def create_data_source(
        self,
        *,
        apiId: str,
        name: str,
        type: DataSourceTypeType,
        description: str = ...,
        serviceRoleArn: str = ...,
        dynamodbConfig: DynamodbDataSourceConfigTypeDef = ...,
        lambdaConfig: LambdaDataSourceConfigTypeDef = ...,
        elasticsearchConfig: ElasticsearchDataSourceConfigTypeDef = ...,
        openSearchServiceConfig: OpenSearchServiceDataSourceConfigTypeDef = ...,
        httpConfig: HttpDataSourceConfigTypeDef = ...,
        relationalDatabaseConfig: RelationalDatabaseDataSourceConfigTypeDef = ...
    ) -> CreateDataSourceResponseTypeDef:
        """
        Creates a `DataSource` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#create_data_source)
        """

    def create_domain_name(
        self, *, domainName: str, certificateArn: str, description: str = ...
    ) -> CreateDomainNameResponseTypeDef:
        """
        Creates a custom `DomainName` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_domain_name)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#create_domain_name)
        """

    def create_function(
        self,
        *,
        apiId: str,
        name: str,
        dataSourceName: str,
        functionVersion: str,
        description: str = ...,
        requestMappingTemplate: str = ...,
        responseMappingTemplate: str = ...,
        syncConfig: SyncConfigTypeDef = ...,
        maxBatchSize: int = ...
    ) -> CreateFunctionResponseTypeDef:
        """
        Creates a `Function` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_function)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#create_function)
        """

    def create_graphql_api(
        self,
        *,
        name: str,
        authenticationType: AuthenticationTypeType,
        logConfig: LogConfigTypeDef = ...,
        userPoolConfig: UserPoolConfigTypeDef = ...,
        openIDConnectConfig: OpenIDConnectConfigTypeDef = ...,
        tags: Mapping[str, str] = ...,
        additionalAuthenticationProviders: Sequence[AdditionalAuthenticationProviderTypeDef] = ...,
        xrayEnabled: bool = ...,
        lambdaAuthorizerConfig: LambdaAuthorizerConfigTypeDef = ...
    ) -> CreateGraphqlApiResponseTypeDef:
        """
        Creates a `GraphqlApi` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_graphql_api)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#create_graphql_api)
        """

    def create_resolver(
        self,
        *,
        apiId: str,
        typeName: str,
        fieldName: str,
        dataSourceName: str = ...,
        requestMappingTemplate: str = ...,
        responseMappingTemplate: str = ...,
        kind: ResolverKindType = ...,
        pipelineConfig: PipelineConfigTypeDef = ...,
        syncConfig: SyncConfigTypeDef = ...,
        cachingConfig: CachingConfigTypeDef = ...,
        maxBatchSize: int = ...
    ) -> CreateResolverResponseTypeDef:
        """
        Creates a `Resolver` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_resolver)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#create_resolver)
        """

    def create_type(
        self, *, apiId: str, definition: str, format: TypeDefinitionFormatType
    ) -> CreateTypeResponseTypeDef:
        """
        Creates a `Type` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#create_type)
        """

    def delete_api_cache(self, *, apiId: str) -> Dict[str, Any]:
        """
        Deletes an `ApiCache` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_api_cache)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#delete_api_cache)
        """

    def delete_api_key(self, *, apiId: str, id: str) -> Dict[str, Any]:
        """
        Deletes an API key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_api_key)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#delete_api_key)
        """

    def delete_data_source(self, *, apiId: str, name: str) -> Dict[str, Any]:
        """
        Deletes a `DataSource` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#delete_data_source)
        """

    def delete_domain_name(self, *, domainName: str) -> Dict[str, Any]:
        """
        Deletes a custom `DomainName` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_domain_name)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#delete_domain_name)
        """

    def delete_function(self, *, apiId: str, functionId: str) -> Dict[str, Any]:
        """
        Deletes a `Function` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_function)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#delete_function)
        """

    def delete_graphql_api(self, *, apiId: str) -> Dict[str, Any]:
        """
        Deletes a `GraphqlApi` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_graphql_api)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#delete_graphql_api)
        """

    def delete_resolver(self, *, apiId: str, typeName: str, fieldName: str) -> Dict[str, Any]:
        """
        Deletes a `Resolver` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_resolver)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#delete_resolver)
        """

    def delete_type(self, *, apiId: str, typeName: str) -> Dict[str, Any]:
        """
        Deletes a `Type` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#delete_type)
        """

    def disassociate_api(self, *, domainName: str) -> Dict[str, Any]:
        """
        Removes an `ApiAssociation` object from a custom domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.disassociate_api)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#disassociate_api)
        """

    def flush_api_cache(self, *, apiId: str) -> Dict[str, Any]:
        """
        Flushes an `ApiCache` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.flush_api_cache)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#flush_api_cache)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#generate_presigned_url)
        """

    def get_api_association(self, *, domainName: str) -> GetApiAssociationResponseTypeDef:
        """
        Retrieves an `ApiAssociation` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_api_association)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_api_association)
        """

    def get_api_cache(self, *, apiId: str) -> GetApiCacheResponseTypeDef:
        """
        Retrieves an `ApiCache` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_api_cache)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_api_cache)
        """

    def get_data_source(self, *, apiId: str, name: str) -> GetDataSourceResponseTypeDef:
        """
        Retrieves a `DataSource` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_data_source)
        """

    def get_domain_name(self, *, domainName: str) -> GetDomainNameResponseTypeDef:
        """
        Retrieves a custom `DomainName` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_domain_name)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_domain_name)
        """

    def get_function(self, *, apiId: str, functionId: str) -> GetFunctionResponseTypeDef:
        """
        Get a `Function` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_function)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_function)
        """

    def get_graphql_api(self, *, apiId: str) -> GetGraphqlApiResponseTypeDef:
        """
        Retrieves a `GraphqlApi` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_graphql_api)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_graphql_api)
        """

    def get_introspection_schema(
        self, *, apiId: str, format: OutputTypeType, includeDirectives: bool = ...
    ) -> GetIntrospectionSchemaResponseTypeDef:
        """
        Retrieves the introspection schema for a GraphQL API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_introspection_schema)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_introspection_schema)
        """

    def get_resolver(
        self, *, apiId: str, typeName: str, fieldName: str
    ) -> GetResolverResponseTypeDef:
        """
        Retrieves a `Resolver` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_resolver)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_resolver)
        """

    def get_schema_creation_status(self, *, apiId: str) -> GetSchemaCreationStatusResponseTypeDef:
        """
        Retrieves the current status of a schema creation operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_schema_creation_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_schema_creation_status)
        """

    def get_type(
        self, *, apiId: str, typeName: str, format: TypeDefinitionFormatType
    ) -> GetTypeResponseTypeDef:
        """
        Retrieves a `Type` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_type)
        """

    def list_api_keys(
        self, *, apiId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListApiKeysResponseTypeDef:
        """
        Lists the API keys for a given API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_api_keys)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#list_api_keys)
        """

    def list_data_sources(
        self, *, apiId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListDataSourcesResponseTypeDef:
        """
        Lists the data sources for a given API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_data_sources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#list_data_sources)
        """

    def list_domain_names(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListDomainNamesResponseTypeDef:
        """
        Lists multiple custom domain names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_domain_names)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#list_domain_names)
        """

    def list_functions(
        self, *, apiId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListFunctionsResponseTypeDef:
        """
        List multiple functions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_functions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#list_functions)
        """

    def list_graphql_apis(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListGraphqlApisResponseTypeDef:
        """
        Lists your GraphQL APIs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_graphql_apis)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#list_graphql_apis)
        """

    def list_resolvers(
        self, *, apiId: str, typeName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListResolversResponseTypeDef:
        """
        Lists the resolvers for a given API and type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_resolvers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#list_resolvers)
        """

    def list_resolvers_by_function(
        self, *, apiId: str, functionId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListResolversByFunctionResponseTypeDef:
        """
        List the resolvers that are associated with a specific function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_resolvers_by_function)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#list_resolvers_by_function)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#list_tags_for_resource)
        """

    def list_types(
        self,
        *,
        apiId: str,
        format: TypeDefinitionFormatType,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListTypesResponseTypeDef:
        """
        Lists the types for a given API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#list_types)
        """

    def start_schema_creation(
        self, *, apiId: str, definition: Union[str, bytes, IO[Any], StreamingBody]
    ) -> StartSchemaCreationResponseTypeDef:
        """
        Adds a new schema to your GraphQL API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.start_schema_creation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#start_schema_creation)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Tags a resource with user-supplied tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Untags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#untag_resource)
        """

    def update_api_cache(
        self,
        *,
        apiId: str,
        ttl: int,
        apiCachingBehavior: ApiCachingBehaviorType,
        type: ApiCacheTypeType
    ) -> UpdateApiCacheResponseTypeDef:
        """
        Updates the cache for the GraphQL API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_api_cache)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#update_api_cache)
        """

    def update_api_key(
        self, *, apiId: str, id: str, description: str = ..., expires: int = ...
    ) -> UpdateApiKeyResponseTypeDef:
        """
        Updates an API key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_api_key)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#update_api_key)
        """

    def update_data_source(
        self,
        *,
        apiId: str,
        name: str,
        type: DataSourceTypeType,
        description: str = ...,
        serviceRoleArn: str = ...,
        dynamodbConfig: DynamodbDataSourceConfigTypeDef = ...,
        lambdaConfig: LambdaDataSourceConfigTypeDef = ...,
        elasticsearchConfig: ElasticsearchDataSourceConfigTypeDef = ...,
        openSearchServiceConfig: OpenSearchServiceDataSourceConfigTypeDef = ...,
        httpConfig: HttpDataSourceConfigTypeDef = ...,
        relationalDatabaseConfig: RelationalDatabaseDataSourceConfigTypeDef = ...
    ) -> UpdateDataSourceResponseTypeDef:
        """
        Updates a `DataSource` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#update_data_source)
        """

    def update_domain_name(
        self, *, domainName: str, description: str = ...
    ) -> UpdateDomainNameResponseTypeDef:
        """
        Updates a custom `DomainName` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_domain_name)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#update_domain_name)
        """

    def update_function(
        self,
        *,
        apiId: str,
        name: str,
        functionId: str,
        dataSourceName: str,
        functionVersion: str,
        description: str = ...,
        requestMappingTemplate: str = ...,
        responseMappingTemplate: str = ...,
        syncConfig: SyncConfigTypeDef = ...,
        maxBatchSize: int = ...
    ) -> UpdateFunctionResponseTypeDef:
        """
        Updates a `Function` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_function)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#update_function)
        """

    def update_graphql_api(
        self,
        *,
        apiId: str,
        name: str,
        logConfig: LogConfigTypeDef = ...,
        authenticationType: AuthenticationTypeType = ...,
        userPoolConfig: UserPoolConfigTypeDef = ...,
        openIDConnectConfig: OpenIDConnectConfigTypeDef = ...,
        additionalAuthenticationProviders: Sequence[AdditionalAuthenticationProviderTypeDef] = ...,
        xrayEnabled: bool = ...,
        lambdaAuthorizerConfig: LambdaAuthorizerConfigTypeDef = ...
    ) -> UpdateGraphqlApiResponseTypeDef:
        """
        Updates a `GraphqlApi` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_graphql_api)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#update_graphql_api)
        """

    def update_resolver(
        self,
        *,
        apiId: str,
        typeName: str,
        fieldName: str,
        dataSourceName: str = ...,
        requestMappingTemplate: str = ...,
        responseMappingTemplate: str = ...,
        kind: ResolverKindType = ...,
        pipelineConfig: PipelineConfigTypeDef = ...,
        syncConfig: SyncConfigTypeDef = ...,
        cachingConfig: CachingConfigTypeDef = ...,
        maxBatchSize: int = ...
    ) -> UpdateResolverResponseTypeDef:
        """
        Updates a `Resolver` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_resolver)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#update_resolver)
        """

    def update_type(
        self, *, apiId: str, typeName: str, format: TypeDefinitionFormatType, definition: str = ...
    ) -> UpdateTypeResponseTypeDef:
        """
        Updates a `Type` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#update_type)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_api_keys"]) -> ListApiKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_sources"]
    ) -> ListDataSourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_functions"]) -> ListFunctionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_graphql_apis"]
    ) -> ListGraphqlApisPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_resolvers"]) -> ListResolversPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolvers_by_function"]
    ) -> ListResolversByFunctionPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_types"]) -> ListTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/client/#get_paginator)
        """
