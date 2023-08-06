"""
Type annotations for service-quotas service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_service_quotas.client import ServiceQuotasClient

    session = Session()
    client: ServiceQuotasClient = session.client("service-quotas")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import RequestStatusType
from .paginator import (
    ListAWSDefaultServiceQuotasPaginator,
    ListRequestedServiceQuotaChangeHistoryByQuotaPaginator,
    ListRequestedServiceQuotaChangeHistoryPaginator,
    ListServiceQuotaIncreaseRequestsInTemplatePaginator,
    ListServiceQuotasPaginator,
    ListServicesPaginator,
)
from .type_defs import (
    GetAssociationForServiceQuotaTemplateResponseTypeDef,
    GetAWSDefaultServiceQuotaResponseTypeDef,
    GetRequestedServiceQuotaChangeResponseTypeDef,
    GetServiceQuotaIncreaseRequestFromTemplateResponseTypeDef,
    GetServiceQuotaResponseTypeDef,
    ListAWSDefaultServiceQuotasResponseTypeDef,
    ListRequestedServiceQuotaChangeHistoryByQuotaResponseTypeDef,
    ListRequestedServiceQuotaChangeHistoryResponseTypeDef,
    ListServiceQuotaIncreaseRequestsInTemplateResponseTypeDef,
    ListServiceQuotasResponseTypeDef,
    ListServicesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutServiceQuotaIncreaseRequestIntoTemplateResponseTypeDef,
    RequestServiceQuotaIncreaseResponseTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ServiceQuotasClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AWSServiceAccessNotEnabledException: Type[BotocoreClientError]
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DependencyAccessDeniedException: Type[BotocoreClientError]
    IllegalArgumentException: Type[BotocoreClientError]
    InvalidPaginationTokenException: Type[BotocoreClientError]
    InvalidResourceStateException: Type[BotocoreClientError]
    NoAvailableOrganizationException: Type[BotocoreClientError]
    NoSuchResourceException: Type[BotocoreClientError]
    OrganizationNotInAllFeaturesModeException: Type[BotocoreClientError]
    QuotaExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ServiceException: Type[BotocoreClientError]
    ServiceQuotaTemplateNotInUseException: Type[BotocoreClientError]
    TagPolicyViolationException: Type[BotocoreClientError]
    TemplatesNotAvailableInRegionException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]


class ServiceQuotasClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ServiceQuotasClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#exceptions)
        """

    def associate_service_quota_template(self) -> Dict[str, Any]:
        """
        Associates your quota request template with your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.associate_service_quota_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#associate_service_quota_template)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#can_paginate)
        """

    def delete_service_quota_increase_request_from_template(
        self, *, ServiceCode: str, QuotaCode: str, AwsRegion: str
    ) -> Dict[str, Any]:
        """
        Deletes the quota increase request for the specified quota from your quota
        request template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.delete_service_quota_increase_request_from_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#delete_service_quota_increase_request_from_template)
        """

    def disassociate_service_quota_template(self) -> Dict[str, Any]:
        """
        Disables your quota request template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.disassociate_service_quota_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#disassociate_service_quota_template)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#generate_presigned_url)
        """

    def get_association_for_service_quota_template(
        self,
    ) -> GetAssociationForServiceQuotaTemplateResponseTypeDef:
        """
        Retrieves the status of the association for the quota request template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.get_association_for_service_quota_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#get_association_for_service_quota_template)
        """

    def get_aws_default_service_quota(
        self, *, ServiceCode: str, QuotaCode: str
    ) -> GetAWSDefaultServiceQuotaResponseTypeDef:
        """
        Retrieves the default value for the specified quota.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.get_aws_default_service_quota)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#get_aws_default_service_quota)
        """

    def get_requested_service_quota_change(
        self, *, RequestId: str
    ) -> GetRequestedServiceQuotaChangeResponseTypeDef:
        """
        Retrieves information about the specified quota increase request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.get_requested_service_quota_change)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#get_requested_service_quota_change)
        """

    def get_service_quota(
        self, *, ServiceCode: str, QuotaCode: str
    ) -> GetServiceQuotaResponseTypeDef:
        """
        Retrieves the applied quota value for the specified quota.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.get_service_quota)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#get_service_quota)
        """

    def get_service_quota_increase_request_from_template(
        self, *, ServiceCode: str, QuotaCode: str, AwsRegion: str
    ) -> GetServiceQuotaIncreaseRequestFromTemplateResponseTypeDef:
        """
        Retrieves information about the specified quota increase request in your quota
        request template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.get_service_quota_increase_request_from_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#get_service_quota_increase_request_from_template)
        """

    def list_aws_default_service_quotas(
        self, *, ServiceCode: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListAWSDefaultServiceQuotasResponseTypeDef:
        """
        Lists the default values for the quotas for the specified AWS service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.list_aws_default_service_quotas)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#list_aws_default_service_quotas)
        """

    def list_requested_service_quota_change_history(
        self,
        *,
        ServiceCode: str = ...,
        Status: RequestStatusType = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListRequestedServiceQuotaChangeHistoryResponseTypeDef:
        """
        Retrieves the quota increase requests for the specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.list_requested_service_quota_change_history)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#list_requested_service_quota_change_history)
        """

    def list_requested_service_quota_change_history_by_quota(
        self,
        *,
        ServiceCode: str,
        QuotaCode: str,
        Status: RequestStatusType = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListRequestedServiceQuotaChangeHistoryByQuotaResponseTypeDef:
        """
        Retrieves the quota increase requests for the specified quota.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.list_requested_service_quota_change_history_by_quota)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#list_requested_service_quota_change_history_by_quota)
        """

    def list_service_quota_increase_requests_in_template(
        self,
        *,
        ServiceCode: str = ...,
        AwsRegion: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListServiceQuotaIncreaseRequestsInTemplateResponseTypeDef:
        """
        Lists the quota increase requests in the specified quota request template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.list_service_quota_increase_requests_in_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#list_service_quota_increase_requests_in_template)
        """

    def list_service_quotas(
        self, *, ServiceCode: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListServiceQuotasResponseTypeDef:
        """
        Lists the applied quota values for the specified AWS service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.list_service_quotas)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#list_service_quotas)
        """

    def list_services(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListServicesResponseTypeDef:
        """
        Lists the names and codes for the services integrated with Service Quotas.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.list_services)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#list_services)
        """

    def list_tags_for_resource(self, *, ResourceARN: str) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of the tags assigned to the specified applied quota.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#list_tags_for_resource)
        """

    def put_service_quota_increase_request_into_template(
        self, *, QuotaCode: str, ServiceCode: str, AwsRegion: str, DesiredValue: float
    ) -> PutServiceQuotaIncreaseRequestIntoTemplateResponseTypeDef:
        """
        Adds a quota increase request to your quota request template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.put_service_quota_increase_request_into_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#put_service_quota_increase_request_into_template)
        """

    def request_service_quota_increase(
        self, *, ServiceCode: str, QuotaCode: str, DesiredValue: float
    ) -> RequestServiceQuotaIncreaseResponseTypeDef:
        """
        Submits a quota increase request for the specified quota.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.request_service_quota_increase)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#request_service_quota_increase)
        """

    def tag_resource(self, *, ResourceARN: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to the specified applied quota.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from the specified applied quota.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_aws_default_service_quotas"]
    ) -> ListAWSDefaultServiceQuotasPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_requested_service_quota_change_history"]
    ) -> ListRequestedServiceQuotaChangeHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_requested_service_quota_change_history_by_quota"]
    ) -> ListRequestedServiceQuotaChangeHistoryByQuotaPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_quota_increase_requests_in_template"]
    ) -> ListServiceQuotaIncreaseRequestsInTemplatePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_quotas"]
    ) -> ListServiceQuotasPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_services"]) -> ListServicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/client/#get_paginator)
        """
