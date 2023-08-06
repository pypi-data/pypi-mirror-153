"""
Type annotations for support service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_support.client import SupportClient

    session = Session()
    client: SupportClient = session.client("support")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import DescribeCasesPaginator, DescribeCommunicationsPaginator
from .type_defs import (
    AddAttachmentsToSetResponseTypeDef,
    AddCommunicationToCaseResponseTypeDef,
    AttachmentTypeDef,
    CreateCaseResponseTypeDef,
    DescribeAttachmentResponseTypeDef,
    DescribeCasesResponseTypeDef,
    DescribeCommunicationsResponseTypeDef,
    DescribeServicesResponseTypeDef,
    DescribeSeverityLevelsResponseTypeDef,
    DescribeTrustedAdvisorCheckRefreshStatusesResponseTypeDef,
    DescribeTrustedAdvisorCheckResultResponseTypeDef,
    DescribeTrustedAdvisorChecksResponseTypeDef,
    DescribeTrustedAdvisorCheckSummariesResponseTypeDef,
    RefreshTrustedAdvisorCheckResponseTypeDef,
    ResolveCaseResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("SupportClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AttachmentIdNotFound: Type[BotocoreClientError]
    AttachmentLimitExceeded: Type[BotocoreClientError]
    AttachmentSetExpired: Type[BotocoreClientError]
    AttachmentSetIdNotFound: Type[BotocoreClientError]
    AttachmentSetSizeLimitExceeded: Type[BotocoreClientError]
    CaseCreationLimitExceeded: Type[BotocoreClientError]
    CaseIdNotFound: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DescribeAttachmentLimitExceeded: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]


class SupportClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SupportClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#exceptions)
        """

    def add_attachments_to_set(
        self, *, attachments: Sequence[AttachmentTypeDef], attachmentSetId: str = ...
    ) -> AddAttachmentsToSetResponseTypeDef:
        """
        Adds one or more attachments to an attachment set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.add_attachments_to_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#add_attachments_to_set)
        """

    def add_communication_to_case(
        self,
        *,
        communicationBody: str,
        caseId: str = ...,
        ccEmailAddresses: Sequence[str] = ...,
        attachmentSetId: str = ...
    ) -> AddCommunicationToCaseResponseTypeDef:
        """
        Adds additional customer communication to an Amazon Web Services Support case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.add_communication_to_case)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#add_communication_to_case)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#can_paginate)
        """

    def create_case(
        self,
        *,
        subject: str,
        communicationBody: str,
        serviceCode: str = ...,
        severityCode: str = ...,
        categoryCode: str = ...,
        ccEmailAddresses: Sequence[str] = ...,
        language: str = ...,
        issueType: str = ...,
        attachmentSetId: str = ...
    ) -> CreateCaseResponseTypeDef:
        """
        Creates a case in the Amazon Web Services Support Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.create_case)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#create_case)
        """

    def describe_attachment(self, *, attachmentId: str) -> DescribeAttachmentResponseTypeDef:
        """
        Returns the attachment that has the specified ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_attachment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#describe_attachment)
        """

    def describe_cases(
        self,
        *,
        caseIdList: Sequence[str] = ...,
        displayId: str = ...,
        afterTime: str = ...,
        beforeTime: str = ...,
        includeResolvedCases: bool = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        language: str = ...,
        includeCommunications: bool = ...
    ) -> DescribeCasesResponseTypeDef:
        """
        Returns a list of cases that you specify by passing one or more case IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_cases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#describe_cases)
        """

    def describe_communications(
        self,
        *,
        caseId: str,
        beforeTime: str = ...,
        afterTime: str = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> DescribeCommunicationsResponseTypeDef:
        """
        Returns communications and attachments for one or more support cases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_communications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#describe_communications)
        """

    def describe_services(
        self, *, serviceCodeList: Sequence[str] = ..., language: str = ...
    ) -> DescribeServicesResponseTypeDef:
        """
        Returns the current list of Amazon Web Services services and a list of service
        categories for each service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_services)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#describe_services)
        """

    def describe_severity_levels(
        self, *, language: str = ...
    ) -> DescribeSeverityLevelsResponseTypeDef:
        """
        Returns the list of severity levels that you can assign to a support case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_severity_levels)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#describe_severity_levels)
        """

    def describe_trusted_advisor_check_refresh_statuses(
        self, *, checkIds: Sequence[str]
    ) -> DescribeTrustedAdvisorCheckRefreshStatusesResponseTypeDef:
        """
        Returns the refresh status of the Trusted Advisor checks that have the specified
        check IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_trusted_advisor_check_refresh_statuses)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#describe_trusted_advisor_check_refresh_statuses)
        """

    def describe_trusted_advisor_check_result(
        self, *, checkId: str, language: str = ...
    ) -> DescribeTrustedAdvisorCheckResultResponseTypeDef:
        """
        Returns the results of the Trusted Advisor check that has the specified check
        ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_trusted_advisor_check_result)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#describe_trusted_advisor_check_result)
        """

    def describe_trusted_advisor_check_summaries(
        self, *, checkIds: Sequence[str]
    ) -> DescribeTrustedAdvisorCheckSummariesResponseTypeDef:
        """
        Returns the results for the Trusted Advisor check summaries for the check IDs
        that you specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_trusted_advisor_check_summaries)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#describe_trusted_advisor_check_summaries)
        """

    def describe_trusted_advisor_checks(
        self, *, language: str
    ) -> DescribeTrustedAdvisorChecksResponseTypeDef:
        """
        Returns information about all available Trusted Advisor checks, including the
        name, ID, category, description, and metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_trusted_advisor_checks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#describe_trusted_advisor_checks)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#generate_presigned_url)
        """

    def refresh_trusted_advisor_check(
        self, *, checkId: str
    ) -> RefreshTrustedAdvisorCheckResponseTypeDef:
        """
        Refreshes the Trusted Advisor check that you specify using the check ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.refresh_trusted_advisor_check)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#refresh_trusted_advisor_check)
        """

    def resolve_case(self, *, caseId: str = ...) -> ResolveCaseResponseTypeDef:
        """
        Resolves a support case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.resolve_case)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#resolve_case)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_cases"]) -> DescribeCasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_communications"]
    ) -> DescribeCommunicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/client/#get_paginator)
        """
