"""
Type annotations for appconfigdata service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfigdata/type_defs/)

Usage::

    ```python
    from mypy_boto3_appconfigdata.type_defs import GetLatestConfigurationRequestRequestTypeDef

    data: GetLatestConfigurationRequestRequestTypeDef = {...}
    ```
"""
import sys
from typing import Dict

from botocore.response import StreamingBody

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "GetLatestConfigurationRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "StartConfigurationSessionRequestRequestTypeDef",
    "GetLatestConfigurationResponseTypeDef",
    "StartConfigurationSessionResponseTypeDef",
)

GetLatestConfigurationRequestRequestTypeDef = TypedDict(
    "GetLatestConfigurationRequestRequestTypeDef",
    {
        "ConfigurationToken": str,
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

_RequiredStartConfigurationSessionRequestRequestTypeDef = TypedDict(
    "_RequiredStartConfigurationSessionRequestRequestTypeDef",
    {
        "ApplicationIdentifier": str,
        "EnvironmentIdentifier": str,
        "ConfigurationProfileIdentifier": str,
    },
)
_OptionalStartConfigurationSessionRequestRequestTypeDef = TypedDict(
    "_OptionalStartConfigurationSessionRequestRequestTypeDef",
    {
        "RequiredMinimumPollIntervalInSeconds": int,
    },
    total=False,
)


class StartConfigurationSessionRequestRequestTypeDef(
    _RequiredStartConfigurationSessionRequestRequestTypeDef,
    _OptionalStartConfigurationSessionRequestRequestTypeDef,
):
    pass


GetLatestConfigurationResponseTypeDef = TypedDict(
    "GetLatestConfigurationResponseTypeDef",
    {
        "NextPollConfigurationToken": str,
        "NextPollIntervalInSeconds": int,
        "ContentType": str,
        "Configuration": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartConfigurationSessionResponseTypeDef = TypedDict(
    "StartConfigurationSessionResponseTypeDef",
    {
        "InitialConfigurationToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
