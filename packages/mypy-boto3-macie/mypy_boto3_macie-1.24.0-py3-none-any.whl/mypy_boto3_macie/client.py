"""
Type annotations for macie service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_macie.client import MacieClient

    session = Session()
    client: MacieClient = session.client("macie")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListMemberAccountsPaginator, ListS3ResourcesPaginator
from .type_defs import (
    AssociateS3ResourcesResultTypeDef,
    DisassociateS3ResourcesResultTypeDef,
    EmptyResponseMetadataTypeDef,
    ListMemberAccountsResultTypeDef,
    ListS3ResourcesResultTypeDef,
    S3ResourceClassificationTypeDef,
    S3ResourceClassificationUpdateTypeDef,
    S3ResourceTypeDef,
    UpdateS3ResourcesResultTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MacieClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]


class MacieClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MacieClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie/client/#exceptions)
        """

    def associate_member_account(self, *, memberAccountId: str) -> EmptyResponseMetadataTypeDef:
        """
        (Discontinued) Associates a specified Amazon Web Services account with Amazon
        Macie Classic as a member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.associate_member_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie/client/#associate_member_account)
        """

    def associate_s3_resources(
        self, *, s3Resources: Sequence[S3ResourceClassificationTypeDef], memberAccountId: str = ...
    ) -> AssociateS3ResourcesResultTypeDef:
        """
        (Discontinued) Associates specified S3 resources with Amazon Macie Classic for
        monitoring and data classification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.associate_s3_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie/client/#associate_s3_resources)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie/client/#can_paginate)
        """

    def disassociate_member_account(self, *, memberAccountId: str) -> EmptyResponseMetadataTypeDef:
        """
        (Discontinued) Removes the specified member account from Amazon Macie Classic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.disassociate_member_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie/client/#disassociate_member_account)
        """

    def disassociate_s3_resources(
        self, *, associatedS3Resources: Sequence[S3ResourceTypeDef], memberAccountId: str = ...
    ) -> DisassociateS3ResourcesResultTypeDef:
        """
        (Discontinued) Removes specified S3 resources from being monitored by Amazon
        Macie Classic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.disassociate_s3_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie/client/#disassociate_s3_resources)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie/client/#generate_presigned_url)
        """

    def list_member_accounts(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListMemberAccountsResultTypeDef:
        """
        (Discontinued) Lists all Amazon Macie Classic member accounts for the current
        Macie Classic administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.list_member_accounts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie/client/#list_member_accounts)
        """

    def list_s3_resources(
        self, *, memberAccountId: str = ..., nextToken: str = ..., maxResults: int = ...
    ) -> ListS3ResourcesResultTypeDef:
        """
        (Discontinued) Lists all the S3 resources associated with Amazon Macie Classic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.list_s3_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie/client/#list_s3_resources)
        """

    def update_s3_resources(
        self,
        *,
        s3ResourcesUpdate: Sequence[S3ResourceClassificationUpdateTypeDef],
        memberAccountId: str = ...
    ) -> UpdateS3ResourcesResultTypeDef:
        """
        (Discontinued) Updates the classification types for the specified S3 resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.update_s3_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie/client/#update_s3_resources)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_member_accounts"]
    ) -> ListMemberAccountsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_s3_resources"]
    ) -> ListS3ResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_macie/client/#get_paginator)
        """
