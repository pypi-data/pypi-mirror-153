"""
Type annotations for elastic-inference service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/type_defs/)

Usage::

    ```python
    from mypy_boto3_elastic_inference.type_defs import AcceleratorTypeOfferingTypeDef

    data: AcceleratorTypeOfferingTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import LocationTypeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AcceleratorTypeOfferingTypeDef",
    "KeyValuePairTypeDef",
    "MemoryInfoTypeDef",
    "DescribeAcceleratorOfferingsRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "FilterTypeDef",
    "PaginatorConfigTypeDef",
    "ElasticInferenceAcceleratorHealthTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AcceleratorTypeTypeDef",
    "DescribeAcceleratorOfferingsResponseTypeDef",
    "ListTagsForResourceResultTypeDef",
    "DescribeAcceleratorsRequestRequestTypeDef",
    "DescribeAcceleratorsRequestDescribeAcceleratorsPaginateTypeDef",
    "ElasticInferenceAcceleratorTypeDef",
    "DescribeAcceleratorTypesResponseTypeDef",
    "DescribeAcceleratorsResponseTypeDef",
)

AcceleratorTypeOfferingTypeDef = TypedDict(
    "AcceleratorTypeOfferingTypeDef",
    {
        "acceleratorType": str,
        "locationType": LocationTypeType,
        "location": str,
    },
    total=False,
)

KeyValuePairTypeDef = TypedDict(
    "KeyValuePairTypeDef",
    {
        "key": str,
        "value": int,
    },
    total=False,
)

MemoryInfoTypeDef = TypedDict(
    "MemoryInfoTypeDef",
    {
        "sizeInMiB": int,
    },
    total=False,
)

_RequiredDescribeAcceleratorOfferingsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAcceleratorOfferingsRequestRequestTypeDef",
    {
        "locationType": LocationTypeType,
    },
)
_OptionalDescribeAcceleratorOfferingsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAcceleratorOfferingsRequestRequestTypeDef",
    {
        "acceleratorTypes": Sequence[str],
    },
    total=False,
)

class DescribeAcceleratorOfferingsRequestRequestTypeDef(
    _RequiredDescribeAcceleratorOfferingsRequestRequestTypeDef,
    _OptionalDescribeAcceleratorOfferingsRequestRequestTypeDef,
):
    pass

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

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "name": str,
        "values": Sequence[str],
    },
    total=False,
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

ElasticInferenceAcceleratorHealthTypeDef = TypedDict(
    "ElasticInferenceAcceleratorHealthTypeDef",
    {
        "status": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

AcceleratorTypeTypeDef = TypedDict(
    "AcceleratorTypeTypeDef",
    {
        "acceleratorTypeName": str,
        "memoryInfo": MemoryInfoTypeDef,
        "throughputInfo": List[KeyValuePairTypeDef],
    },
    total=False,
)

DescribeAcceleratorOfferingsResponseTypeDef = TypedDict(
    "DescribeAcceleratorOfferingsResponseTypeDef",
    {
        "acceleratorTypeOfferings": List[AcceleratorTypeOfferingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResultTypeDef = TypedDict(
    "ListTagsForResourceResultTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAcceleratorsRequestRequestTypeDef = TypedDict(
    "DescribeAcceleratorsRequestRequestTypeDef",
    {
        "acceleratorIds": Sequence[str],
        "filters": Sequence[FilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeAcceleratorsRequestDescribeAcceleratorsPaginateTypeDef = TypedDict(
    "DescribeAcceleratorsRequestDescribeAcceleratorsPaginateTypeDef",
    {
        "acceleratorIds": Sequence[str],
        "filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ElasticInferenceAcceleratorTypeDef = TypedDict(
    "ElasticInferenceAcceleratorTypeDef",
    {
        "acceleratorHealth": ElasticInferenceAcceleratorHealthTypeDef,
        "acceleratorType": str,
        "acceleratorId": str,
        "availabilityZone": str,
        "attachedResource": str,
    },
    total=False,
)

DescribeAcceleratorTypesResponseTypeDef = TypedDict(
    "DescribeAcceleratorTypesResponseTypeDef",
    {
        "acceleratorTypes": List[AcceleratorTypeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAcceleratorsResponseTypeDef = TypedDict(
    "DescribeAcceleratorsResponseTypeDef",
    {
        "acceleratorSet": List[ElasticInferenceAcceleratorTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
