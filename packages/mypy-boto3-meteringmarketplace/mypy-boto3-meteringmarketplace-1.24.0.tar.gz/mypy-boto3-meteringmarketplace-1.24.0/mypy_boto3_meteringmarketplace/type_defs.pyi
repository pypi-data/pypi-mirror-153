"""
Type annotations for meteringmarketplace service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_meteringmarketplace/type_defs/)

Usage::

    ```python
    from mypy_boto3_meteringmarketplace.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import UsageRecordResultStatusType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ResponseMetadataTypeDef",
    "RegisterUsageRequestRequestTypeDef",
    "ResolveCustomerRequestRequestTypeDef",
    "TagTypeDef",
    "MeterUsageResultTypeDef",
    "RegisterUsageResultTypeDef",
    "ResolveCustomerResultTypeDef",
    "UsageAllocationTypeDef",
    "MeterUsageRequestRequestTypeDef",
    "UsageRecordTypeDef",
    "BatchMeterUsageRequestRequestTypeDef",
    "UsageRecordResultTypeDef",
    "BatchMeterUsageResultTypeDef",
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

_RequiredRegisterUsageRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterUsageRequestRequestTypeDef",
    {
        "ProductCode": str,
        "PublicKeyVersion": int,
    },
)
_OptionalRegisterUsageRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterUsageRequestRequestTypeDef",
    {
        "Nonce": str,
    },
    total=False,
)

class RegisterUsageRequestRequestTypeDef(
    _RequiredRegisterUsageRequestRequestTypeDef, _OptionalRegisterUsageRequestRequestTypeDef
):
    pass

ResolveCustomerRequestRequestTypeDef = TypedDict(
    "ResolveCustomerRequestRequestTypeDef",
    {
        "RegistrationToken": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

MeterUsageResultTypeDef = TypedDict(
    "MeterUsageResultTypeDef",
    {
        "MeteringRecordId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterUsageResultTypeDef = TypedDict(
    "RegisterUsageResultTypeDef",
    {
        "PublicKeyRotationTimestamp": datetime,
        "Signature": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResolveCustomerResultTypeDef = TypedDict(
    "ResolveCustomerResultTypeDef",
    {
        "CustomerIdentifier": str,
        "ProductCode": str,
        "CustomerAWSAccountId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUsageAllocationTypeDef = TypedDict(
    "_RequiredUsageAllocationTypeDef",
    {
        "AllocatedUsageQuantity": int,
    },
)
_OptionalUsageAllocationTypeDef = TypedDict(
    "_OptionalUsageAllocationTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class UsageAllocationTypeDef(_RequiredUsageAllocationTypeDef, _OptionalUsageAllocationTypeDef):
    pass

_RequiredMeterUsageRequestRequestTypeDef = TypedDict(
    "_RequiredMeterUsageRequestRequestTypeDef",
    {
        "ProductCode": str,
        "Timestamp": Union[datetime, str],
        "UsageDimension": str,
    },
)
_OptionalMeterUsageRequestRequestTypeDef = TypedDict(
    "_OptionalMeterUsageRequestRequestTypeDef",
    {
        "UsageQuantity": int,
        "DryRun": bool,
        "UsageAllocations": Sequence[UsageAllocationTypeDef],
    },
    total=False,
)

class MeterUsageRequestRequestTypeDef(
    _RequiredMeterUsageRequestRequestTypeDef, _OptionalMeterUsageRequestRequestTypeDef
):
    pass

_RequiredUsageRecordTypeDef = TypedDict(
    "_RequiredUsageRecordTypeDef",
    {
        "Timestamp": Union[datetime, str],
        "CustomerIdentifier": str,
        "Dimension": str,
    },
)
_OptionalUsageRecordTypeDef = TypedDict(
    "_OptionalUsageRecordTypeDef",
    {
        "Quantity": int,
        "UsageAllocations": Sequence[UsageAllocationTypeDef],
    },
    total=False,
)

class UsageRecordTypeDef(_RequiredUsageRecordTypeDef, _OptionalUsageRecordTypeDef):
    pass

BatchMeterUsageRequestRequestTypeDef = TypedDict(
    "BatchMeterUsageRequestRequestTypeDef",
    {
        "UsageRecords": Sequence[UsageRecordTypeDef],
        "ProductCode": str,
    },
)

UsageRecordResultTypeDef = TypedDict(
    "UsageRecordResultTypeDef",
    {
        "UsageRecord": UsageRecordTypeDef,
        "MeteringRecordId": str,
        "Status": UsageRecordResultStatusType,
    },
    total=False,
)

BatchMeterUsageResultTypeDef = TypedDict(
    "BatchMeterUsageResultTypeDef",
    {
        "Results": List[UsageRecordResultTypeDef],
        "UnprocessedRecords": List[UsageRecordTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
