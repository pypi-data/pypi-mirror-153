"""
Type annotations for wellarchitected service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_wellarchitected.client import WellArchitectedClient

    session = Session()
    client: WellArchitectedClient = session.client("wellarchitected")
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import (
    AnswerReasonType,
    LensStatusTypeType,
    LensTypeType,
    PermissionTypeType,
    ShareInvitationActionType,
    ShareResourceTypeType,
    WorkloadEnvironmentType,
    WorkloadImprovementStatusType,
)
from .type_defs import (
    ChoiceUpdateTypeDef,
    CreateLensShareOutputTypeDef,
    CreateLensVersionOutputTypeDef,
    CreateMilestoneOutputTypeDef,
    CreateWorkloadOutputTypeDef,
    CreateWorkloadShareOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportLensOutputTypeDef,
    GetAnswerOutputTypeDef,
    GetLensOutputTypeDef,
    GetLensReviewOutputTypeDef,
    GetLensReviewReportOutputTypeDef,
    GetLensVersionDifferenceOutputTypeDef,
    GetMilestoneOutputTypeDef,
    GetWorkloadOutputTypeDef,
    ImportLensOutputTypeDef,
    ListAnswersOutputTypeDef,
    ListLensesOutputTypeDef,
    ListLensReviewImprovementsOutputTypeDef,
    ListLensReviewsOutputTypeDef,
    ListLensSharesOutputTypeDef,
    ListMilestonesOutputTypeDef,
    ListNotificationsOutputTypeDef,
    ListShareInvitationsOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListWorkloadSharesOutputTypeDef,
    ListWorkloadsOutputTypeDef,
    UpdateAnswerOutputTypeDef,
    UpdateLensReviewOutputTypeDef,
    UpdateShareInvitationOutputTypeDef,
    UpdateWorkloadOutputTypeDef,
    UpdateWorkloadShareOutputTypeDef,
)

__all__ = ("WellArchitectedClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class WellArchitectedClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WellArchitectedClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#exceptions)
        """

    def associate_lenses(
        self, *, WorkloadId: str, LensAliases: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associate a lens to a workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.associate_lenses)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#associate_lenses)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#can_paginate)
        """

    def create_lens_share(
        self, *, LensAlias: str, SharedWith: str, ClientRequestToken: str
    ) -> CreateLensShareOutputTypeDef:
        """
        Create a lens share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.create_lens_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#create_lens_share)
        """

    def create_lens_version(
        self,
        *,
        LensAlias: str,
        LensVersion: str,
        ClientRequestToken: str,
        IsMajorVersion: bool = ...
    ) -> CreateLensVersionOutputTypeDef:
        """
        Create a new lens version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.create_lens_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#create_lens_version)
        """

    def create_milestone(
        self, *, WorkloadId: str, MilestoneName: str, ClientRequestToken: str
    ) -> CreateMilestoneOutputTypeDef:
        """
        Create a milestone for an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.create_milestone)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#create_milestone)
        """

    def create_workload(
        self,
        *,
        WorkloadName: str,
        Description: str,
        Environment: WorkloadEnvironmentType,
        ReviewOwner: str,
        Lenses: Sequence[str],
        ClientRequestToken: str,
        AccountIds: Sequence[str] = ...,
        AwsRegions: Sequence[str] = ...,
        NonAwsRegions: Sequence[str] = ...,
        PillarPriorities: Sequence[str] = ...,
        ArchitecturalDesign: str = ...,
        IndustryType: str = ...,
        Industry: str = ...,
        Notes: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateWorkloadOutputTypeDef:
        """
        Create a new workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.create_workload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#create_workload)
        """

    def create_workload_share(
        self,
        *,
        WorkloadId: str,
        SharedWith: str,
        PermissionType: PermissionTypeType,
        ClientRequestToken: str
    ) -> CreateWorkloadShareOutputTypeDef:
        """
        Create a workload share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.create_workload_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#create_workload_share)
        """

    def delete_lens(
        self, *, LensAlias: str, ClientRequestToken: str, LensStatus: LensStatusTypeType
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete an existing lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.delete_lens)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#delete_lens)
        """

    def delete_lens_share(
        self, *, ShareId: str, LensAlias: str, ClientRequestToken: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a lens share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.delete_lens_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#delete_lens_share)
        """

    def delete_workload(
        self, *, WorkloadId: str, ClientRequestToken: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.delete_workload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#delete_workload)
        """

    def delete_workload_share(
        self, *, ShareId: str, WorkloadId: str, ClientRequestToken: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a workload share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.delete_workload_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#delete_workload_share)
        """

    def disassociate_lenses(
        self, *, WorkloadId: str, LensAliases: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociate a lens from a workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.disassociate_lenses)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#disassociate_lenses)
        """

    def export_lens(self, *, LensAlias: str, LensVersion: str = ...) -> ExportLensOutputTypeDef:
        """
        Export an existing lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.export_lens)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#export_lens)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#generate_presigned_url)
        """

    def get_answer(
        self, *, WorkloadId: str, LensAlias: str, QuestionId: str, MilestoneNumber: int = ...
    ) -> GetAnswerOutputTypeDef:
        """
        Get the answer to a specific question in a workload review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_answer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#get_answer)
        """

    def get_lens(self, *, LensAlias: str, LensVersion: str = ...) -> GetLensOutputTypeDef:
        """
        Get an existing lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_lens)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#get_lens)
        """

    def get_lens_review(
        self, *, WorkloadId: str, LensAlias: str, MilestoneNumber: int = ...
    ) -> GetLensReviewOutputTypeDef:
        """
        Get lens review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_lens_review)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#get_lens_review)
        """

    def get_lens_review_report(
        self, *, WorkloadId: str, LensAlias: str, MilestoneNumber: int = ...
    ) -> GetLensReviewReportOutputTypeDef:
        """
        Get lens review report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_lens_review_report)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#get_lens_review_report)
        """

    def get_lens_version_difference(
        self, *, LensAlias: str, BaseLensVersion: str = ..., TargetLensVersion: str = ...
    ) -> GetLensVersionDifferenceOutputTypeDef:
        """
        Get lens version differences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_lens_version_difference)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#get_lens_version_difference)
        """

    def get_milestone(self, *, WorkloadId: str, MilestoneNumber: int) -> GetMilestoneOutputTypeDef:
        """
        Get a milestone for an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_milestone)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#get_milestone)
        """

    def get_workload(self, *, WorkloadId: str) -> GetWorkloadOutputTypeDef:
        """
        Get an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_workload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#get_workload)
        """

    def import_lens(
        self,
        *,
        JSONString: str,
        ClientRequestToken: str,
        LensAlias: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> ImportLensOutputTypeDef:
        """
        Import a new lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.import_lens)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#import_lens)
        """

    def list_answers(
        self,
        *,
        WorkloadId: str,
        LensAlias: str,
        PillarId: str = ...,
        MilestoneNumber: int = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListAnswersOutputTypeDef:
        """
        List of answers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_answers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#list_answers)
        """

    def list_lens_review_improvements(
        self,
        *,
        WorkloadId: str,
        LensAlias: str,
        PillarId: str = ...,
        MilestoneNumber: int = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListLensReviewImprovementsOutputTypeDef:
        """
        List lens review improvements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_lens_review_improvements)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#list_lens_review_improvements)
        """

    def list_lens_reviews(
        self,
        *,
        WorkloadId: str,
        MilestoneNumber: int = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListLensReviewsOutputTypeDef:
        """
        List lens reviews.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_lens_reviews)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#list_lens_reviews)
        """

    def list_lens_shares(
        self,
        *,
        LensAlias: str,
        SharedWithPrefix: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListLensSharesOutputTypeDef:
        """
        List the lens shares associated with the lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_lens_shares)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#list_lens_shares)
        """

    def list_lenses(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        LensType: LensTypeType = ...,
        LensStatus: LensStatusTypeType = ...,
        LensName: str = ...
    ) -> ListLensesOutputTypeDef:
        """
        List the available lenses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_lenses)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#list_lenses)
        """

    def list_milestones(
        self, *, WorkloadId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMilestonesOutputTypeDef:
        """
        List all milestones for an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_milestones)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#list_milestones)
        """

    def list_notifications(
        self, *, WorkloadId: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListNotificationsOutputTypeDef:
        """
        List lens notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_notifications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#list_notifications)
        """

    def list_share_invitations(
        self,
        *,
        WorkloadNamePrefix: str = ...,
        LensNamePrefix: str = ...,
        ShareResourceType: ShareResourceTypeType = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListShareInvitationsOutputTypeDef:
        """
        List the workload invitations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_share_invitations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#list_share_invitations)
        """

    def list_tags_for_resource(self, *, WorkloadArn: str) -> ListTagsForResourceOutputTypeDef:
        """
        List the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#list_tags_for_resource)
        """

    def list_workload_shares(
        self,
        *,
        WorkloadId: str,
        SharedWithPrefix: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListWorkloadSharesOutputTypeDef:
        """
        List the workload shares associated with the workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_workload_shares)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#list_workload_shares)
        """

    def list_workloads(
        self, *, WorkloadNamePrefix: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListWorkloadsOutputTypeDef:
        """
        List workloads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_workloads)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#list_workloads)
        """

    def tag_resource(self, *, WorkloadArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds one or more tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#tag_resource)
        """

    def untag_resource(self, *, WorkloadArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#untag_resource)
        """

    def update_answer(
        self,
        *,
        WorkloadId: str,
        LensAlias: str,
        QuestionId: str,
        SelectedChoices: Sequence[str] = ...,
        ChoiceUpdates: Mapping[str, ChoiceUpdateTypeDef] = ...,
        Notes: str = ...,
        IsApplicable: bool = ...,
        Reason: AnswerReasonType = ...
    ) -> UpdateAnswerOutputTypeDef:
        """
        Update the answer to a specific question in a workload review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_answer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#update_answer)
        """

    def update_lens_review(
        self,
        *,
        WorkloadId: str,
        LensAlias: str,
        LensNotes: str = ...,
        PillarNotes: Mapping[str, str] = ...
    ) -> UpdateLensReviewOutputTypeDef:
        """
        Update lens review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_lens_review)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#update_lens_review)
        """

    def update_share_invitation(
        self, *, ShareInvitationId: str, ShareInvitationAction: ShareInvitationActionType
    ) -> UpdateShareInvitationOutputTypeDef:
        """
        Update a workload invitation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_share_invitation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#update_share_invitation)
        """

    def update_workload(
        self,
        *,
        WorkloadId: str,
        WorkloadName: str = ...,
        Description: str = ...,
        Environment: WorkloadEnvironmentType = ...,
        AccountIds: Sequence[str] = ...,
        AwsRegions: Sequence[str] = ...,
        NonAwsRegions: Sequence[str] = ...,
        PillarPriorities: Sequence[str] = ...,
        ArchitecturalDesign: str = ...,
        ReviewOwner: str = ...,
        IsReviewOwnerUpdateAcknowledged: bool = ...,
        IndustryType: str = ...,
        Industry: str = ...,
        Notes: str = ...,
        ImprovementStatus: WorkloadImprovementStatusType = ...
    ) -> UpdateWorkloadOutputTypeDef:
        """
        Update an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_workload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#update_workload)
        """

    def update_workload_share(
        self, *, ShareId: str, WorkloadId: str, PermissionType: PermissionTypeType
    ) -> UpdateWorkloadShareOutputTypeDef:
        """
        Update a workload share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_workload_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#update_workload_share)
        """

    def upgrade_lens_review(
        self, *, WorkloadId: str, LensAlias: str, MilestoneName: str, ClientRequestToken: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Upgrade lens review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.upgrade_lens_review)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/client/#upgrade_lens_review)
        """
