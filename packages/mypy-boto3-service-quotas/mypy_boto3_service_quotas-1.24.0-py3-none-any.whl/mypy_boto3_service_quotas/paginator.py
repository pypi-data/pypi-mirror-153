"""
Type annotations for service-quotas service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_service_quotas.client import ServiceQuotasClient
    from mypy_boto3_service_quotas.paginator import (
        ListAWSDefaultServiceQuotasPaginator,
        ListRequestedServiceQuotaChangeHistoryPaginator,
        ListRequestedServiceQuotaChangeHistoryByQuotaPaginator,
        ListServiceQuotaIncreaseRequestsInTemplatePaginator,
        ListServiceQuotasPaginator,
        ListServicesPaginator,
    )

    session = Session()
    client: ServiceQuotasClient = session.client("service-quotas")

    list_aws_default_service_quotas_paginator: ListAWSDefaultServiceQuotasPaginator = client.get_paginator("list_aws_default_service_quotas")
    list_requested_service_quota_change_history_paginator: ListRequestedServiceQuotaChangeHistoryPaginator = client.get_paginator("list_requested_service_quota_change_history")
    list_requested_service_quota_change_history_by_quota_paginator: ListRequestedServiceQuotaChangeHistoryByQuotaPaginator = client.get_paginator("list_requested_service_quota_change_history_by_quota")
    list_service_quota_increase_requests_in_template_paginator: ListServiceQuotaIncreaseRequestsInTemplatePaginator = client.get_paginator("list_service_quota_increase_requests_in_template")
    list_service_quotas_paginator: ListServiceQuotasPaginator = client.get_paginator("list_service_quotas")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import RequestStatusType
from .type_defs import (
    ListAWSDefaultServiceQuotasResponseTypeDef,
    ListRequestedServiceQuotaChangeHistoryByQuotaResponseTypeDef,
    ListRequestedServiceQuotaChangeHistoryResponseTypeDef,
    ListServiceQuotaIncreaseRequestsInTemplateResponseTypeDef,
    ListServiceQuotasResponseTypeDef,
    ListServicesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListAWSDefaultServiceQuotasPaginator",
    "ListRequestedServiceQuotaChangeHistoryPaginator",
    "ListRequestedServiceQuotaChangeHistoryByQuotaPaginator",
    "ListServiceQuotaIncreaseRequestsInTemplatePaginator",
    "ListServiceQuotasPaginator",
    "ListServicesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAWSDefaultServiceQuotasPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Paginator.ListAWSDefaultServiceQuotas)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listawsdefaultservicequotaspaginator)
    """

    def paginate(
        self, *, ServiceCode: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAWSDefaultServiceQuotasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Paginator.ListAWSDefaultServiceQuotas.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listawsdefaultservicequotaspaginator)
        """


class ListRequestedServiceQuotaChangeHistoryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Paginator.ListRequestedServiceQuotaChangeHistory)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listrequestedservicequotachangehistorypaginator)
    """

    def paginate(
        self,
        *,
        ServiceCode: str = ...,
        Status: RequestStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRequestedServiceQuotaChangeHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Paginator.ListRequestedServiceQuotaChangeHistory.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listrequestedservicequotachangehistorypaginator)
        """


class ListRequestedServiceQuotaChangeHistoryByQuotaPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Paginator.ListRequestedServiceQuotaChangeHistoryByQuota)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listrequestedservicequotachangehistorybyquotapaginator)
    """

    def paginate(
        self,
        *,
        ServiceCode: str,
        QuotaCode: str,
        Status: RequestStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRequestedServiceQuotaChangeHistoryByQuotaResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Paginator.ListRequestedServiceQuotaChangeHistoryByQuota.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listrequestedservicequotachangehistorybyquotapaginator)
        """


class ListServiceQuotaIncreaseRequestsInTemplatePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Paginator.ListServiceQuotaIncreaseRequestsInTemplate)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listservicequotaincreaserequestsintemplatepaginator)
    """

    def paginate(
        self,
        *,
        ServiceCode: str = ...,
        AwsRegion: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServiceQuotaIncreaseRequestsInTemplateResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Paginator.ListServiceQuotaIncreaseRequestsInTemplate.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listservicequotaincreaserequestsintemplatepaginator)
        """


class ListServiceQuotasPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Paginator.ListServiceQuotas)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listservicequotaspaginator)
    """

    def paginate(
        self, *, ServiceCode: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServiceQuotasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Paginator.ListServiceQuotas.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listservicequotaspaginator)
        """


class ListServicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Paginator.ListServices)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listservicespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas.Paginator.ListServices.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listservicespaginator)
        """
