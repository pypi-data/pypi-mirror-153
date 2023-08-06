"""
Type annotations for acm service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/type_defs/)

Usage::

    ```python
    from mypy_boto3_acm.type_defs import TagTypeDef

    data: TagTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    CertificateStatusType,
    CertificateTransparencyLoggingPreferenceType,
    CertificateTypeType,
    DomainStatusType,
    ExtendedKeyUsageNameType,
    FailureReasonType,
    KeyAlgorithmType,
    KeyUsageNameType,
    RenewalEligibilityType,
    RenewalStatusType,
    RevocationReasonType,
    ValidationMethodType,
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
    "TagTypeDef",
    "CertificateOptionsTypeDef",
    "ExtendedKeyUsageTypeDef",
    "KeyUsageTypeDef",
    "CertificateSummaryTypeDef",
    "DeleteCertificateRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeCertificateRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "DomainValidationOptionTypeDef",
    "ResourceRecordTypeDef",
    "ExpiryEventsConfigurationTypeDef",
    "ExportCertificateRequestRequestTypeDef",
    "FiltersTypeDef",
    "GetCertificateRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListTagsForCertificateRequestRequestTypeDef",
    "RenewCertificateRequestRequestTypeDef",
    "ResendValidationEmailRequestRequestTypeDef",
    "AddTagsToCertificateRequestRequestTypeDef",
    "ImportCertificateRequestRequestTypeDef",
    "RemoveTagsFromCertificateRequestRequestTypeDef",
    "UpdateCertificateOptionsRequestRequestTypeDef",
    "DescribeCertificateRequestCertificateValidatedWaitTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExportCertificateResponseTypeDef",
    "GetCertificateResponseTypeDef",
    "ImportCertificateResponseTypeDef",
    "ListCertificatesResponseTypeDef",
    "ListTagsForCertificateResponseTypeDef",
    "RequestCertificateResponseTypeDef",
    "RequestCertificateRequestRequestTypeDef",
    "DomainValidationTypeDef",
    "GetAccountConfigurationResponseTypeDef",
    "PutAccountConfigurationRequestRequestTypeDef",
    "ListCertificatesRequestRequestTypeDef",
    "ListCertificatesRequestListCertificatesPaginateTypeDef",
    "RenewalSummaryTypeDef",
    "CertificateDetailTypeDef",
    "DescribeCertificateResponseTypeDef",
)

_RequiredTagTypeDef = TypedDict(
    "_RequiredTagTypeDef",
    {
        "Key": str,
    },
)
_OptionalTagTypeDef = TypedDict(
    "_OptionalTagTypeDef",
    {
        "Value": str,
    },
    total=False,
)


class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
    pass


CertificateOptionsTypeDef = TypedDict(
    "CertificateOptionsTypeDef",
    {
        "CertificateTransparencyLoggingPreference": CertificateTransparencyLoggingPreferenceType,
    },
    total=False,
)

ExtendedKeyUsageTypeDef = TypedDict(
    "ExtendedKeyUsageTypeDef",
    {
        "Name": ExtendedKeyUsageNameType,
        "OID": str,
    },
    total=False,
)

KeyUsageTypeDef = TypedDict(
    "KeyUsageTypeDef",
    {
        "Name": KeyUsageNameType,
    },
    total=False,
)

CertificateSummaryTypeDef = TypedDict(
    "CertificateSummaryTypeDef",
    {
        "CertificateArn": str,
        "DomainName": str,
    },
    total=False,
)

DeleteCertificateRequestRequestTypeDef = TypedDict(
    "DeleteCertificateRequestRequestTypeDef",
    {
        "CertificateArn": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeCertificateRequestRequestTypeDef = TypedDict(
    "DescribeCertificateRequestRequestTypeDef",
    {
        "CertificateArn": str,
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

DomainValidationOptionTypeDef = TypedDict(
    "DomainValidationOptionTypeDef",
    {
        "DomainName": str,
        "ValidationDomain": str,
    },
)

ResourceRecordTypeDef = TypedDict(
    "ResourceRecordTypeDef",
    {
        "Name": str,
        "Type": Literal["CNAME"],
        "Value": str,
    },
)

ExpiryEventsConfigurationTypeDef = TypedDict(
    "ExpiryEventsConfigurationTypeDef",
    {
        "DaysBeforeExpiry": int,
    },
    total=False,
)

ExportCertificateRequestRequestTypeDef = TypedDict(
    "ExportCertificateRequestRequestTypeDef",
    {
        "CertificateArn": str,
        "Passphrase": Union[str, bytes, IO[Any], StreamingBody],
    },
)

FiltersTypeDef = TypedDict(
    "FiltersTypeDef",
    {
        "extendedKeyUsage": Sequence[ExtendedKeyUsageNameType],
        "keyUsage": Sequence[KeyUsageNameType],
        "keyTypes": Sequence[KeyAlgorithmType],
    },
    total=False,
)

GetCertificateRequestRequestTypeDef = TypedDict(
    "GetCertificateRequestRequestTypeDef",
    {
        "CertificateArn": str,
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

ListTagsForCertificateRequestRequestTypeDef = TypedDict(
    "ListTagsForCertificateRequestRequestTypeDef",
    {
        "CertificateArn": str,
    },
)

RenewCertificateRequestRequestTypeDef = TypedDict(
    "RenewCertificateRequestRequestTypeDef",
    {
        "CertificateArn": str,
    },
)

ResendValidationEmailRequestRequestTypeDef = TypedDict(
    "ResendValidationEmailRequestRequestTypeDef",
    {
        "CertificateArn": str,
        "Domain": str,
        "ValidationDomain": str,
    },
)

AddTagsToCertificateRequestRequestTypeDef = TypedDict(
    "AddTagsToCertificateRequestRequestTypeDef",
    {
        "CertificateArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredImportCertificateRequestRequestTypeDef = TypedDict(
    "_RequiredImportCertificateRequestRequestTypeDef",
    {
        "Certificate": Union[str, bytes, IO[Any], StreamingBody],
        "PrivateKey": Union[str, bytes, IO[Any], StreamingBody],
    },
)
_OptionalImportCertificateRequestRequestTypeDef = TypedDict(
    "_OptionalImportCertificateRequestRequestTypeDef",
    {
        "CertificateArn": str,
        "CertificateChain": Union[str, bytes, IO[Any], StreamingBody],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class ImportCertificateRequestRequestTypeDef(
    _RequiredImportCertificateRequestRequestTypeDef, _OptionalImportCertificateRequestRequestTypeDef
):
    pass


RemoveTagsFromCertificateRequestRequestTypeDef = TypedDict(
    "RemoveTagsFromCertificateRequestRequestTypeDef",
    {
        "CertificateArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

UpdateCertificateOptionsRequestRequestTypeDef = TypedDict(
    "UpdateCertificateOptionsRequestRequestTypeDef",
    {
        "CertificateArn": str,
        "Options": CertificateOptionsTypeDef,
    },
)

_RequiredDescribeCertificateRequestCertificateValidatedWaitTypeDef = TypedDict(
    "_RequiredDescribeCertificateRequestCertificateValidatedWaitTypeDef",
    {
        "CertificateArn": str,
    },
)
_OptionalDescribeCertificateRequestCertificateValidatedWaitTypeDef = TypedDict(
    "_OptionalDescribeCertificateRequestCertificateValidatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeCertificateRequestCertificateValidatedWaitTypeDef(
    _RequiredDescribeCertificateRequestCertificateValidatedWaitTypeDef,
    _OptionalDescribeCertificateRequestCertificateValidatedWaitTypeDef,
):
    pass


EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportCertificateResponseTypeDef = TypedDict(
    "ExportCertificateResponseTypeDef",
    {
        "Certificate": str,
        "CertificateChain": str,
        "PrivateKey": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCertificateResponseTypeDef = TypedDict(
    "GetCertificateResponseTypeDef",
    {
        "Certificate": str,
        "CertificateChain": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportCertificateResponseTypeDef = TypedDict(
    "ImportCertificateResponseTypeDef",
    {
        "CertificateArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCertificatesResponseTypeDef = TypedDict(
    "ListCertificatesResponseTypeDef",
    {
        "NextToken": str,
        "CertificateSummaryList": List[CertificateSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForCertificateResponseTypeDef = TypedDict(
    "ListTagsForCertificateResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RequestCertificateResponseTypeDef = TypedDict(
    "RequestCertificateResponseTypeDef",
    {
        "CertificateArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRequestCertificateRequestRequestTypeDef = TypedDict(
    "_RequiredRequestCertificateRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalRequestCertificateRequestRequestTypeDef = TypedDict(
    "_OptionalRequestCertificateRequestRequestTypeDef",
    {
        "ValidationMethod": ValidationMethodType,
        "SubjectAlternativeNames": Sequence[str],
        "IdempotencyToken": str,
        "DomainValidationOptions": Sequence[DomainValidationOptionTypeDef],
        "Options": CertificateOptionsTypeDef,
        "CertificateAuthorityArn": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class RequestCertificateRequestRequestTypeDef(
    _RequiredRequestCertificateRequestRequestTypeDef,
    _OptionalRequestCertificateRequestRequestTypeDef,
):
    pass


_RequiredDomainValidationTypeDef = TypedDict(
    "_RequiredDomainValidationTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalDomainValidationTypeDef = TypedDict(
    "_OptionalDomainValidationTypeDef",
    {
        "ValidationEmails": List[str],
        "ValidationDomain": str,
        "ValidationStatus": DomainStatusType,
        "ResourceRecord": ResourceRecordTypeDef,
        "ValidationMethod": ValidationMethodType,
    },
    total=False,
)


class DomainValidationTypeDef(_RequiredDomainValidationTypeDef, _OptionalDomainValidationTypeDef):
    pass


GetAccountConfigurationResponseTypeDef = TypedDict(
    "GetAccountConfigurationResponseTypeDef",
    {
        "ExpiryEvents": ExpiryEventsConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutAccountConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutAccountConfigurationRequestRequestTypeDef",
    {
        "IdempotencyToken": str,
    },
)
_OptionalPutAccountConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutAccountConfigurationRequestRequestTypeDef",
    {
        "ExpiryEvents": ExpiryEventsConfigurationTypeDef,
    },
    total=False,
)


class PutAccountConfigurationRequestRequestTypeDef(
    _RequiredPutAccountConfigurationRequestRequestTypeDef,
    _OptionalPutAccountConfigurationRequestRequestTypeDef,
):
    pass


ListCertificatesRequestRequestTypeDef = TypedDict(
    "ListCertificatesRequestRequestTypeDef",
    {
        "CertificateStatuses": Sequence[CertificateStatusType],
        "Includes": FiltersTypeDef,
        "NextToken": str,
        "MaxItems": int,
    },
    total=False,
)

ListCertificatesRequestListCertificatesPaginateTypeDef = TypedDict(
    "ListCertificatesRequestListCertificatesPaginateTypeDef",
    {
        "CertificateStatuses": Sequence[CertificateStatusType],
        "Includes": FiltersTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredRenewalSummaryTypeDef = TypedDict(
    "_RequiredRenewalSummaryTypeDef",
    {
        "RenewalStatus": RenewalStatusType,
        "DomainValidationOptions": List[DomainValidationTypeDef],
        "UpdatedAt": datetime,
    },
)
_OptionalRenewalSummaryTypeDef = TypedDict(
    "_OptionalRenewalSummaryTypeDef",
    {
        "RenewalStatusReason": FailureReasonType,
    },
    total=False,
)


class RenewalSummaryTypeDef(_RequiredRenewalSummaryTypeDef, _OptionalRenewalSummaryTypeDef):
    pass


CertificateDetailTypeDef = TypedDict(
    "CertificateDetailTypeDef",
    {
        "CertificateArn": str,
        "DomainName": str,
        "SubjectAlternativeNames": List[str],
        "DomainValidationOptions": List[DomainValidationTypeDef],
        "Serial": str,
        "Subject": str,
        "Issuer": str,
        "CreatedAt": datetime,
        "IssuedAt": datetime,
        "ImportedAt": datetime,
        "Status": CertificateStatusType,
        "RevokedAt": datetime,
        "RevocationReason": RevocationReasonType,
        "NotBefore": datetime,
        "NotAfter": datetime,
        "KeyAlgorithm": KeyAlgorithmType,
        "SignatureAlgorithm": str,
        "InUseBy": List[str],
        "FailureReason": FailureReasonType,
        "Type": CertificateTypeType,
        "RenewalSummary": RenewalSummaryTypeDef,
        "KeyUsages": List[KeyUsageTypeDef],
        "ExtendedKeyUsages": List[ExtendedKeyUsageTypeDef],
        "CertificateAuthorityArn": str,
        "RenewalEligibility": RenewalEligibilityType,
        "Options": CertificateOptionsTypeDef,
    },
    total=False,
)

DescribeCertificateResponseTypeDef = TypedDict(
    "DescribeCertificateResponseTypeDef",
    {
        "Certificate": CertificateDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
