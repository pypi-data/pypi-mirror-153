"""
Type annotations for mturk service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_mturk.client import MTurkClient

    session = Session()
    client: MTurkClient = session.client("mturk")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    AssignmentStatusType,
    EventTypeType,
    QualificationStatusType,
    QualificationTypeStatusType,
    ReviewableHITStatusType,
    ReviewPolicyLevelType,
)
from .paginator import (
    ListAssignmentsForHITPaginator,
    ListBonusPaymentsPaginator,
    ListHITsForQualificationTypePaginator,
    ListHITsPaginator,
    ListQualificationRequestsPaginator,
    ListQualificationTypesPaginator,
    ListReviewableHITsPaginator,
    ListWorkerBlocksPaginator,
    ListWorkersWithQualificationTypePaginator,
)
from .type_defs import (
    CreateHITResponseTypeDef,
    CreateHITTypeResponseTypeDef,
    CreateHITWithHITTypeResponseTypeDef,
    CreateQualificationTypeResponseTypeDef,
    GetAccountBalanceResponseTypeDef,
    GetAssignmentResponseTypeDef,
    GetFileUploadURLResponseTypeDef,
    GetHITResponseTypeDef,
    GetQualificationScoreResponseTypeDef,
    GetQualificationTypeResponseTypeDef,
    HITLayoutParameterTypeDef,
    ListAssignmentsForHITResponseTypeDef,
    ListBonusPaymentsResponseTypeDef,
    ListHITsForQualificationTypeResponseTypeDef,
    ListHITsResponseTypeDef,
    ListQualificationRequestsResponseTypeDef,
    ListQualificationTypesResponseTypeDef,
    ListReviewableHITsResponseTypeDef,
    ListReviewPolicyResultsForHITResponseTypeDef,
    ListWorkerBlocksResponseTypeDef,
    ListWorkersWithQualificationTypeResponseTypeDef,
    NotificationSpecificationTypeDef,
    NotifyWorkersResponseTypeDef,
    QualificationRequirementTypeDef,
    ReviewPolicyTypeDef,
    UpdateQualificationTypeResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MTurkClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    RequestError: Type[BotocoreClientError]
    ServiceFault: Type[BotocoreClientError]


class MTurkClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MTurkClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#exceptions)
        """

    def accept_qualification_request(
        self, *, QualificationRequestId: str, IntegerValue: int = ...
    ) -> Dict[str, Any]:
        """
        The `AcceptQualificationRequest` operation approves a Worker's request for a
        Qualification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.accept_qualification_request)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#accept_qualification_request)
        """

    def approve_assignment(
        self, *, AssignmentId: str, RequesterFeedback: str = ..., OverrideRejection: bool = ...
    ) -> Dict[str, Any]:
        """
        The `ApproveAssignment` operation approves the results of a completed
        assignment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.approve_assignment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#approve_assignment)
        """

    def associate_qualification_with_worker(
        self,
        *,
        QualificationTypeId: str,
        WorkerId: str,
        IntegerValue: int = ...,
        SendNotification: bool = ...
    ) -> Dict[str, Any]:
        """
        The `AssociateQualificationWithWorker` operation gives a Worker a Qualification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.associate_qualification_with_worker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#associate_qualification_with_worker)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#can_paginate)
        """

    def create_additional_assignments_for_hit(
        self, *, HITId: str, NumberOfAdditionalAssignments: int, UniqueRequestToken: str = ...
    ) -> Dict[str, Any]:
        """
        The `CreateAdditionalAssignmentsForHIT` operation increases the maximum number
        of assignments of an existing HIT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.create_additional_assignments_for_hit)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#create_additional_assignments_for_hit)
        """

    def create_hit(
        self,
        *,
        LifetimeInSeconds: int,
        AssignmentDurationInSeconds: int,
        Reward: str,
        Title: str,
        Description: str,
        MaxAssignments: int = ...,
        AutoApprovalDelayInSeconds: int = ...,
        Keywords: str = ...,
        Question: str = ...,
        RequesterAnnotation: str = ...,
        QualificationRequirements: Sequence[QualificationRequirementTypeDef] = ...,
        UniqueRequestToken: str = ...,
        AssignmentReviewPolicy: ReviewPolicyTypeDef = ...,
        HITReviewPolicy: ReviewPolicyTypeDef = ...,
        HITLayoutId: str = ...,
        HITLayoutParameters: Sequence[HITLayoutParameterTypeDef] = ...
    ) -> CreateHITResponseTypeDef:
        """
        The `CreateHIT` operation creates a new Human Intelligence Task (HIT).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.create_hit)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#create_hit)
        """

    def create_hit_type(
        self,
        *,
        AssignmentDurationInSeconds: int,
        Reward: str,
        Title: str,
        Description: str,
        AutoApprovalDelayInSeconds: int = ...,
        Keywords: str = ...,
        QualificationRequirements: Sequence[QualificationRequirementTypeDef] = ...
    ) -> CreateHITTypeResponseTypeDef:
        """
        The `CreateHITType` operation creates a new HIT type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.create_hit_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#create_hit_type)
        """

    def create_hit_with_hit_type(
        self,
        *,
        HITTypeId: str,
        LifetimeInSeconds: int,
        MaxAssignments: int = ...,
        Question: str = ...,
        RequesterAnnotation: str = ...,
        UniqueRequestToken: str = ...,
        AssignmentReviewPolicy: ReviewPolicyTypeDef = ...,
        HITReviewPolicy: ReviewPolicyTypeDef = ...,
        HITLayoutId: str = ...,
        HITLayoutParameters: Sequence[HITLayoutParameterTypeDef] = ...
    ) -> CreateHITWithHITTypeResponseTypeDef:
        """
        The `CreateHITWithHITType` operation creates a new Human Intelligence Task (HIT)
        using an existing HITTypeID generated by the `CreateHITType` operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.create_hit_with_hit_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#create_hit_with_hit_type)
        """

    def create_qualification_type(
        self,
        *,
        Name: str,
        Description: str,
        QualificationTypeStatus: QualificationTypeStatusType,
        Keywords: str = ...,
        RetryDelayInSeconds: int = ...,
        Test: str = ...,
        AnswerKey: str = ...,
        TestDurationInSeconds: int = ...,
        AutoGranted: bool = ...,
        AutoGrantedValue: int = ...
    ) -> CreateQualificationTypeResponseTypeDef:
        """
        The `CreateQualificationType` operation creates a new Qualification type, which
        is represented by a `QualificationType` data structure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.create_qualification_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#create_qualification_type)
        """

    def create_worker_block(self, *, WorkerId: str, Reason: str) -> Dict[str, Any]:
        """
        The `CreateWorkerBlock` operation allows you to prevent a Worker from working on
        your HITs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.create_worker_block)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#create_worker_block)
        """

    def delete_hit(self, *, HITId: str) -> Dict[str, Any]:
        """
        The `DeleteHIT` operation is used to delete HIT that is no longer needed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.delete_hit)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#delete_hit)
        """

    def delete_qualification_type(self, *, QualificationTypeId: str) -> Dict[str, Any]:
        """
        The `DeleteQualificationType` deletes a Qualification type and deletes any HIT
        types that are associated with the Qualification type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.delete_qualification_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#delete_qualification_type)
        """

    def delete_worker_block(self, *, WorkerId: str, Reason: str = ...) -> Dict[str, Any]:
        """
        The `DeleteWorkerBlock` operation allows you to reinstate a blocked Worker to
        work on your HITs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.delete_worker_block)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#delete_worker_block)
        """

    def disassociate_qualification_from_worker(
        self, *, WorkerId: str, QualificationTypeId: str, Reason: str = ...
    ) -> Dict[str, Any]:
        """
        The `DisassociateQualificationFromWorker` revokes a previously granted
        Qualification from a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.disassociate_qualification_from_worker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#disassociate_qualification_from_worker)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#generate_presigned_url)
        """

    def get_account_balance(self) -> GetAccountBalanceResponseTypeDef:
        """
        The `GetAccountBalance` operation retrieves the Prepaid HITs balance in your
        Amazon Mechanical Turk account if you are a Prepaid Requester.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.get_account_balance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#get_account_balance)
        """

    def get_assignment(self, *, AssignmentId: str) -> GetAssignmentResponseTypeDef:
        """
        The `GetAssignment` operation retrieves the details of the specified Assignment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.get_assignment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#get_assignment)
        """

    def get_file_upload_url(
        self, *, AssignmentId: str, QuestionIdentifier: str
    ) -> GetFileUploadURLResponseTypeDef:
        """
        The `GetFileUploadURL` operation generates and returns a temporary URL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.get_file_upload_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#get_file_upload_url)
        """

    def get_hit(self, *, HITId: str) -> GetHITResponseTypeDef:
        """
        The `GetHIT` operation retrieves the details of the specified HIT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.get_hit)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#get_hit)
        """

    def get_qualification_score(
        self, *, QualificationTypeId: str, WorkerId: str
    ) -> GetQualificationScoreResponseTypeDef:
        """
        The `GetQualificationScore` operation returns the value of a Worker's
        Qualification for a given Qualification type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.get_qualification_score)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#get_qualification_score)
        """

    def get_qualification_type(
        self, *, QualificationTypeId: str
    ) -> GetQualificationTypeResponseTypeDef:
        """
        The `GetQualificationType` operation retrieves information about a Qualification
        type using its ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.get_qualification_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#get_qualification_type)
        """

    def list_assignments_for_hit(
        self,
        *,
        HITId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        AssignmentStatuses: Sequence[AssignmentStatusType] = ...
    ) -> ListAssignmentsForHITResponseTypeDef:
        """
        The `ListAssignmentsForHIT` operation retrieves completed assignments for a HIT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.list_assignments_for_hit)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#list_assignments_for_hit)
        """

    def list_bonus_payments(
        self,
        *,
        HITId: str = ...,
        AssignmentId: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListBonusPaymentsResponseTypeDef:
        """
        The `ListBonusPayments` operation retrieves the amounts of bonuses you have paid
        to Workers for a given HIT or assignment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.list_bonus_payments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#list_bonus_payments)
        """

    def list_hits(self, *, NextToken: str = ..., MaxResults: int = ...) -> ListHITsResponseTypeDef:
        """
        The `ListHITs` operation returns all of a Requester's HITs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.list_hits)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#list_hits)
        """

    def list_hits_for_qualification_type(
        self, *, QualificationTypeId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListHITsForQualificationTypeResponseTypeDef:
        """
        The `ListHITsForQualificationType` operation returns the HITs that use the given
        Qualification type for a Qualification requirement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.list_hits_for_qualification_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#list_hits_for_qualification_type)
        """

    def list_qualification_requests(
        self, *, QualificationTypeId: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListQualificationRequestsResponseTypeDef:
        """
        The `ListQualificationRequests` operation retrieves requests for Qualifications
        of a particular Qualification type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.list_qualification_requests)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#list_qualification_requests)
        """

    def list_qualification_types(
        self,
        *,
        MustBeRequestable: bool,
        Query: str = ...,
        MustBeOwnedByCaller: bool = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListQualificationTypesResponseTypeDef:
        """
        The `ListQualificationTypes` operation returns a list of Qualification types,
        filtered by an optional search term.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.list_qualification_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#list_qualification_types)
        """

    def list_review_policy_results_for_hit(
        self,
        *,
        HITId: str,
        PolicyLevels: Sequence[ReviewPolicyLevelType] = ...,
        RetrieveActions: bool = ...,
        RetrieveResults: bool = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListReviewPolicyResultsForHITResponseTypeDef:
        """
        The `ListReviewPolicyResultsForHIT` operation retrieves the computed results and
        the actions taken in the course of executing your Review Policies for a given
        HIT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.list_review_policy_results_for_hit)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#list_review_policy_results_for_hit)
        """

    def list_reviewable_hits(
        self,
        *,
        HITTypeId: str = ...,
        Status: ReviewableHITStatusType = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListReviewableHITsResponseTypeDef:
        """
        The `ListReviewableHITs` operation retrieves the HITs with Status equal to
        Reviewable or Status equal to Reviewing that belong to the Requester calling the
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.list_reviewable_hits)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#list_reviewable_hits)
        """

    def list_worker_blocks(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListWorkerBlocksResponseTypeDef:
        """
        The `ListWorkersBlocks` operation retrieves a list of Workers who are blocked
        from working on your HITs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.list_worker_blocks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#list_worker_blocks)
        """

    def list_workers_with_qualification_type(
        self,
        *,
        QualificationTypeId: str,
        Status: QualificationStatusType = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListWorkersWithQualificationTypeResponseTypeDef:
        """
        The `ListWorkersWithQualificationType` operation returns all of the Workers that
        have been associated with a given Qualification type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.list_workers_with_qualification_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#list_workers_with_qualification_type)
        """

    def notify_workers(
        self, *, Subject: str, MessageText: str, WorkerIds: Sequence[str]
    ) -> NotifyWorkersResponseTypeDef:
        """
        The `NotifyWorkers` operation sends an email to one or more Workers that you
        specify with the Worker ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.notify_workers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#notify_workers)
        """

    def reject_assignment(self, *, AssignmentId: str, RequesterFeedback: str) -> Dict[str, Any]:
        """
        The `RejectAssignment` operation rejects the results of a completed assignment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.reject_assignment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#reject_assignment)
        """

    def reject_qualification_request(
        self, *, QualificationRequestId: str, Reason: str = ...
    ) -> Dict[str, Any]:
        """
        The `RejectQualificationRequest` operation rejects a user's request for a
        Qualification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.reject_qualification_request)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#reject_qualification_request)
        """

    def send_bonus(
        self,
        *,
        WorkerId: str,
        BonusAmount: str,
        AssignmentId: str,
        Reason: str,
        UniqueRequestToken: str = ...
    ) -> Dict[str, Any]:
        """
        The `SendBonus` operation issues a payment of money from your account to a
        Worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.send_bonus)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#send_bonus)
        """

    def send_test_event_notification(
        self, *, Notification: NotificationSpecificationTypeDef, TestEventType: EventTypeType
    ) -> Dict[str, Any]:
        """
        The `SendTestEventNotification` operation causes Amazon Mechanical Turk to send
        a notification message as if a HIT event occurred, according to the provided
        notification specification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.send_test_event_notification)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#send_test_event_notification)
        """

    def update_expiration_for_hit(
        self, *, HITId: str, ExpireAt: Union[datetime, str]
    ) -> Dict[str, Any]:
        """
        The `UpdateExpirationForHIT` operation allows you update the expiration time of
        a HIT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.update_expiration_for_hit)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#update_expiration_for_hit)
        """

    def update_hit_review_status(self, *, HITId: str, Revert: bool = ...) -> Dict[str, Any]:
        """
        The `UpdateHITReviewStatus` operation updates the status of a HIT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.update_hit_review_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#update_hit_review_status)
        """

    def update_hit_type_of_hit(self, *, HITId: str, HITTypeId: str) -> Dict[str, Any]:
        """
        The `UpdateHITTypeOfHIT` operation allows you to change the HITType properties
        of a HIT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.update_hit_type_of_hit)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#update_hit_type_of_hit)
        """

    def update_notification_settings(
        self,
        *,
        HITTypeId: str,
        Notification: NotificationSpecificationTypeDef = ...,
        Active: bool = ...
    ) -> Dict[str, Any]:
        """
        The `UpdateNotificationSettings` operation creates, updates, disables or re-
        enables notifications for a HIT type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.update_notification_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#update_notification_settings)
        """

    def update_qualification_type(
        self,
        *,
        QualificationTypeId: str,
        Description: str = ...,
        QualificationTypeStatus: QualificationTypeStatusType = ...,
        Test: str = ...,
        AnswerKey: str = ...,
        TestDurationInSeconds: int = ...,
        RetryDelayInSeconds: int = ...,
        AutoGranted: bool = ...,
        AutoGrantedValue: int = ...
    ) -> UpdateQualificationTypeResponseTypeDef:
        """
        The `UpdateQualificationType` operation modifies the attributes of an existing
        Qualification type, which is represented by a QualificationType data structure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.update_qualification_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#update_qualification_type)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_assignments_for_hit"]
    ) -> ListAssignmentsForHITPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bonus_payments"]
    ) -> ListBonusPaymentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_hits"]) -> ListHITsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_hits_for_qualification_type"]
    ) -> ListHITsForQualificationTypePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_qualification_requests"]
    ) -> ListQualificationRequestsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_qualification_types"]
    ) -> ListQualificationTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_reviewable_hits"]
    ) -> ListReviewableHITsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_worker_blocks"]
    ) -> ListWorkerBlocksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_workers_with_qualification_type"]
    ) -> ListWorkersWithQualificationTypePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mturk/client/#get_paginator)
        """
