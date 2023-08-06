"""
Type annotations for appconfigdata service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfigdata/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_appconfigdata.client import AppConfigDataClient

    session = Session()
    client: AppConfigDataClient = session.client("appconfigdata")
    ```
"""
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    GetLatestConfigurationResponseTypeDef,
    StartConfigurationSessionResponseTypeDef,
)

__all__ = ("AppConfigDataClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class AppConfigDataClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfigdata.html#AppConfigData.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfigdata/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppConfigDataClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfigdata.html#AppConfigData.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfigdata/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfigdata.html#AppConfigData.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfigdata/client/#can_paginate)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfigdata.html#AppConfigData.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfigdata/client/#generate_presigned_url)
        """

    def get_latest_configuration(
        self, *, ConfigurationToken: str
    ) -> GetLatestConfigurationResponseTypeDef:
        """
        Retrieves the latest deployed configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfigdata.html#AppConfigData.Client.get_latest_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfigdata/client/#get_latest_configuration)
        """

    def start_configuration_session(
        self,
        *,
        ApplicationIdentifier: str,
        EnvironmentIdentifier: str,
        ConfigurationProfileIdentifier: str,
        RequiredMinimumPollIntervalInSeconds: int = ...
    ) -> StartConfigurationSessionResponseTypeDef:
        """
        Starts a configuration session used to retrieve a deployed configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfigdata.html#AppConfigData.Client.start_configuration_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfigdata/client/#start_configuration_session)
        """
