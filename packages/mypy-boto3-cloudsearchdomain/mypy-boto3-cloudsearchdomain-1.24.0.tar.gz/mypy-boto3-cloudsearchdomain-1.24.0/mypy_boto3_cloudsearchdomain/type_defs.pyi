"""
Type annotations for cloudsearchdomain service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearchdomain/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloudsearchdomain.type_defs import BucketTypeDef

    data: BucketTypeDef = {...}
    ```
"""
import sys
from typing import IO, Any, Dict, List, Union

from botocore.response import StreamingBody

from .literals import ContentTypeType, QueryParserType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "BucketTypeDef",
    "DocumentServiceWarningTypeDef",
    "FieldStatsTypeDef",
    "HitTypeDef",
    "ResponseMetadataTypeDef",
    "SearchRequestRequestTypeDef",
    "SearchStatusTypeDef",
    "SuggestionMatchTypeDef",
    "SuggestRequestRequestTypeDef",
    "SuggestStatusTypeDef",
    "UploadDocumentsRequestRequestTypeDef",
    "BucketInfoTypeDef",
    "HitsTypeDef",
    "UploadDocumentsResponseTypeDef",
    "SuggestModelTypeDef",
    "SearchResponseTypeDef",
    "SuggestResponseTypeDef",
)

BucketTypeDef = TypedDict(
    "BucketTypeDef",
    {
        "value": str,
        "count": int,
    },
    total=False,
)

DocumentServiceWarningTypeDef = TypedDict(
    "DocumentServiceWarningTypeDef",
    {
        "message": str,
    },
    total=False,
)

FieldStatsTypeDef = TypedDict(
    "FieldStatsTypeDef",
    {
        "min": str,
        "max": str,
        "count": int,
        "missing": int,
        "sum": float,
        "sumOfSquares": float,
        "mean": str,
        "stddev": float,
    },
    total=False,
)

HitTypeDef = TypedDict(
    "HitTypeDef",
    {
        "id": str,
        "fields": Dict[str, List[str]],
        "exprs": Dict[str, str],
        "highlights": Dict[str, str],
    },
    total=False,
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

_RequiredSearchRequestRequestTypeDef = TypedDict(
    "_RequiredSearchRequestRequestTypeDef",
    {
        "query": str,
    },
)
_OptionalSearchRequestRequestTypeDef = TypedDict(
    "_OptionalSearchRequestRequestTypeDef",
    {
        "cursor": str,
        "expr": str,
        "facet": str,
        "filterQuery": str,
        "highlight": str,
        "partial": bool,
        "queryOptions": str,
        "queryParser": QueryParserType,
        "returnFields": str,
        "size": int,
        "sort": str,
        "start": int,
        "stats": str,
    },
    total=False,
)

class SearchRequestRequestTypeDef(
    _RequiredSearchRequestRequestTypeDef, _OptionalSearchRequestRequestTypeDef
):
    pass

SearchStatusTypeDef = TypedDict(
    "SearchStatusTypeDef",
    {
        "timems": int,
        "rid": str,
    },
    total=False,
)

SuggestionMatchTypeDef = TypedDict(
    "SuggestionMatchTypeDef",
    {
        "suggestion": str,
        "score": int,
        "id": str,
    },
    total=False,
)

_RequiredSuggestRequestRequestTypeDef = TypedDict(
    "_RequiredSuggestRequestRequestTypeDef",
    {
        "query": str,
        "suggester": str,
    },
)
_OptionalSuggestRequestRequestTypeDef = TypedDict(
    "_OptionalSuggestRequestRequestTypeDef",
    {
        "size": int,
    },
    total=False,
)

class SuggestRequestRequestTypeDef(
    _RequiredSuggestRequestRequestTypeDef, _OptionalSuggestRequestRequestTypeDef
):
    pass

SuggestStatusTypeDef = TypedDict(
    "SuggestStatusTypeDef",
    {
        "timems": int,
        "rid": str,
    },
    total=False,
)

UploadDocumentsRequestRequestTypeDef = TypedDict(
    "UploadDocumentsRequestRequestTypeDef",
    {
        "documents": Union[str, bytes, IO[Any], StreamingBody],
        "contentType": ContentTypeType,
    },
)

BucketInfoTypeDef = TypedDict(
    "BucketInfoTypeDef",
    {
        "buckets": List[BucketTypeDef],
    },
    total=False,
)

HitsTypeDef = TypedDict(
    "HitsTypeDef",
    {
        "found": int,
        "start": int,
        "cursor": str,
        "hit": List[HitTypeDef],
    },
    total=False,
)

UploadDocumentsResponseTypeDef = TypedDict(
    "UploadDocumentsResponseTypeDef",
    {
        "status": str,
        "adds": int,
        "deletes": int,
        "warnings": List[DocumentServiceWarningTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SuggestModelTypeDef = TypedDict(
    "SuggestModelTypeDef",
    {
        "query": str,
        "found": int,
        "suggestions": List[SuggestionMatchTypeDef],
    },
    total=False,
)

SearchResponseTypeDef = TypedDict(
    "SearchResponseTypeDef",
    {
        "status": SearchStatusTypeDef,
        "hits": HitsTypeDef,
        "facets": Dict[str, BucketInfoTypeDef],
        "stats": Dict[str, FieldStatsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SuggestResponseTypeDef = TypedDict(
    "SuggestResponseTypeDef",
    {
        "status": SuggestStatusTypeDef,
        "suggest": SuggestModelTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
