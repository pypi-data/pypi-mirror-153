"""
Type annotations for service-quotas service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/type_defs/)

Usage::

    ```python
    from mypy_boto3_service_quotas.type_defs import DeleteServiceQuotaIncreaseRequestFromTemplateRequestRequestTypeDef

    data: DeleteServiceQuotaIncreaseRequestFromTemplateRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    ErrorCodeType,
    PeriodUnitType,
    RequestStatusType,
    ServiceQuotaTemplateAssociationStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "DeleteServiceQuotaIncreaseRequestFromTemplateRequestRequestTypeDef",
    "ErrorReasonTypeDef",
    "GetAWSDefaultServiceQuotaRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "GetRequestedServiceQuotaChangeRequestRequestTypeDef",
    "RequestedServiceQuotaChangeTypeDef",
    "GetServiceQuotaIncreaseRequestFromTemplateRequestRequestTypeDef",
    "ServiceQuotaIncreaseRequestInTemplateTypeDef",
    "GetServiceQuotaRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListAWSDefaultServiceQuotasRequestRequestTypeDef",
    "ListRequestedServiceQuotaChangeHistoryByQuotaRequestRequestTypeDef",
    "ListRequestedServiceQuotaChangeHistoryRequestRequestTypeDef",
    "ListServiceQuotaIncreaseRequestsInTemplateRequestRequestTypeDef",
    "ListServiceQuotasRequestRequestTypeDef",
    "ListServicesRequestRequestTypeDef",
    "ServiceInfoTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagTypeDef",
    "MetricInfoTypeDef",
    "PutServiceQuotaIncreaseRequestIntoTemplateRequestRequestTypeDef",
    "QuotaPeriodTypeDef",
    "RequestServiceQuotaIncreaseRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "GetAssociationForServiceQuotaTemplateResponseTypeDef",
    "GetRequestedServiceQuotaChangeResponseTypeDef",
    "ListRequestedServiceQuotaChangeHistoryByQuotaResponseTypeDef",
    "ListRequestedServiceQuotaChangeHistoryResponseTypeDef",
    "RequestServiceQuotaIncreaseResponseTypeDef",
    "GetServiceQuotaIncreaseRequestFromTemplateResponseTypeDef",
    "ListServiceQuotaIncreaseRequestsInTemplateResponseTypeDef",
    "PutServiceQuotaIncreaseRequestIntoTemplateResponseTypeDef",
    "ListAWSDefaultServiceQuotasRequestListAWSDefaultServiceQuotasPaginateTypeDef",
    "ListRequestedServiceQuotaChangeHistoryByQuotaRequestListRequestedServiceQuotaChangeHistoryByQuotaPaginateTypeDef",
    "ListRequestedServiceQuotaChangeHistoryRequestListRequestedServiceQuotaChangeHistoryPaginateTypeDef",
    "ListServiceQuotaIncreaseRequestsInTemplateRequestListServiceQuotaIncreaseRequestsInTemplatePaginateTypeDef",
    "ListServiceQuotasRequestListServiceQuotasPaginateTypeDef",
    "ListServicesRequestListServicesPaginateTypeDef",
    "ListServicesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ServiceQuotaTypeDef",
    "GetAWSDefaultServiceQuotaResponseTypeDef",
    "GetServiceQuotaResponseTypeDef",
    "ListAWSDefaultServiceQuotasResponseTypeDef",
    "ListServiceQuotasResponseTypeDef",
)

DeleteServiceQuotaIncreaseRequestFromTemplateRequestRequestTypeDef = TypedDict(
    "DeleteServiceQuotaIncreaseRequestFromTemplateRequestRequestTypeDef",
    {
        "ServiceCode": str,
        "QuotaCode": str,
        "AwsRegion": str,
    },
)

ErrorReasonTypeDef = TypedDict(
    "ErrorReasonTypeDef",
    {
        "ErrorCode": ErrorCodeType,
        "ErrorMessage": str,
    },
    total=False,
)

GetAWSDefaultServiceQuotaRequestRequestTypeDef = TypedDict(
    "GetAWSDefaultServiceQuotaRequestRequestTypeDef",
    {
        "ServiceCode": str,
        "QuotaCode": str,
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

GetRequestedServiceQuotaChangeRequestRequestTypeDef = TypedDict(
    "GetRequestedServiceQuotaChangeRequestRequestTypeDef",
    {
        "RequestId": str,
    },
)

RequestedServiceQuotaChangeTypeDef = TypedDict(
    "RequestedServiceQuotaChangeTypeDef",
    {
        "Id": str,
        "CaseId": str,
        "ServiceCode": str,
        "ServiceName": str,
        "QuotaCode": str,
        "QuotaName": str,
        "DesiredValue": float,
        "Status": RequestStatusType,
        "Created": datetime,
        "LastUpdated": datetime,
        "Requester": str,
        "QuotaArn": str,
        "GlobalQuota": bool,
        "Unit": str,
    },
    total=False,
)

GetServiceQuotaIncreaseRequestFromTemplateRequestRequestTypeDef = TypedDict(
    "GetServiceQuotaIncreaseRequestFromTemplateRequestRequestTypeDef",
    {
        "ServiceCode": str,
        "QuotaCode": str,
        "AwsRegion": str,
    },
)

ServiceQuotaIncreaseRequestInTemplateTypeDef = TypedDict(
    "ServiceQuotaIncreaseRequestInTemplateTypeDef",
    {
        "ServiceCode": str,
        "ServiceName": str,
        "QuotaCode": str,
        "QuotaName": str,
        "DesiredValue": float,
        "AwsRegion": str,
        "Unit": str,
        "GlobalQuota": bool,
    },
    total=False,
)

GetServiceQuotaRequestRequestTypeDef = TypedDict(
    "GetServiceQuotaRequestRequestTypeDef",
    {
        "ServiceCode": str,
        "QuotaCode": str,
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

_RequiredListAWSDefaultServiceQuotasRequestRequestTypeDef = TypedDict(
    "_RequiredListAWSDefaultServiceQuotasRequestRequestTypeDef",
    {
        "ServiceCode": str,
    },
)
_OptionalListAWSDefaultServiceQuotasRequestRequestTypeDef = TypedDict(
    "_OptionalListAWSDefaultServiceQuotasRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListAWSDefaultServiceQuotasRequestRequestTypeDef(
    _RequiredListAWSDefaultServiceQuotasRequestRequestTypeDef,
    _OptionalListAWSDefaultServiceQuotasRequestRequestTypeDef,
):
    pass

_RequiredListRequestedServiceQuotaChangeHistoryByQuotaRequestRequestTypeDef = TypedDict(
    "_RequiredListRequestedServiceQuotaChangeHistoryByQuotaRequestRequestTypeDef",
    {
        "ServiceCode": str,
        "QuotaCode": str,
    },
)
_OptionalListRequestedServiceQuotaChangeHistoryByQuotaRequestRequestTypeDef = TypedDict(
    "_OptionalListRequestedServiceQuotaChangeHistoryByQuotaRequestRequestTypeDef",
    {
        "Status": RequestStatusType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListRequestedServiceQuotaChangeHistoryByQuotaRequestRequestTypeDef(
    _RequiredListRequestedServiceQuotaChangeHistoryByQuotaRequestRequestTypeDef,
    _OptionalListRequestedServiceQuotaChangeHistoryByQuotaRequestRequestTypeDef,
):
    pass

ListRequestedServiceQuotaChangeHistoryRequestRequestTypeDef = TypedDict(
    "ListRequestedServiceQuotaChangeHistoryRequestRequestTypeDef",
    {
        "ServiceCode": str,
        "Status": RequestStatusType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListServiceQuotaIncreaseRequestsInTemplateRequestRequestTypeDef = TypedDict(
    "ListServiceQuotaIncreaseRequestsInTemplateRequestRequestTypeDef",
    {
        "ServiceCode": str,
        "AwsRegion": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListServiceQuotasRequestRequestTypeDef = TypedDict(
    "_RequiredListServiceQuotasRequestRequestTypeDef",
    {
        "ServiceCode": str,
    },
)
_OptionalListServiceQuotasRequestRequestTypeDef = TypedDict(
    "_OptionalListServiceQuotasRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListServiceQuotasRequestRequestTypeDef(
    _RequiredListServiceQuotasRequestRequestTypeDef, _OptionalListServiceQuotasRequestRequestTypeDef
):
    pass

ListServicesRequestRequestTypeDef = TypedDict(
    "ListServicesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ServiceInfoTypeDef = TypedDict(
    "ServiceInfoTypeDef",
    {
        "ServiceCode": str,
        "ServiceName": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

MetricInfoTypeDef = TypedDict(
    "MetricInfoTypeDef",
    {
        "MetricNamespace": str,
        "MetricName": str,
        "MetricDimensions": Dict[str, str],
        "MetricStatisticRecommendation": str,
    },
    total=False,
)

PutServiceQuotaIncreaseRequestIntoTemplateRequestRequestTypeDef = TypedDict(
    "PutServiceQuotaIncreaseRequestIntoTemplateRequestRequestTypeDef",
    {
        "QuotaCode": str,
        "ServiceCode": str,
        "AwsRegion": str,
        "DesiredValue": float,
    },
)

QuotaPeriodTypeDef = TypedDict(
    "QuotaPeriodTypeDef",
    {
        "PeriodValue": int,
        "PeriodUnit": PeriodUnitType,
    },
    total=False,
)

RequestServiceQuotaIncreaseRequestRequestTypeDef = TypedDict(
    "RequestServiceQuotaIncreaseRequestRequestTypeDef",
    {
        "ServiceCode": str,
        "QuotaCode": str,
        "DesiredValue": float,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

GetAssociationForServiceQuotaTemplateResponseTypeDef = TypedDict(
    "GetAssociationForServiceQuotaTemplateResponseTypeDef",
    {
        "ServiceQuotaTemplateAssociationStatus": ServiceQuotaTemplateAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRequestedServiceQuotaChangeResponseTypeDef = TypedDict(
    "GetRequestedServiceQuotaChangeResponseTypeDef",
    {
        "RequestedQuota": RequestedServiceQuotaChangeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRequestedServiceQuotaChangeHistoryByQuotaResponseTypeDef = TypedDict(
    "ListRequestedServiceQuotaChangeHistoryByQuotaResponseTypeDef",
    {
        "NextToken": str,
        "RequestedQuotas": List[RequestedServiceQuotaChangeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRequestedServiceQuotaChangeHistoryResponseTypeDef = TypedDict(
    "ListRequestedServiceQuotaChangeHistoryResponseTypeDef",
    {
        "NextToken": str,
        "RequestedQuotas": List[RequestedServiceQuotaChangeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RequestServiceQuotaIncreaseResponseTypeDef = TypedDict(
    "RequestServiceQuotaIncreaseResponseTypeDef",
    {
        "RequestedQuota": RequestedServiceQuotaChangeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceQuotaIncreaseRequestFromTemplateResponseTypeDef = TypedDict(
    "GetServiceQuotaIncreaseRequestFromTemplateResponseTypeDef",
    {
        "ServiceQuotaIncreaseRequestInTemplate": ServiceQuotaIncreaseRequestInTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServiceQuotaIncreaseRequestsInTemplateResponseTypeDef = TypedDict(
    "ListServiceQuotaIncreaseRequestsInTemplateResponseTypeDef",
    {
        "ServiceQuotaIncreaseRequestInTemplateList": List[
            ServiceQuotaIncreaseRequestInTemplateTypeDef
        ],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutServiceQuotaIncreaseRequestIntoTemplateResponseTypeDef = TypedDict(
    "PutServiceQuotaIncreaseRequestIntoTemplateResponseTypeDef",
    {
        "ServiceQuotaIncreaseRequestInTemplate": ServiceQuotaIncreaseRequestInTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListAWSDefaultServiceQuotasRequestListAWSDefaultServiceQuotasPaginateTypeDef = TypedDict(
    "_RequiredListAWSDefaultServiceQuotasRequestListAWSDefaultServiceQuotasPaginateTypeDef",
    {
        "ServiceCode": str,
    },
)
_OptionalListAWSDefaultServiceQuotasRequestListAWSDefaultServiceQuotasPaginateTypeDef = TypedDict(
    "_OptionalListAWSDefaultServiceQuotasRequestListAWSDefaultServiceQuotasPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListAWSDefaultServiceQuotasRequestListAWSDefaultServiceQuotasPaginateTypeDef(
    _RequiredListAWSDefaultServiceQuotasRequestListAWSDefaultServiceQuotasPaginateTypeDef,
    _OptionalListAWSDefaultServiceQuotasRequestListAWSDefaultServiceQuotasPaginateTypeDef,
):
    pass

_RequiredListRequestedServiceQuotaChangeHistoryByQuotaRequestListRequestedServiceQuotaChangeHistoryByQuotaPaginateTypeDef = TypedDict(
    "_RequiredListRequestedServiceQuotaChangeHistoryByQuotaRequestListRequestedServiceQuotaChangeHistoryByQuotaPaginateTypeDef",
    {
        "ServiceCode": str,
        "QuotaCode": str,
    },
)
_OptionalListRequestedServiceQuotaChangeHistoryByQuotaRequestListRequestedServiceQuotaChangeHistoryByQuotaPaginateTypeDef = TypedDict(
    "_OptionalListRequestedServiceQuotaChangeHistoryByQuotaRequestListRequestedServiceQuotaChangeHistoryByQuotaPaginateTypeDef",
    {
        "Status": RequestStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListRequestedServiceQuotaChangeHistoryByQuotaRequestListRequestedServiceQuotaChangeHistoryByQuotaPaginateTypeDef(
    _RequiredListRequestedServiceQuotaChangeHistoryByQuotaRequestListRequestedServiceQuotaChangeHistoryByQuotaPaginateTypeDef,
    _OptionalListRequestedServiceQuotaChangeHistoryByQuotaRequestListRequestedServiceQuotaChangeHistoryByQuotaPaginateTypeDef,
):
    pass

ListRequestedServiceQuotaChangeHistoryRequestListRequestedServiceQuotaChangeHistoryPaginateTypeDef = TypedDict(
    "ListRequestedServiceQuotaChangeHistoryRequestListRequestedServiceQuotaChangeHistoryPaginateTypeDef",
    {
        "ServiceCode": str,
        "Status": RequestStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListServiceQuotaIncreaseRequestsInTemplateRequestListServiceQuotaIncreaseRequestsInTemplatePaginateTypeDef = TypedDict(
    "ListServiceQuotaIncreaseRequestsInTemplateRequestListServiceQuotaIncreaseRequestsInTemplatePaginateTypeDef",
    {
        "ServiceCode": str,
        "AwsRegion": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListServiceQuotasRequestListServiceQuotasPaginateTypeDef = TypedDict(
    "_RequiredListServiceQuotasRequestListServiceQuotasPaginateTypeDef",
    {
        "ServiceCode": str,
    },
)
_OptionalListServiceQuotasRequestListServiceQuotasPaginateTypeDef = TypedDict(
    "_OptionalListServiceQuotasRequestListServiceQuotasPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListServiceQuotasRequestListServiceQuotasPaginateTypeDef(
    _RequiredListServiceQuotasRequestListServiceQuotasPaginateTypeDef,
    _OptionalListServiceQuotasRequestListServiceQuotasPaginateTypeDef,
):
    pass

ListServicesRequestListServicesPaginateTypeDef = TypedDict(
    "ListServicesRequestListServicesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListServicesResponseTypeDef = TypedDict(
    "ListServicesResponseTypeDef",
    {
        "NextToken": str,
        "Services": List[ServiceInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

ServiceQuotaTypeDef = TypedDict(
    "ServiceQuotaTypeDef",
    {
        "ServiceCode": str,
        "ServiceName": str,
        "QuotaArn": str,
        "QuotaCode": str,
        "QuotaName": str,
        "Value": float,
        "Unit": str,
        "Adjustable": bool,
        "GlobalQuota": bool,
        "UsageMetric": MetricInfoTypeDef,
        "Period": QuotaPeriodTypeDef,
        "ErrorReason": ErrorReasonTypeDef,
    },
    total=False,
)

GetAWSDefaultServiceQuotaResponseTypeDef = TypedDict(
    "GetAWSDefaultServiceQuotaResponseTypeDef",
    {
        "Quota": ServiceQuotaTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceQuotaResponseTypeDef = TypedDict(
    "GetServiceQuotaResponseTypeDef",
    {
        "Quota": ServiceQuotaTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAWSDefaultServiceQuotasResponseTypeDef = TypedDict(
    "ListAWSDefaultServiceQuotasResponseTypeDef",
    {
        "NextToken": str,
        "Quotas": List[ServiceQuotaTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServiceQuotasResponseTypeDef = TypedDict(
    "ListServiceQuotasResponseTypeDef",
    {
        "NextToken": str,
        "Quotas": List[ServiceQuotaTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
