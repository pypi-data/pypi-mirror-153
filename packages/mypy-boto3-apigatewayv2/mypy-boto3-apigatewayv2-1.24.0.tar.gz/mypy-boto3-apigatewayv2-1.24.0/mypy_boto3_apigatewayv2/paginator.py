"""
Type annotations for apigatewayv2 service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_apigatewayv2.client import ApiGatewayV2Client
    from mypy_boto3_apigatewayv2.paginator import (
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

    session = Session()
    client: ApiGatewayV2Client = session.client("apigatewayv2")

    get_apis_paginator: GetApisPaginator = client.get_paginator("get_apis")
    get_authorizers_paginator: GetAuthorizersPaginator = client.get_paginator("get_authorizers")
    get_deployments_paginator: GetDeploymentsPaginator = client.get_paginator("get_deployments")
    get_domain_names_paginator: GetDomainNamesPaginator = client.get_paginator("get_domain_names")
    get_integration_responses_paginator: GetIntegrationResponsesPaginator = client.get_paginator("get_integration_responses")
    get_integrations_paginator: GetIntegrationsPaginator = client.get_paginator("get_integrations")
    get_models_paginator: GetModelsPaginator = client.get_paginator("get_models")
    get_route_responses_paginator: GetRouteResponsesPaginator = client.get_paginator("get_route_responses")
    get_routes_paginator: GetRoutesPaginator = client.get_paginator("get_routes")
    get_stages_paginator: GetStagesPaginator = client.get_paginator("get_stages")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    GetApisResponseTypeDef,
    GetAuthorizersResponseTypeDef,
    GetDeploymentsResponseTypeDef,
    GetDomainNamesResponseTypeDef,
    GetIntegrationResponsesResponseTypeDef,
    GetIntegrationsResponseTypeDef,
    GetModelsResponseTypeDef,
    GetRouteResponsesResponseTypeDef,
    GetRoutesResponseTypeDef,
    GetStagesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetApisPaginator",
    "GetAuthorizersPaginator",
    "GetDeploymentsPaginator",
    "GetDomainNamesPaginator",
    "GetIntegrationResponsesPaginator",
    "GetIntegrationsPaginator",
    "GetModelsPaginator",
    "GetRouteResponsesPaginator",
    "GetRoutesPaginator",
    "GetStagesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetApisPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetApis)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getapispaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetApisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetApis.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getapispaginator)
        """


class GetAuthorizersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetAuthorizers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getauthorizerspaginator)
    """

    def paginate(
        self, *, ApiId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetAuthorizersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetAuthorizers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getauthorizerspaginator)
        """


class GetDeploymentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetDeployments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getdeploymentspaginator)
    """

    def paginate(
        self, *, ApiId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetDeployments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getdeploymentspaginator)
        """


class GetDomainNamesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetDomainNames)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getdomainnamespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetDomainNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetDomainNames.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getdomainnamespaginator)
        """


class GetIntegrationResponsesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetIntegrationResponses)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getintegrationresponsespaginator)
    """

    def paginate(
        self, *, ApiId: str, IntegrationId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetIntegrationResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetIntegrationResponses.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getintegrationresponsespaginator)
        """


class GetIntegrationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetIntegrations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getintegrationspaginator)
    """

    def paginate(
        self, *, ApiId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetIntegrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetIntegrations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getintegrationspaginator)
        """


class GetModelsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetModels)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getmodelspaginator)
    """

    def paginate(
        self, *, ApiId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetModels.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getmodelspaginator)
        """


class GetRouteResponsesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetRouteResponses)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getrouteresponsespaginator)
    """

    def paginate(
        self, *, ApiId: str, RouteId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetRouteResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetRouteResponses.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getrouteresponsespaginator)
        """


class GetRoutesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetRoutes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getroutespaginator)
    """

    def paginate(
        self, *, ApiId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetRoutesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetRoutes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getroutespaginator)
        """


class GetStagesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetStages)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getstagespaginator)
    """

    def paginate(
        self, *, ApiId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetStagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetStages.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getstagespaginator)
        """
