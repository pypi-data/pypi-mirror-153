"""
Type annotations for apigatewayv2 service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_apigatewayv2.client import ApiGatewayV2Client

    session = Session()
    client: ApiGatewayV2Client = session.client("apigatewayv2")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    AuthorizationTypeType,
    AuthorizerTypeType,
    ConnectionTypeType,
    ContentHandlingStrategyType,
    IntegrationTypeType,
    JSONYAMLType,
    PassthroughBehaviorType,
    ProtocolTypeType,
)
from .paginator import (
    GetApisPaginator,
    GetAuthorizersPaginator,
    GetDeploymentsPaginator,
    GetDomainNamesPaginator,
    GetIntegrationResponsesPaginator,
    GetIntegrationsPaginator,
    GetModelsPaginator,
    GetRouteResponsesPaginator,
    GetRoutesPaginator,
    GetStagesPaginator,
)
from .type_defs import (
    AccessLogSettingsTypeDef,
    CorsTypeDef,
    CreateApiMappingResponseTypeDef,
    CreateApiResponseTypeDef,
    CreateAuthorizerResponseTypeDef,
    CreateDeploymentResponseTypeDef,
    CreateDomainNameResponseTypeDef,
    CreateIntegrationResponseResponseTypeDef,
    CreateIntegrationResultTypeDef,
    CreateModelResponseTypeDef,
    CreateRouteResponseResponseTypeDef,
    CreateRouteResultTypeDef,
    CreateStageResponseTypeDef,
    CreateVpcLinkResponseTypeDef,
    DomainNameConfigurationTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportApiResponseTypeDef,
    GetApiMappingResponseTypeDef,
    GetApiMappingsResponseTypeDef,
    GetApiResponseTypeDef,
    GetApisResponseTypeDef,
    GetAuthorizerResponseTypeDef,
    GetAuthorizersResponseTypeDef,
    GetDeploymentResponseTypeDef,
    GetDeploymentsResponseTypeDef,
    GetDomainNameResponseTypeDef,
    GetDomainNamesResponseTypeDef,
    GetIntegrationResponseResponseTypeDef,
    GetIntegrationResponsesResponseTypeDef,
    GetIntegrationResultTypeDef,
    GetIntegrationsResponseTypeDef,
    GetModelResponseTypeDef,
    GetModelsResponseTypeDef,
    GetModelTemplateResponseTypeDef,
    GetRouteResponseResponseTypeDef,
    GetRouteResponsesResponseTypeDef,
    GetRouteResultTypeDef,
    GetRoutesResponseTypeDef,
    GetStageResponseTypeDef,
    GetStagesResponseTypeDef,
    GetTagsResponseTypeDef,
    GetVpcLinkResponseTypeDef,
    GetVpcLinksResponseTypeDef,
    ImportApiResponseTypeDef,
    JWTConfigurationTypeDef,
    MutualTlsAuthenticationInputTypeDef,
    ParameterConstraintsTypeDef,
    ReimportApiResponseTypeDef,
    RouteSettingsTypeDef,
    TlsConfigInputTypeDef,
    UpdateApiMappingResponseTypeDef,
    UpdateApiResponseTypeDef,
    UpdateAuthorizerResponseTypeDef,
    UpdateDeploymentResponseTypeDef,
    UpdateDomainNameResponseTypeDef,
    UpdateIntegrationResponseResponseTypeDef,
    UpdateIntegrationResultTypeDef,
    UpdateModelResponseTypeDef,
    UpdateRouteResponseResponseTypeDef,
    UpdateRouteResultTypeDef,
    UpdateStageResponseTypeDef,
    UpdateVpcLinkResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ApiGatewayV2Client",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class ApiGatewayV2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ApiGatewayV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#can_paginate)
        """

    def create_api(
        self,
        *,
        Name: str,
        ProtocolType: ProtocolTypeType,
        ApiKeySelectionExpression: str = ...,
        CorsConfiguration: CorsTypeDef = ...,
        CredentialsArn: str = ...,
        Description: str = ...,
        DisableSchemaValidation: bool = ...,
        DisableExecuteApiEndpoint: bool = ...,
        RouteKey: str = ...,
        RouteSelectionExpression: str = ...,
        Tags: Mapping[str, str] = ...,
        Target: str = ...,
        Version: str = ...
    ) -> CreateApiResponseTypeDef:
        """
        Creates an Api resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_api)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#create_api)
        """

    def create_api_mapping(
        self, *, ApiId: str, DomainName: str, Stage: str, ApiMappingKey: str = ...
    ) -> CreateApiMappingResponseTypeDef:
        """
        Creates an API mapping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_api_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#create_api_mapping)
        """

    def create_authorizer(
        self,
        *,
        ApiId: str,
        AuthorizerType: AuthorizerTypeType,
        IdentitySource: Sequence[str],
        Name: str,
        AuthorizerCredentialsArn: str = ...,
        AuthorizerPayloadFormatVersion: str = ...,
        AuthorizerResultTtlInSeconds: int = ...,
        AuthorizerUri: str = ...,
        EnableSimpleResponses: bool = ...,
        IdentityValidationExpression: str = ...,
        JwtConfiguration: JWTConfigurationTypeDef = ...
    ) -> CreateAuthorizerResponseTypeDef:
        """
        Creates an Authorizer for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_authorizer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#create_authorizer)
        """

    def create_deployment(
        self, *, ApiId: str, Description: str = ..., StageName: str = ...
    ) -> CreateDeploymentResponseTypeDef:
        """
        Creates a Deployment for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#create_deployment)
        """

    def create_domain_name(
        self,
        *,
        DomainName: str,
        DomainNameConfigurations: Sequence[DomainNameConfigurationTypeDef] = ...,
        MutualTlsAuthentication: MutualTlsAuthenticationInputTypeDef = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateDomainNameResponseTypeDef:
        """
        Creates a domain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_domain_name)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#create_domain_name)
        """

    def create_integration(
        self,
        *,
        ApiId: str,
        IntegrationType: IntegrationTypeType,
        ConnectionId: str = ...,
        ConnectionType: ConnectionTypeType = ...,
        ContentHandlingStrategy: ContentHandlingStrategyType = ...,
        CredentialsArn: str = ...,
        Description: str = ...,
        IntegrationMethod: str = ...,
        IntegrationSubtype: str = ...,
        IntegrationUri: str = ...,
        PassthroughBehavior: PassthroughBehaviorType = ...,
        PayloadFormatVersion: str = ...,
        RequestParameters: Mapping[str, str] = ...,
        RequestTemplates: Mapping[str, str] = ...,
        ResponseParameters: Mapping[str, Mapping[str, str]] = ...,
        TemplateSelectionExpression: str = ...,
        TimeoutInMillis: int = ...,
        TlsConfig: TlsConfigInputTypeDef = ...
    ) -> CreateIntegrationResultTypeDef:
        """
        Creates an Integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_integration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#create_integration)
        """

    def create_integration_response(
        self,
        *,
        ApiId: str,
        IntegrationId: str,
        IntegrationResponseKey: str,
        ContentHandlingStrategy: ContentHandlingStrategyType = ...,
        ResponseParameters: Mapping[str, str] = ...,
        ResponseTemplates: Mapping[str, str] = ...,
        TemplateSelectionExpression: str = ...
    ) -> CreateIntegrationResponseResponseTypeDef:
        """
        Creates an IntegrationResponses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_integration_response)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#create_integration_response)
        """

    def create_model(
        self, *, ApiId: str, Name: str, Schema: str, ContentType: str = ..., Description: str = ...
    ) -> CreateModelResponseTypeDef:
        """
        Creates a Model for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_model)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#create_model)
        """

    def create_route(
        self,
        *,
        ApiId: str,
        RouteKey: str,
        ApiKeyRequired: bool = ...,
        AuthorizationScopes: Sequence[str] = ...,
        AuthorizationType: AuthorizationTypeType = ...,
        AuthorizerId: str = ...,
        ModelSelectionExpression: str = ...,
        OperationName: str = ...,
        RequestModels: Mapping[str, str] = ...,
        RequestParameters: Mapping[str, ParameterConstraintsTypeDef] = ...,
        RouteResponseSelectionExpression: str = ...,
        Target: str = ...
    ) -> CreateRouteResultTypeDef:
        """
        Creates a Route for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#create_route)
        """

    def create_route_response(
        self,
        *,
        ApiId: str,
        RouteId: str,
        RouteResponseKey: str,
        ModelSelectionExpression: str = ...,
        ResponseModels: Mapping[str, str] = ...,
        ResponseParameters: Mapping[str, ParameterConstraintsTypeDef] = ...
    ) -> CreateRouteResponseResponseTypeDef:
        """
        Creates a RouteResponse for a Route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_route_response)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#create_route_response)
        """

    def create_stage(
        self,
        *,
        ApiId: str,
        StageName: str,
        AccessLogSettings: AccessLogSettingsTypeDef = ...,
        AutoDeploy: bool = ...,
        ClientCertificateId: str = ...,
        DefaultRouteSettings: RouteSettingsTypeDef = ...,
        DeploymentId: str = ...,
        Description: str = ...,
        RouteSettings: Mapping[str, RouteSettingsTypeDef] = ...,
        StageVariables: Mapping[str, str] = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateStageResponseTypeDef:
        """
        Creates a Stage for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_stage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#create_stage)
        """

    def create_vpc_link(
        self,
        *,
        Name: str,
        SubnetIds: Sequence[str],
        SecurityGroupIds: Sequence[str] = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateVpcLinkResponseTypeDef:
        """
        Creates a VPC link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_vpc_link)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#create_vpc_link)
        """

    def delete_access_log_settings(
        self, *, ApiId: str, StageName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the AccessLogSettings for a Stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_access_log_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_access_log_settings)
        """

    def delete_api(self, *, ApiId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Api resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_api)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_api)
        """

    def delete_api_mapping(
        self, *, ApiMappingId: str, DomainName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an API mapping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_api_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_api_mapping)
        """

    def delete_authorizer(self, *, ApiId: str, AuthorizerId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_authorizer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_authorizer)
        """

    def delete_cors_configuration(self, *, ApiId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a CORS configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_cors_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_cors_configuration)
        """

    def delete_deployment(self, *, ApiId: str, DeploymentId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_deployment)
        """

    def delete_domain_name(self, *, DomainName: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a domain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_domain_name)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_domain_name)
        """

    def delete_integration(self, *, ApiId: str, IntegrationId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_integration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_integration)
        """

    def delete_integration_response(
        self, *, ApiId: str, IntegrationId: str, IntegrationResponseId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an IntegrationResponses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_integration_response)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_integration_response)
        """

    def delete_model(self, *, ApiId: str, ModelId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_model)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_model)
        """

    def delete_route(self, *, ApiId: str, RouteId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_route)
        """

    def delete_route_request_parameter(
        self, *, ApiId: str, RequestParameterKey: str, RouteId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a route request parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_route_request_parameter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_route_request_parameter)
        """

    def delete_route_response(
        self, *, ApiId: str, RouteId: str, RouteResponseId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a RouteResponse.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_route_response)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_route_response)
        """

    def delete_route_settings(
        self, *, ApiId: str, RouteKey: str, StageName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the RouteSettings for a stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_route_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_route_settings)
        """

    def delete_stage(self, *, ApiId: str, StageName: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_stage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_stage)
        """

    def delete_vpc_link(self, *, VpcLinkId: str) -> Dict[str, Any]:
        """
        Deletes a VPC link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_vpc_link)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#delete_vpc_link)
        """

    def export_api(
        self,
        *,
        ApiId: str,
        OutputType: JSONYAMLType,
        Specification: Literal["OAS30"],
        ExportVersion: str = ...,
        IncludeExtensions: bool = ...,
        StageName: str = ...
    ) -> ExportApiResponseTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/apigatewayv2-2018-11-29/ExportApi).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.export_api)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#export_api)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#generate_presigned_url)
        """

    def get_api(self, *, ApiId: str) -> GetApiResponseTypeDef:
        """
        Gets an Api resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_api)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_api)
        """

    def get_api_mapping(
        self, *, ApiMappingId: str, DomainName: str
    ) -> GetApiMappingResponseTypeDef:
        """
        Gets an API mapping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_api_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_api_mapping)
        """

    def get_api_mappings(
        self, *, DomainName: str, MaxResults: str = ..., NextToken: str = ...
    ) -> GetApiMappingsResponseTypeDef:
        """
        Gets API mappings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_api_mappings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_api_mappings)
        """

    def get_apis(self, *, MaxResults: str = ..., NextToken: str = ...) -> GetApisResponseTypeDef:
        """
        Gets a collection of Api resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_apis)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_apis)
        """

    def get_authorizer(self, *, ApiId: str, AuthorizerId: str) -> GetAuthorizerResponseTypeDef:
        """
        Gets an Authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_authorizer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_authorizer)
        """

    def get_authorizers(
        self, *, ApiId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> GetAuthorizersResponseTypeDef:
        """
        Gets the Authorizers for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_authorizers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_authorizers)
        """

    def get_deployment(self, *, ApiId: str, DeploymentId: str) -> GetDeploymentResponseTypeDef:
        """
        Gets a Deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_deployment)
        """

    def get_deployments(
        self, *, ApiId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> GetDeploymentsResponseTypeDef:
        """
        Gets the Deployments for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_deployments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_deployments)
        """

    def get_domain_name(self, *, DomainName: str) -> GetDomainNameResponseTypeDef:
        """
        Gets a domain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_domain_name)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_domain_name)
        """

    def get_domain_names(
        self, *, MaxResults: str = ..., NextToken: str = ...
    ) -> GetDomainNamesResponseTypeDef:
        """
        Gets the domain names for an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_domain_names)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_domain_names)
        """

    def get_integration(self, *, ApiId: str, IntegrationId: str) -> GetIntegrationResultTypeDef:
        """
        Gets an Integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_integration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_integration)
        """

    def get_integration_response(
        self, *, ApiId: str, IntegrationId: str, IntegrationResponseId: str
    ) -> GetIntegrationResponseResponseTypeDef:
        """
        Gets an IntegrationResponses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_integration_response)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_integration_response)
        """

    def get_integration_responses(
        self, *, ApiId: str, IntegrationId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> GetIntegrationResponsesResponseTypeDef:
        """
        Gets the IntegrationResponses for an Integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_integration_responses)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_integration_responses)
        """

    def get_integrations(
        self, *, ApiId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> GetIntegrationsResponseTypeDef:
        """
        Gets the Integrations for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_integrations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_integrations)
        """

    def get_model(self, *, ApiId: str, ModelId: str) -> GetModelResponseTypeDef:
        """
        Gets a Model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_model)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_model)
        """

    def get_model_template(self, *, ApiId: str, ModelId: str) -> GetModelTemplateResponseTypeDef:
        """
        Gets a model template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_model_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_model_template)
        """

    def get_models(
        self, *, ApiId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> GetModelsResponseTypeDef:
        """
        Gets the Models for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_models)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_models)
        """

    def get_route(self, *, ApiId: str, RouteId: str) -> GetRouteResultTypeDef:
        """
        Gets a Route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_route)
        """

    def get_route_response(
        self, *, ApiId: str, RouteId: str, RouteResponseId: str
    ) -> GetRouteResponseResponseTypeDef:
        """
        Gets a RouteResponse.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_route_response)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_route_response)
        """

    def get_route_responses(
        self, *, ApiId: str, RouteId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> GetRouteResponsesResponseTypeDef:
        """
        Gets the RouteResponses for a Route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_route_responses)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_route_responses)
        """

    def get_routes(
        self, *, ApiId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> GetRoutesResponseTypeDef:
        """
        Gets the Routes for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_routes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_routes)
        """

    def get_stage(self, *, ApiId: str, StageName: str) -> GetStageResponseTypeDef:
        """
        Gets a Stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_stage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_stage)
        """

    def get_stages(
        self, *, ApiId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> GetStagesResponseTypeDef:
        """
        Gets the Stages for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_stages)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_stages)
        """

    def get_tags(self, *, ResourceArn: str) -> GetTagsResponseTypeDef:
        """
        Gets a collection of Tag resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_tags)
        """

    def get_vpc_link(self, *, VpcLinkId: str) -> GetVpcLinkResponseTypeDef:
        """
        Gets a VPC link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_vpc_link)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_vpc_link)
        """

    def get_vpc_links(
        self, *, MaxResults: str = ..., NextToken: str = ...
    ) -> GetVpcLinksResponseTypeDef:
        """
        Gets a collection of VPC links.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_vpc_links)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_vpc_links)
        """

    def import_api(
        self, *, Body: str, Basepath: str = ..., FailOnWarnings: bool = ...
    ) -> ImportApiResponseTypeDef:
        """
        Imports an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.import_api)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#import_api)
        """

    def reimport_api(
        self, *, ApiId: str, Body: str, Basepath: str = ..., FailOnWarnings: bool = ...
    ) -> ReimportApiResponseTypeDef:
        """
        Puts an Api resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.reimport_api)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#reimport_api)
        """

    def reset_authorizers_cache(
        self, *, ApiId: str, StageName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Resets all authorizer cache entries on a stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.reset_authorizers_cache)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#reset_authorizers_cache)
        """

    def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str] = ...) -> Dict[str, Any]:
        """
        Creates a new Tag resource to represent a tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#tag_resource)
        """

    def untag_resource(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#untag_resource)
        """

    def update_api(
        self,
        *,
        ApiId: str,
        ApiKeySelectionExpression: str = ...,
        CorsConfiguration: CorsTypeDef = ...,
        CredentialsArn: str = ...,
        Description: str = ...,
        DisableSchemaValidation: bool = ...,
        DisableExecuteApiEndpoint: bool = ...,
        Name: str = ...,
        RouteKey: str = ...,
        RouteSelectionExpression: str = ...,
        Target: str = ...,
        Version: str = ...
    ) -> UpdateApiResponseTypeDef:
        """
        Updates an Api resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_api)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#update_api)
        """

    def update_api_mapping(
        self,
        *,
        ApiId: str,
        ApiMappingId: str,
        DomainName: str,
        ApiMappingKey: str = ...,
        Stage: str = ...
    ) -> UpdateApiMappingResponseTypeDef:
        """
        The API mapping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_api_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#update_api_mapping)
        """

    def update_authorizer(
        self,
        *,
        ApiId: str,
        AuthorizerId: str,
        AuthorizerCredentialsArn: str = ...,
        AuthorizerPayloadFormatVersion: str = ...,
        AuthorizerResultTtlInSeconds: int = ...,
        AuthorizerType: AuthorizerTypeType = ...,
        AuthorizerUri: str = ...,
        EnableSimpleResponses: bool = ...,
        IdentitySource: Sequence[str] = ...,
        IdentityValidationExpression: str = ...,
        JwtConfiguration: JWTConfigurationTypeDef = ...,
        Name: str = ...
    ) -> UpdateAuthorizerResponseTypeDef:
        """
        Updates an Authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_authorizer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#update_authorizer)
        """

    def update_deployment(
        self, *, ApiId: str, DeploymentId: str, Description: str = ...
    ) -> UpdateDeploymentResponseTypeDef:
        """
        Updates a Deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#update_deployment)
        """

    def update_domain_name(
        self,
        *,
        DomainName: str,
        DomainNameConfigurations: Sequence[DomainNameConfigurationTypeDef] = ...,
        MutualTlsAuthentication: MutualTlsAuthenticationInputTypeDef = ...
    ) -> UpdateDomainNameResponseTypeDef:
        """
        Updates a domain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_domain_name)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#update_domain_name)
        """

    def update_integration(
        self,
        *,
        ApiId: str,
        IntegrationId: str,
        ConnectionId: str = ...,
        ConnectionType: ConnectionTypeType = ...,
        ContentHandlingStrategy: ContentHandlingStrategyType = ...,
        CredentialsArn: str = ...,
        Description: str = ...,
        IntegrationMethod: str = ...,
        IntegrationSubtype: str = ...,
        IntegrationType: IntegrationTypeType = ...,
        IntegrationUri: str = ...,
        PassthroughBehavior: PassthroughBehaviorType = ...,
        PayloadFormatVersion: str = ...,
        RequestParameters: Mapping[str, str] = ...,
        RequestTemplates: Mapping[str, str] = ...,
        ResponseParameters: Mapping[str, Mapping[str, str]] = ...,
        TemplateSelectionExpression: str = ...,
        TimeoutInMillis: int = ...,
        TlsConfig: TlsConfigInputTypeDef = ...
    ) -> UpdateIntegrationResultTypeDef:
        """
        Updates an Integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_integration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#update_integration)
        """

    def update_integration_response(
        self,
        *,
        ApiId: str,
        IntegrationId: str,
        IntegrationResponseId: str,
        ContentHandlingStrategy: ContentHandlingStrategyType = ...,
        IntegrationResponseKey: str = ...,
        ResponseParameters: Mapping[str, str] = ...,
        ResponseTemplates: Mapping[str, str] = ...,
        TemplateSelectionExpression: str = ...
    ) -> UpdateIntegrationResponseResponseTypeDef:
        """
        Updates an IntegrationResponses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_integration_response)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#update_integration_response)
        """

    def update_model(
        self,
        *,
        ApiId: str,
        ModelId: str,
        ContentType: str = ...,
        Description: str = ...,
        Name: str = ...,
        Schema: str = ...
    ) -> UpdateModelResponseTypeDef:
        """
        Updates a Model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_model)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#update_model)
        """

    def update_route(
        self,
        *,
        ApiId: str,
        RouteId: str,
        ApiKeyRequired: bool = ...,
        AuthorizationScopes: Sequence[str] = ...,
        AuthorizationType: AuthorizationTypeType = ...,
        AuthorizerId: str = ...,
        ModelSelectionExpression: str = ...,
        OperationName: str = ...,
        RequestModels: Mapping[str, str] = ...,
        RequestParameters: Mapping[str, ParameterConstraintsTypeDef] = ...,
        RouteKey: str = ...,
        RouteResponseSelectionExpression: str = ...,
        Target: str = ...
    ) -> UpdateRouteResultTypeDef:
        """
        Updates a Route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#update_route)
        """

    def update_route_response(
        self,
        *,
        ApiId: str,
        RouteId: str,
        RouteResponseId: str,
        ModelSelectionExpression: str = ...,
        ResponseModels: Mapping[str, str] = ...,
        ResponseParameters: Mapping[str, ParameterConstraintsTypeDef] = ...,
        RouteResponseKey: str = ...
    ) -> UpdateRouteResponseResponseTypeDef:
        """
        Updates a RouteResponse.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_route_response)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#update_route_response)
        """

    def update_stage(
        self,
        *,
        ApiId: str,
        StageName: str,
        AccessLogSettings: AccessLogSettingsTypeDef = ...,
        AutoDeploy: bool = ...,
        ClientCertificateId: str = ...,
        DefaultRouteSettings: RouteSettingsTypeDef = ...,
        DeploymentId: str = ...,
        Description: str = ...,
        RouteSettings: Mapping[str, RouteSettingsTypeDef] = ...,
        StageVariables: Mapping[str, str] = ...
    ) -> UpdateStageResponseTypeDef:
        """
        Updates a Stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_stage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#update_stage)
        """

    def update_vpc_link(self, *, VpcLinkId: str, Name: str = ...) -> UpdateVpcLinkResponseTypeDef:
        """
        Updates a VPC link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_vpc_link)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#update_vpc_link)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_apis"]) -> GetApisPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_authorizers"]) -> GetAuthorizersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_deployments"]) -> GetDeploymentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_domain_names"]) -> GetDomainNamesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_integration_responses"]
    ) -> GetIntegrationResponsesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_integrations"]
    ) -> GetIntegrationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_models"]) -> GetModelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_route_responses"]
    ) -> GetRouteResponsesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_routes"]) -> GetRoutesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_stages"]) -> GetStagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/client/#get_paginator)
        """
