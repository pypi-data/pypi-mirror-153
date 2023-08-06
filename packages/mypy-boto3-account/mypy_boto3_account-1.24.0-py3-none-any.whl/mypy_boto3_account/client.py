"""
Type annotations for account service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_account.client import AccountClient

    session = Session()
    client: AccountClient = session.client("account")
    ```
"""
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .literals import AlternateContactTypeType
from .type_defs import EmptyResponseMetadataTypeDef, GetAlternateContactResponseTypeDef

__all__ = ("AccountClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class AccountClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account.html#Account.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AccountClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account.html#Account.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account.html#Account.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account/client/#can_paginate)
        """

    def delete_alternate_contact(
        self, *, AlternateContactType: AlternateContactTypeType, AccountId: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified alternate contact from an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account.html#Account.Client.delete_alternate_contact)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account/client/#delete_alternate_contact)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account.html#Account.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account/client/#generate_presigned_url)
        """

    def get_alternate_contact(
        self, *, AlternateContactType: AlternateContactTypeType, AccountId: str = ...
    ) -> GetAlternateContactResponseTypeDef:
        """
        Retrieves the specified alternate contact attached to an Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account.html#Account.Client.get_alternate_contact)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account/client/#get_alternate_contact)
        """

    def put_alternate_contact(
        self,
        *,
        AlternateContactType: AlternateContactTypeType,
        EmailAddress: str,
        Name: str,
        PhoneNumber: str,
        Title: str,
        AccountId: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies the specified alternate contact attached to an Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account.html#Account.Client.put_alternate_contact)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account/client/#put_alternate_contact)
        """
