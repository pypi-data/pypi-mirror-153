"""
Type annotations for codecommit service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/type_defs/)

Usage::

    ```python
    from mypy_boto3_codecommit.type_defs import ApprovalRuleEventMetadataTypeDef

    data: ApprovalRuleEventMetadataTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ApprovalStateType,
    ChangeTypeEnumType,
    ConflictDetailLevelTypeEnumType,
    ConflictResolutionStrategyTypeEnumType,
    FileModeTypeEnumType,
    MergeOptionTypeEnumType,
    ObjectTypeEnumType,
    OrderEnumType,
    OverrideStatusType,
    PullRequestEventTypeType,
    PullRequestStatusEnumType,
    RelativeFileVersionEnumType,
    ReplacementTypeEnumType,
    RepositoryTriggerEventEnumType,
    SortByEnumType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ApprovalRuleEventMetadataTypeDef",
    "ApprovalRuleOverriddenEventMetadataTypeDef",
    "ApprovalRuleTemplateTypeDef",
    "OriginApprovalRuleTemplateTypeDef",
    "ApprovalStateChangedEventMetadataTypeDef",
    "ApprovalTypeDef",
    "AssociateApprovalRuleTemplateWithRepositoryInputRequestTypeDef",
    "BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef",
    "BatchAssociateApprovalRuleTemplateWithRepositoriesInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "BatchDescribeMergeConflictsErrorTypeDef",
    "BatchDescribeMergeConflictsInputRequestTypeDef",
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesErrorTypeDef",
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesInputRequestTypeDef",
    "BatchGetCommitsErrorTypeDef",
    "BatchGetCommitsInputRequestTypeDef",
    "BatchGetRepositoriesInputRequestTypeDef",
    "RepositoryMetadataTypeDef",
    "BlobMetadataTypeDef",
    "BranchInfoTypeDef",
    "CommentTypeDef",
    "LocationTypeDef",
    "UserInfoTypeDef",
    "FileModesTypeDef",
    "FileSizesTypeDef",
    "IsBinaryFileTypeDef",
    "MergeOperationsTypeDef",
    "ObjectTypesTypeDef",
    "DeleteFileEntryTypeDef",
    "ReplaceContentEntryTypeDef",
    "SetFileModeEntryTypeDef",
    "CreateApprovalRuleTemplateInputRequestTypeDef",
    "CreateBranchInputRequestTypeDef",
    "FileMetadataTypeDef",
    "CreatePullRequestApprovalRuleInputRequestTypeDef",
    "TargetTypeDef",
    "CreateRepositoryInputRequestTypeDef",
    "DeleteApprovalRuleTemplateInputRequestTypeDef",
    "DeleteBranchInputRequestTypeDef",
    "DeleteCommentContentInputRequestTypeDef",
    "DeleteFileInputRequestTypeDef",
    "DeletePullRequestApprovalRuleInputRequestTypeDef",
    "DeleteRepositoryInputRequestTypeDef",
    "DescribeMergeConflictsInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribePullRequestEventsInputRequestTypeDef",
    "DisassociateApprovalRuleTemplateFromRepositoryInputRequestTypeDef",
    "EvaluatePullRequestApprovalRulesInputRequestTypeDef",
    "EvaluationTypeDef",
    "FileTypeDef",
    "FolderTypeDef",
    "GetApprovalRuleTemplateInputRequestTypeDef",
    "GetBlobInputRequestTypeDef",
    "GetBranchInputRequestTypeDef",
    "GetCommentInputRequestTypeDef",
    "GetCommentReactionsInputRequestTypeDef",
    "GetCommentsForComparedCommitInputRequestTypeDef",
    "GetCommentsForPullRequestInputRequestTypeDef",
    "GetCommitInputRequestTypeDef",
    "GetDifferencesInputRequestTypeDef",
    "GetFileInputRequestTypeDef",
    "GetFolderInputRequestTypeDef",
    "SubModuleTypeDef",
    "SymbolicLinkTypeDef",
    "GetMergeCommitInputRequestTypeDef",
    "GetMergeConflictsInputRequestTypeDef",
    "GetMergeOptionsInputRequestTypeDef",
    "GetPullRequestApprovalStatesInputRequestTypeDef",
    "GetPullRequestInputRequestTypeDef",
    "GetPullRequestOverrideStateInputRequestTypeDef",
    "GetRepositoryInputRequestTypeDef",
    "GetRepositoryTriggersInputRequestTypeDef",
    "RepositoryTriggerTypeDef",
    "ListApprovalRuleTemplatesInputRequestTypeDef",
    "ListAssociatedApprovalRuleTemplatesForRepositoryInputRequestTypeDef",
    "ListBranchesInputRequestTypeDef",
    "ListPullRequestsInputRequestTypeDef",
    "ListRepositoriesForApprovalRuleTemplateInputRequestTypeDef",
    "ListRepositoriesInputRequestTypeDef",
    "RepositoryNameIdPairTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "MergeBranchesByFastForwardInputRequestTypeDef",
    "MergeHunkDetailTypeDef",
    "MergeMetadataTypeDef",
    "MergePullRequestByFastForwardInputRequestTypeDef",
    "OverridePullRequestApprovalRulesInputRequestTypeDef",
    "PostCommentReplyInputRequestTypeDef",
    "PullRequestCreatedEventMetadataTypeDef",
    "PullRequestSourceReferenceUpdatedEventMetadataTypeDef",
    "PullRequestStatusChangedEventMetadataTypeDef",
    "PutCommentReactionInputRequestTypeDef",
    "SourceFileSpecifierTypeDef",
    "PutFileInputRequestTypeDef",
    "ReactionValueFormatsTypeDef",
    "RepositoryTriggerExecutionFailureTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateApprovalRuleTemplateContentInputRequestTypeDef",
    "UpdateApprovalRuleTemplateDescriptionInputRequestTypeDef",
    "UpdateApprovalRuleTemplateNameInputRequestTypeDef",
    "UpdateCommentInputRequestTypeDef",
    "UpdateDefaultBranchInputRequestTypeDef",
    "UpdatePullRequestApprovalRuleContentInputRequestTypeDef",
    "UpdatePullRequestApprovalStateInputRequestTypeDef",
    "UpdatePullRequestDescriptionInputRequestTypeDef",
    "UpdatePullRequestStatusInputRequestTypeDef",
    "UpdatePullRequestTitleInputRequestTypeDef",
    "UpdateRepositoryDescriptionInputRequestTypeDef",
    "UpdateRepositoryNameInputRequestTypeDef",
    "ApprovalRuleTypeDef",
    "BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef",
    "CreateApprovalRuleTemplateOutputTypeDef",
    "CreateUnreferencedMergeCommitOutputTypeDef",
    "DeleteApprovalRuleTemplateOutputTypeDef",
    "DeleteFileOutputTypeDef",
    "DeletePullRequestApprovalRuleOutputTypeDef",
    "DeleteRepositoryOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetApprovalRuleTemplateOutputTypeDef",
    "GetBlobOutputTypeDef",
    "GetFileOutputTypeDef",
    "GetMergeCommitOutputTypeDef",
    "GetMergeOptionsOutputTypeDef",
    "GetPullRequestApprovalStatesOutputTypeDef",
    "GetPullRequestOverrideStateOutputTypeDef",
    "ListApprovalRuleTemplatesOutputTypeDef",
    "ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef",
    "ListBranchesOutputTypeDef",
    "ListPullRequestsOutputTypeDef",
    "ListRepositoriesForApprovalRuleTemplateOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "MergeBranchesByFastForwardOutputTypeDef",
    "MergeBranchesBySquashOutputTypeDef",
    "MergeBranchesByThreeWayOutputTypeDef",
    "PutFileOutputTypeDef",
    "PutRepositoryTriggersOutputTypeDef",
    "UpdateApprovalRuleTemplateContentOutputTypeDef",
    "UpdateApprovalRuleTemplateDescriptionOutputTypeDef",
    "UpdateApprovalRuleTemplateNameOutputTypeDef",
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef",
    "BatchGetRepositoriesOutputTypeDef",
    "CreateRepositoryOutputTypeDef",
    "GetRepositoryOutputTypeDef",
    "DifferenceTypeDef",
    "DeleteBranchOutputTypeDef",
    "GetBranchOutputTypeDef",
    "DeleteCommentContentOutputTypeDef",
    "GetCommentOutputTypeDef",
    "PostCommentReplyOutputTypeDef",
    "UpdateCommentOutputTypeDef",
    "CommentsForComparedCommitTypeDef",
    "CommentsForPullRequestTypeDef",
    "PostCommentForComparedCommitInputRequestTypeDef",
    "PostCommentForComparedCommitOutputTypeDef",
    "PostCommentForPullRequestInputRequestTypeDef",
    "PostCommentForPullRequestOutputTypeDef",
    "CommitTypeDef",
    "ConflictMetadataTypeDef",
    "ConflictResolutionTypeDef",
    "CreateCommitOutputTypeDef",
    "CreatePullRequestInputRequestTypeDef",
    "DescribePullRequestEventsInputDescribePullRequestEventsPaginateTypeDef",
    "GetCommentsForComparedCommitInputGetCommentsForComparedCommitPaginateTypeDef",
    "GetCommentsForPullRequestInputGetCommentsForPullRequestPaginateTypeDef",
    "GetDifferencesInputGetDifferencesPaginateTypeDef",
    "ListBranchesInputListBranchesPaginateTypeDef",
    "ListPullRequestsInputListPullRequestsPaginateTypeDef",
    "ListRepositoriesInputListRepositoriesPaginateTypeDef",
    "EvaluatePullRequestApprovalRulesOutputTypeDef",
    "GetFolderOutputTypeDef",
    "GetRepositoryTriggersOutputTypeDef",
    "PutRepositoryTriggersInputRequestTypeDef",
    "TestRepositoryTriggersInputRequestTypeDef",
    "ListRepositoriesOutputTypeDef",
    "MergeHunkTypeDef",
    "PullRequestMergedStateChangedEventMetadataTypeDef",
    "PullRequestTargetTypeDef",
    "PutFileEntryTypeDef",
    "ReactionForCommentTypeDef",
    "TestRepositoryTriggersOutputTypeDef",
    "CreatePullRequestApprovalRuleOutputTypeDef",
    "UpdatePullRequestApprovalRuleContentOutputTypeDef",
    "GetDifferencesOutputTypeDef",
    "GetCommentsForComparedCommitOutputTypeDef",
    "GetCommentsForPullRequestOutputTypeDef",
    "BatchGetCommitsOutputTypeDef",
    "GetCommitOutputTypeDef",
    "GetMergeConflictsOutputTypeDef",
    "CreateUnreferencedMergeCommitInputRequestTypeDef",
    "MergeBranchesBySquashInputRequestTypeDef",
    "MergeBranchesByThreeWayInputRequestTypeDef",
    "MergePullRequestBySquashInputRequestTypeDef",
    "MergePullRequestByThreeWayInputRequestTypeDef",
    "ConflictTypeDef",
    "DescribeMergeConflictsOutputTypeDef",
    "PullRequestEventTypeDef",
    "PullRequestTypeDef",
    "CreateCommitInputRequestTypeDef",
    "GetCommentReactionsOutputTypeDef",
    "BatchDescribeMergeConflictsOutputTypeDef",
    "DescribePullRequestEventsOutputTypeDef",
    "CreatePullRequestOutputTypeDef",
    "GetPullRequestOutputTypeDef",
    "MergePullRequestByFastForwardOutputTypeDef",
    "MergePullRequestBySquashOutputTypeDef",
    "MergePullRequestByThreeWayOutputTypeDef",
    "UpdatePullRequestDescriptionOutputTypeDef",
    "UpdatePullRequestStatusOutputTypeDef",
    "UpdatePullRequestTitleOutputTypeDef",
)

ApprovalRuleEventMetadataTypeDef = TypedDict(
    "ApprovalRuleEventMetadataTypeDef",
    {
        "approvalRuleName": str,
        "approvalRuleId": str,
        "approvalRuleContent": str,
    },
    total=False,
)

ApprovalRuleOverriddenEventMetadataTypeDef = TypedDict(
    "ApprovalRuleOverriddenEventMetadataTypeDef",
    {
        "revisionId": str,
        "overrideStatus": OverrideStatusType,
    },
    total=False,
)

ApprovalRuleTemplateTypeDef = TypedDict(
    "ApprovalRuleTemplateTypeDef",
    {
        "approvalRuleTemplateId": str,
        "approvalRuleTemplateName": str,
        "approvalRuleTemplateDescription": str,
        "approvalRuleTemplateContent": str,
        "ruleContentSha256": str,
        "lastModifiedDate": datetime,
        "creationDate": datetime,
        "lastModifiedUser": str,
    },
    total=False,
)

OriginApprovalRuleTemplateTypeDef = TypedDict(
    "OriginApprovalRuleTemplateTypeDef",
    {
        "approvalRuleTemplateId": str,
        "approvalRuleTemplateName": str,
    },
    total=False,
)

ApprovalStateChangedEventMetadataTypeDef = TypedDict(
    "ApprovalStateChangedEventMetadataTypeDef",
    {
        "revisionId": str,
        "approvalStatus": ApprovalStateType,
    },
    total=False,
)

ApprovalTypeDef = TypedDict(
    "ApprovalTypeDef",
    {
        "userArn": str,
        "approvalState": ApprovalStateType,
    },
    total=False,
)

AssociateApprovalRuleTemplateWithRepositoryInputRequestTypeDef = TypedDict(
    "AssociateApprovalRuleTemplateWithRepositoryInputRequestTypeDef",
    {
        "approvalRuleTemplateName": str,
        "repositoryName": str,
    },
)

BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef = TypedDict(
    "BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef",
    {
        "repositoryName": str,
        "errorCode": str,
        "errorMessage": str,
    },
    total=False,
)

BatchAssociateApprovalRuleTemplateWithRepositoriesInputRequestTypeDef = TypedDict(
    "BatchAssociateApprovalRuleTemplateWithRepositoriesInputRequestTypeDef",
    {
        "approvalRuleTemplateName": str,
        "repositoryNames": Sequence[str],
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

BatchDescribeMergeConflictsErrorTypeDef = TypedDict(
    "BatchDescribeMergeConflictsErrorTypeDef",
    {
        "filePath": str,
        "exceptionName": str,
        "message": str,
    },
)

_RequiredBatchDescribeMergeConflictsInputRequestTypeDef = TypedDict(
    "_RequiredBatchDescribeMergeConflictsInputRequestTypeDef",
    {
        "repositoryName": str,
        "destinationCommitSpecifier": str,
        "sourceCommitSpecifier": str,
        "mergeOption": MergeOptionTypeEnumType,
    },
)
_OptionalBatchDescribeMergeConflictsInputRequestTypeDef = TypedDict(
    "_OptionalBatchDescribeMergeConflictsInputRequestTypeDef",
    {
        "maxMergeHunks": int,
        "maxConflictFiles": int,
        "filePaths": Sequence[str],
        "conflictDetailLevel": ConflictDetailLevelTypeEnumType,
        "conflictResolutionStrategy": ConflictResolutionStrategyTypeEnumType,
        "nextToken": str,
    },
    total=False,
)


class BatchDescribeMergeConflictsInputRequestTypeDef(
    _RequiredBatchDescribeMergeConflictsInputRequestTypeDef,
    _OptionalBatchDescribeMergeConflictsInputRequestTypeDef,
):
    pass


BatchDisassociateApprovalRuleTemplateFromRepositoriesErrorTypeDef = TypedDict(
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesErrorTypeDef",
    {
        "repositoryName": str,
        "errorCode": str,
        "errorMessage": str,
    },
    total=False,
)

BatchDisassociateApprovalRuleTemplateFromRepositoriesInputRequestTypeDef = TypedDict(
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesInputRequestTypeDef",
    {
        "approvalRuleTemplateName": str,
        "repositoryNames": Sequence[str],
    },
)

BatchGetCommitsErrorTypeDef = TypedDict(
    "BatchGetCommitsErrorTypeDef",
    {
        "commitId": str,
        "errorCode": str,
        "errorMessage": str,
    },
    total=False,
)

BatchGetCommitsInputRequestTypeDef = TypedDict(
    "BatchGetCommitsInputRequestTypeDef",
    {
        "commitIds": Sequence[str],
        "repositoryName": str,
    },
)

BatchGetRepositoriesInputRequestTypeDef = TypedDict(
    "BatchGetRepositoriesInputRequestTypeDef",
    {
        "repositoryNames": Sequence[str],
    },
)

RepositoryMetadataTypeDef = TypedDict(
    "RepositoryMetadataTypeDef",
    {
        "accountId": str,
        "repositoryId": str,
        "repositoryName": str,
        "repositoryDescription": str,
        "defaultBranch": str,
        "lastModifiedDate": datetime,
        "creationDate": datetime,
        "cloneUrlHttp": str,
        "cloneUrlSsh": str,
        "Arn": str,
    },
    total=False,
)

BlobMetadataTypeDef = TypedDict(
    "BlobMetadataTypeDef",
    {
        "blobId": str,
        "path": str,
        "mode": str,
    },
    total=False,
)

BranchInfoTypeDef = TypedDict(
    "BranchInfoTypeDef",
    {
        "branchName": str,
        "commitId": str,
    },
    total=False,
)

CommentTypeDef = TypedDict(
    "CommentTypeDef",
    {
        "commentId": str,
        "content": str,
        "inReplyTo": str,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
        "authorArn": str,
        "deleted": bool,
        "clientRequestToken": str,
        "callerReactions": List[str],
        "reactionCounts": Dict[str, int],
    },
    total=False,
)

LocationTypeDef = TypedDict(
    "LocationTypeDef",
    {
        "filePath": str,
        "filePosition": int,
        "relativeFileVersion": RelativeFileVersionEnumType,
    },
    total=False,
)

UserInfoTypeDef = TypedDict(
    "UserInfoTypeDef",
    {
        "name": str,
        "email": str,
        "date": str,
    },
    total=False,
)

FileModesTypeDef = TypedDict(
    "FileModesTypeDef",
    {
        "source": FileModeTypeEnumType,
        "destination": FileModeTypeEnumType,
        "base": FileModeTypeEnumType,
    },
    total=False,
)

FileSizesTypeDef = TypedDict(
    "FileSizesTypeDef",
    {
        "source": int,
        "destination": int,
        "base": int,
    },
    total=False,
)

IsBinaryFileTypeDef = TypedDict(
    "IsBinaryFileTypeDef",
    {
        "source": bool,
        "destination": bool,
        "base": bool,
    },
    total=False,
)

MergeOperationsTypeDef = TypedDict(
    "MergeOperationsTypeDef",
    {
        "source": ChangeTypeEnumType,
        "destination": ChangeTypeEnumType,
    },
    total=False,
)

ObjectTypesTypeDef = TypedDict(
    "ObjectTypesTypeDef",
    {
        "source": ObjectTypeEnumType,
        "destination": ObjectTypeEnumType,
        "base": ObjectTypeEnumType,
    },
    total=False,
)

DeleteFileEntryTypeDef = TypedDict(
    "DeleteFileEntryTypeDef",
    {
        "filePath": str,
    },
)

_RequiredReplaceContentEntryTypeDef = TypedDict(
    "_RequiredReplaceContentEntryTypeDef",
    {
        "filePath": str,
        "replacementType": ReplacementTypeEnumType,
    },
)
_OptionalReplaceContentEntryTypeDef = TypedDict(
    "_OptionalReplaceContentEntryTypeDef",
    {
        "content": Union[str, bytes, IO[Any], StreamingBody],
        "fileMode": FileModeTypeEnumType,
    },
    total=False,
)


class ReplaceContentEntryTypeDef(
    _RequiredReplaceContentEntryTypeDef, _OptionalReplaceContentEntryTypeDef
):
    pass


SetFileModeEntryTypeDef = TypedDict(
    "SetFileModeEntryTypeDef",
    {
        "filePath": str,
        "fileMode": FileModeTypeEnumType,
    },
)

_RequiredCreateApprovalRuleTemplateInputRequestTypeDef = TypedDict(
    "_RequiredCreateApprovalRuleTemplateInputRequestTypeDef",
    {
        "approvalRuleTemplateName": str,
        "approvalRuleTemplateContent": str,
    },
)
_OptionalCreateApprovalRuleTemplateInputRequestTypeDef = TypedDict(
    "_OptionalCreateApprovalRuleTemplateInputRequestTypeDef",
    {
        "approvalRuleTemplateDescription": str,
    },
    total=False,
)


class CreateApprovalRuleTemplateInputRequestTypeDef(
    _RequiredCreateApprovalRuleTemplateInputRequestTypeDef,
    _OptionalCreateApprovalRuleTemplateInputRequestTypeDef,
):
    pass


CreateBranchInputRequestTypeDef = TypedDict(
    "CreateBranchInputRequestTypeDef",
    {
        "repositoryName": str,
        "branchName": str,
        "commitId": str,
    },
)

FileMetadataTypeDef = TypedDict(
    "FileMetadataTypeDef",
    {
        "absolutePath": str,
        "blobId": str,
        "fileMode": FileModeTypeEnumType,
    },
    total=False,
)

CreatePullRequestApprovalRuleInputRequestTypeDef = TypedDict(
    "CreatePullRequestApprovalRuleInputRequestTypeDef",
    {
        "pullRequestId": str,
        "approvalRuleName": str,
        "approvalRuleContent": str,
    },
)

_RequiredTargetTypeDef = TypedDict(
    "_RequiredTargetTypeDef",
    {
        "repositoryName": str,
        "sourceReference": str,
    },
)
_OptionalTargetTypeDef = TypedDict(
    "_OptionalTargetTypeDef",
    {
        "destinationReference": str,
    },
    total=False,
)


class TargetTypeDef(_RequiredTargetTypeDef, _OptionalTargetTypeDef):
    pass


_RequiredCreateRepositoryInputRequestTypeDef = TypedDict(
    "_RequiredCreateRepositoryInputRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalCreateRepositoryInputRequestTypeDef = TypedDict(
    "_OptionalCreateRepositoryInputRequestTypeDef",
    {
        "repositoryDescription": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateRepositoryInputRequestTypeDef(
    _RequiredCreateRepositoryInputRequestTypeDef, _OptionalCreateRepositoryInputRequestTypeDef
):
    pass


DeleteApprovalRuleTemplateInputRequestTypeDef = TypedDict(
    "DeleteApprovalRuleTemplateInputRequestTypeDef",
    {
        "approvalRuleTemplateName": str,
    },
)

DeleteBranchInputRequestTypeDef = TypedDict(
    "DeleteBranchInputRequestTypeDef",
    {
        "repositoryName": str,
        "branchName": str,
    },
)

DeleteCommentContentInputRequestTypeDef = TypedDict(
    "DeleteCommentContentInputRequestTypeDef",
    {
        "commentId": str,
    },
)

_RequiredDeleteFileInputRequestTypeDef = TypedDict(
    "_RequiredDeleteFileInputRequestTypeDef",
    {
        "repositoryName": str,
        "branchName": str,
        "filePath": str,
        "parentCommitId": str,
    },
)
_OptionalDeleteFileInputRequestTypeDef = TypedDict(
    "_OptionalDeleteFileInputRequestTypeDef",
    {
        "keepEmptyFolders": bool,
        "commitMessage": str,
        "name": str,
        "email": str,
    },
    total=False,
)


class DeleteFileInputRequestTypeDef(
    _RequiredDeleteFileInputRequestTypeDef, _OptionalDeleteFileInputRequestTypeDef
):
    pass


DeletePullRequestApprovalRuleInputRequestTypeDef = TypedDict(
    "DeletePullRequestApprovalRuleInputRequestTypeDef",
    {
        "pullRequestId": str,
        "approvalRuleName": str,
    },
)

DeleteRepositoryInputRequestTypeDef = TypedDict(
    "DeleteRepositoryInputRequestTypeDef",
    {
        "repositoryName": str,
    },
)

_RequiredDescribeMergeConflictsInputRequestTypeDef = TypedDict(
    "_RequiredDescribeMergeConflictsInputRequestTypeDef",
    {
        "repositoryName": str,
        "destinationCommitSpecifier": str,
        "sourceCommitSpecifier": str,
        "mergeOption": MergeOptionTypeEnumType,
        "filePath": str,
    },
)
_OptionalDescribeMergeConflictsInputRequestTypeDef = TypedDict(
    "_OptionalDescribeMergeConflictsInputRequestTypeDef",
    {
        "maxMergeHunks": int,
        "conflictDetailLevel": ConflictDetailLevelTypeEnumType,
        "conflictResolutionStrategy": ConflictResolutionStrategyTypeEnumType,
        "nextToken": str,
    },
    total=False,
)


class DescribeMergeConflictsInputRequestTypeDef(
    _RequiredDescribeMergeConflictsInputRequestTypeDef,
    _OptionalDescribeMergeConflictsInputRequestTypeDef,
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredDescribePullRequestEventsInputRequestTypeDef = TypedDict(
    "_RequiredDescribePullRequestEventsInputRequestTypeDef",
    {
        "pullRequestId": str,
    },
)
_OptionalDescribePullRequestEventsInputRequestTypeDef = TypedDict(
    "_OptionalDescribePullRequestEventsInputRequestTypeDef",
    {
        "pullRequestEventType": PullRequestEventTypeType,
        "actorArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class DescribePullRequestEventsInputRequestTypeDef(
    _RequiredDescribePullRequestEventsInputRequestTypeDef,
    _OptionalDescribePullRequestEventsInputRequestTypeDef,
):
    pass


DisassociateApprovalRuleTemplateFromRepositoryInputRequestTypeDef = TypedDict(
    "DisassociateApprovalRuleTemplateFromRepositoryInputRequestTypeDef",
    {
        "approvalRuleTemplateName": str,
        "repositoryName": str,
    },
)

EvaluatePullRequestApprovalRulesInputRequestTypeDef = TypedDict(
    "EvaluatePullRequestApprovalRulesInputRequestTypeDef",
    {
        "pullRequestId": str,
        "revisionId": str,
    },
)

EvaluationTypeDef = TypedDict(
    "EvaluationTypeDef",
    {
        "approved": bool,
        "overridden": bool,
        "approvalRulesSatisfied": List[str],
        "approvalRulesNotSatisfied": List[str],
    },
    total=False,
)

FileTypeDef = TypedDict(
    "FileTypeDef",
    {
        "blobId": str,
        "absolutePath": str,
        "relativePath": str,
        "fileMode": FileModeTypeEnumType,
    },
    total=False,
)

FolderTypeDef = TypedDict(
    "FolderTypeDef",
    {
        "treeId": str,
        "absolutePath": str,
        "relativePath": str,
    },
    total=False,
)

GetApprovalRuleTemplateInputRequestTypeDef = TypedDict(
    "GetApprovalRuleTemplateInputRequestTypeDef",
    {
        "approvalRuleTemplateName": str,
    },
)

GetBlobInputRequestTypeDef = TypedDict(
    "GetBlobInputRequestTypeDef",
    {
        "repositoryName": str,
        "blobId": str,
    },
)

GetBranchInputRequestTypeDef = TypedDict(
    "GetBranchInputRequestTypeDef",
    {
        "repositoryName": str,
        "branchName": str,
    },
    total=False,
)

GetCommentInputRequestTypeDef = TypedDict(
    "GetCommentInputRequestTypeDef",
    {
        "commentId": str,
    },
)

_RequiredGetCommentReactionsInputRequestTypeDef = TypedDict(
    "_RequiredGetCommentReactionsInputRequestTypeDef",
    {
        "commentId": str,
    },
)
_OptionalGetCommentReactionsInputRequestTypeDef = TypedDict(
    "_OptionalGetCommentReactionsInputRequestTypeDef",
    {
        "reactionUserArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetCommentReactionsInputRequestTypeDef(
    _RequiredGetCommentReactionsInputRequestTypeDef, _OptionalGetCommentReactionsInputRequestTypeDef
):
    pass


_RequiredGetCommentsForComparedCommitInputRequestTypeDef = TypedDict(
    "_RequiredGetCommentsForComparedCommitInputRequestTypeDef",
    {
        "repositoryName": str,
        "afterCommitId": str,
    },
)
_OptionalGetCommentsForComparedCommitInputRequestTypeDef = TypedDict(
    "_OptionalGetCommentsForComparedCommitInputRequestTypeDef",
    {
        "beforeCommitId": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetCommentsForComparedCommitInputRequestTypeDef(
    _RequiredGetCommentsForComparedCommitInputRequestTypeDef,
    _OptionalGetCommentsForComparedCommitInputRequestTypeDef,
):
    pass


_RequiredGetCommentsForPullRequestInputRequestTypeDef = TypedDict(
    "_RequiredGetCommentsForPullRequestInputRequestTypeDef",
    {
        "pullRequestId": str,
    },
)
_OptionalGetCommentsForPullRequestInputRequestTypeDef = TypedDict(
    "_OptionalGetCommentsForPullRequestInputRequestTypeDef",
    {
        "repositoryName": str,
        "beforeCommitId": str,
        "afterCommitId": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetCommentsForPullRequestInputRequestTypeDef(
    _RequiredGetCommentsForPullRequestInputRequestTypeDef,
    _OptionalGetCommentsForPullRequestInputRequestTypeDef,
):
    pass


GetCommitInputRequestTypeDef = TypedDict(
    "GetCommitInputRequestTypeDef",
    {
        "repositoryName": str,
        "commitId": str,
    },
)

_RequiredGetDifferencesInputRequestTypeDef = TypedDict(
    "_RequiredGetDifferencesInputRequestTypeDef",
    {
        "repositoryName": str,
        "afterCommitSpecifier": str,
    },
)
_OptionalGetDifferencesInputRequestTypeDef = TypedDict(
    "_OptionalGetDifferencesInputRequestTypeDef",
    {
        "beforeCommitSpecifier": str,
        "beforePath": str,
        "afterPath": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetDifferencesInputRequestTypeDef(
    _RequiredGetDifferencesInputRequestTypeDef, _OptionalGetDifferencesInputRequestTypeDef
):
    pass


_RequiredGetFileInputRequestTypeDef = TypedDict(
    "_RequiredGetFileInputRequestTypeDef",
    {
        "repositoryName": str,
        "filePath": str,
    },
)
_OptionalGetFileInputRequestTypeDef = TypedDict(
    "_OptionalGetFileInputRequestTypeDef",
    {
        "commitSpecifier": str,
    },
    total=False,
)


class GetFileInputRequestTypeDef(
    _RequiredGetFileInputRequestTypeDef, _OptionalGetFileInputRequestTypeDef
):
    pass


_RequiredGetFolderInputRequestTypeDef = TypedDict(
    "_RequiredGetFolderInputRequestTypeDef",
    {
        "repositoryName": str,
        "folderPath": str,
    },
)
_OptionalGetFolderInputRequestTypeDef = TypedDict(
    "_OptionalGetFolderInputRequestTypeDef",
    {
        "commitSpecifier": str,
    },
    total=False,
)


class GetFolderInputRequestTypeDef(
    _RequiredGetFolderInputRequestTypeDef, _OptionalGetFolderInputRequestTypeDef
):
    pass


SubModuleTypeDef = TypedDict(
    "SubModuleTypeDef",
    {
        "commitId": str,
        "absolutePath": str,
        "relativePath": str,
    },
    total=False,
)

SymbolicLinkTypeDef = TypedDict(
    "SymbolicLinkTypeDef",
    {
        "blobId": str,
        "absolutePath": str,
        "relativePath": str,
        "fileMode": FileModeTypeEnumType,
    },
    total=False,
)

_RequiredGetMergeCommitInputRequestTypeDef = TypedDict(
    "_RequiredGetMergeCommitInputRequestTypeDef",
    {
        "repositoryName": str,
        "sourceCommitSpecifier": str,
        "destinationCommitSpecifier": str,
    },
)
_OptionalGetMergeCommitInputRequestTypeDef = TypedDict(
    "_OptionalGetMergeCommitInputRequestTypeDef",
    {
        "conflictDetailLevel": ConflictDetailLevelTypeEnumType,
        "conflictResolutionStrategy": ConflictResolutionStrategyTypeEnumType,
    },
    total=False,
)


class GetMergeCommitInputRequestTypeDef(
    _RequiredGetMergeCommitInputRequestTypeDef, _OptionalGetMergeCommitInputRequestTypeDef
):
    pass


_RequiredGetMergeConflictsInputRequestTypeDef = TypedDict(
    "_RequiredGetMergeConflictsInputRequestTypeDef",
    {
        "repositoryName": str,
        "destinationCommitSpecifier": str,
        "sourceCommitSpecifier": str,
        "mergeOption": MergeOptionTypeEnumType,
    },
)
_OptionalGetMergeConflictsInputRequestTypeDef = TypedDict(
    "_OptionalGetMergeConflictsInputRequestTypeDef",
    {
        "conflictDetailLevel": ConflictDetailLevelTypeEnumType,
        "maxConflictFiles": int,
        "conflictResolutionStrategy": ConflictResolutionStrategyTypeEnumType,
        "nextToken": str,
    },
    total=False,
)


class GetMergeConflictsInputRequestTypeDef(
    _RequiredGetMergeConflictsInputRequestTypeDef, _OptionalGetMergeConflictsInputRequestTypeDef
):
    pass


_RequiredGetMergeOptionsInputRequestTypeDef = TypedDict(
    "_RequiredGetMergeOptionsInputRequestTypeDef",
    {
        "repositoryName": str,
        "sourceCommitSpecifier": str,
        "destinationCommitSpecifier": str,
    },
)
_OptionalGetMergeOptionsInputRequestTypeDef = TypedDict(
    "_OptionalGetMergeOptionsInputRequestTypeDef",
    {
        "conflictDetailLevel": ConflictDetailLevelTypeEnumType,
        "conflictResolutionStrategy": ConflictResolutionStrategyTypeEnumType,
    },
    total=False,
)


class GetMergeOptionsInputRequestTypeDef(
    _RequiredGetMergeOptionsInputRequestTypeDef, _OptionalGetMergeOptionsInputRequestTypeDef
):
    pass


GetPullRequestApprovalStatesInputRequestTypeDef = TypedDict(
    "GetPullRequestApprovalStatesInputRequestTypeDef",
    {
        "pullRequestId": str,
        "revisionId": str,
    },
)

GetPullRequestInputRequestTypeDef = TypedDict(
    "GetPullRequestInputRequestTypeDef",
    {
        "pullRequestId": str,
    },
)

GetPullRequestOverrideStateInputRequestTypeDef = TypedDict(
    "GetPullRequestOverrideStateInputRequestTypeDef",
    {
        "pullRequestId": str,
        "revisionId": str,
    },
)

GetRepositoryInputRequestTypeDef = TypedDict(
    "GetRepositoryInputRequestTypeDef",
    {
        "repositoryName": str,
    },
)

GetRepositoryTriggersInputRequestTypeDef = TypedDict(
    "GetRepositoryTriggersInputRequestTypeDef",
    {
        "repositoryName": str,
    },
)

_RequiredRepositoryTriggerTypeDef = TypedDict(
    "_RequiredRepositoryTriggerTypeDef",
    {
        "name": str,
        "destinationArn": str,
        "events": List[RepositoryTriggerEventEnumType],
    },
)
_OptionalRepositoryTriggerTypeDef = TypedDict(
    "_OptionalRepositoryTriggerTypeDef",
    {
        "customData": str,
        "branches": List[str],
    },
    total=False,
)


class RepositoryTriggerTypeDef(
    _RequiredRepositoryTriggerTypeDef, _OptionalRepositoryTriggerTypeDef
):
    pass


ListApprovalRuleTemplatesInputRequestTypeDef = TypedDict(
    "ListApprovalRuleTemplatesInputRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListAssociatedApprovalRuleTemplatesForRepositoryInputRequestTypeDef = TypedDict(
    "_RequiredListAssociatedApprovalRuleTemplatesForRepositoryInputRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalListAssociatedApprovalRuleTemplatesForRepositoryInputRequestTypeDef = TypedDict(
    "_OptionalListAssociatedApprovalRuleTemplatesForRepositoryInputRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAssociatedApprovalRuleTemplatesForRepositoryInputRequestTypeDef(
    _RequiredListAssociatedApprovalRuleTemplatesForRepositoryInputRequestTypeDef,
    _OptionalListAssociatedApprovalRuleTemplatesForRepositoryInputRequestTypeDef,
):
    pass


_RequiredListBranchesInputRequestTypeDef = TypedDict(
    "_RequiredListBranchesInputRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalListBranchesInputRequestTypeDef = TypedDict(
    "_OptionalListBranchesInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListBranchesInputRequestTypeDef(
    _RequiredListBranchesInputRequestTypeDef, _OptionalListBranchesInputRequestTypeDef
):
    pass


_RequiredListPullRequestsInputRequestTypeDef = TypedDict(
    "_RequiredListPullRequestsInputRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalListPullRequestsInputRequestTypeDef = TypedDict(
    "_OptionalListPullRequestsInputRequestTypeDef",
    {
        "authorArn": str,
        "pullRequestStatus": PullRequestStatusEnumType,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListPullRequestsInputRequestTypeDef(
    _RequiredListPullRequestsInputRequestTypeDef, _OptionalListPullRequestsInputRequestTypeDef
):
    pass


_RequiredListRepositoriesForApprovalRuleTemplateInputRequestTypeDef = TypedDict(
    "_RequiredListRepositoriesForApprovalRuleTemplateInputRequestTypeDef",
    {
        "approvalRuleTemplateName": str,
    },
)
_OptionalListRepositoriesForApprovalRuleTemplateInputRequestTypeDef = TypedDict(
    "_OptionalListRepositoriesForApprovalRuleTemplateInputRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListRepositoriesForApprovalRuleTemplateInputRequestTypeDef(
    _RequiredListRepositoriesForApprovalRuleTemplateInputRequestTypeDef,
    _OptionalListRepositoriesForApprovalRuleTemplateInputRequestTypeDef,
):
    pass


ListRepositoriesInputRequestTypeDef = TypedDict(
    "ListRepositoriesInputRequestTypeDef",
    {
        "nextToken": str,
        "sortBy": SortByEnumType,
        "order": OrderEnumType,
    },
    total=False,
)

RepositoryNameIdPairTypeDef = TypedDict(
    "RepositoryNameIdPairTypeDef",
    {
        "repositoryName": str,
        "repositoryId": str,
    },
    total=False,
)

_RequiredListTagsForResourceInputRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalListTagsForResourceInputRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListTagsForResourceInputRequestTypeDef(
    _RequiredListTagsForResourceInputRequestTypeDef, _OptionalListTagsForResourceInputRequestTypeDef
):
    pass


_RequiredMergeBranchesByFastForwardInputRequestTypeDef = TypedDict(
    "_RequiredMergeBranchesByFastForwardInputRequestTypeDef",
    {
        "repositoryName": str,
        "sourceCommitSpecifier": str,
        "destinationCommitSpecifier": str,
    },
)
_OptionalMergeBranchesByFastForwardInputRequestTypeDef = TypedDict(
    "_OptionalMergeBranchesByFastForwardInputRequestTypeDef",
    {
        "targetBranch": str,
    },
    total=False,
)


class MergeBranchesByFastForwardInputRequestTypeDef(
    _RequiredMergeBranchesByFastForwardInputRequestTypeDef,
    _OptionalMergeBranchesByFastForwardInputRequestTypeDef,
):
    pass


MergeHunkDetailTypeDef = TypedDict(
    "MergeHunkDetailTypeDef",
    {
        "startLine": int,
        "endLine": int,
        "hunkContent": str,
    },
    total=False,
)

MergeMetadataTypeDef = TypedDict(
    "MergeMetadataTypeDef",
    {
        "isMerged": bool,
        "mergedBy": str,
        "mergeCommitId": str,
        "mergeOption": MergeOptionTypeEnumType,
    },
    total=False,
)

_RequiredMergePullRequestByFastForwardInputRequestTypeDef = TypedDict(
    "_RequiredMergePullRequestByFastForwardInputRequestTypeDef",
    {
        "pullRequestId": str,
        "repositoryName": str,
    },
)
_OptionalMergePullRequestByFastForwardInputRequestTypeDef = TypedDict(
    "_OptionalMergePullRequestByFastForwardInputRequestTypeDef",
    {
        "sourceCommitId": str,
    },
    total=False,
)


class MergePullRequestByFastForwardInputRequestTypeDef(
    _RequiredMergePullRequestByFastForwardInputRequestTypeDef,
    _OptionalMergePullRequestByFastForwardInputRequestTypeDef,
):
    pass


OverridePullRequestApprovalRulesInputRequestTypeDef = TypedDict(
    "OverridePullRequestApprovalRulesInputRequestTypeDef",
    {
        "pullRequestId": str,
        "revisionId": str,
        "overrideStatus": OverrideStatusType,
    },
)

_RequiredPostCommentReplyInputRequestTypeDef = TypedDict(
    "_RequiredPostCommentReplyInputRequestTypeDef",
    {
        "inReplyTo": str,
        "content": str,
    },
)
_OptionalPostCommentReplyInputRequestTypeDef = TypedDict(
    "_OptionalPostCommentReplyInputRequestTypeDef",
    {
        "clientRequestToken": str,
    },
    total=False,
)


class PostCommentReplyInputRequestTypeDef(
    _RequiredPostCommentReplyInputRequestTypeDef, _OptionalPostCommentReplyInputRequestTypeDef
):
    pass


PullRequestCreatedEventMetadataTypeDef = TypedDict(
    "PullRequestCreatedEventMetadataTypeDef",
    {
        "repositoryName": str,
        "sourceCommitId": str,
        "destinationCommitId": str,
        "mergeBase": str,
    },
    total=False,
)

PullRequestSourceReferenceUpdatedEventMetadataTypeDef = TypedDict(
    "PullRequestSourceReferenceUpdatedEventMetadataTypeDef",
    {
        "repositoryName": str,
        "beforeCommitId": str,
        "afterCommitId": str,
        "mergeBase": str,
    },
    total=False,
)

PullRequestStatusChangedEventMetadataTypeDef = TypedDict(
    "PullRequestStatusChangedEventMetadataTypeDef",
    {
        "pullRequestStatus": PullRequestStatusEnumType,
    },
    total=False,
)

PutCommentReactionInputRequestTypeDef = TypedDict(
    "PutCommentReactionInputRequestTypeDef",
    {
        "commentId": str,
        "reactionValue": str,
    },
)

_RequiredSourceFileSpecifierTypeDef = TypedDict(
    "_RequiredSourceFileSpecifierTypeDef",
    {
        "filePath": str,
    },
)
_OptionalSourceFileSpecifierTypeDef = TypedDict(
    "_OptionalSourceFileSpecifierTypeDef",
    {
        "isMove": bool,
    },
    total=False,
)


class SourceFileSpecifierTypeDef(
    _RequiredSourceFileSpecifierTypeDef, _OptionalSourceFileSpecifierTypeDef
):
    pass


_RequiredPutFileInputRequestTypeDef = TypedDict(
    "_RequiredPutFileInputRequestTypeDef",
    {
        "repositoryName": str,
        "branchName": str,
        "fileContent": Union[str, bytes, IO[Any], StreamingBody],
        "filePath": str,
    },
)
_OptionalPutFileInputRequestTypeDef = TypedDict(
    "_OptionalPutFileInputRequestTypeDef",
    {
        "fileMode": FileModeTypeEnumType,
        "parentCommitId": str,
        "commitMessage": str,
        "name": str,
        "email": str,
    },
    total=False,
)


class PutFileInputRequestTypeDef(
    _RequiredPutFileInputRequestTypeDef, _OptionalPutFileInputRequestTypeDef
):
    pass


ReactionValueFormatsTypeDef = TypedDict(
    "ReactionValueFormatsTypeDef",
    {
        "emoji": str,
        "shortCode": str,
        "unicode": str,
    },
    total=False,
)

RepositoryTriggerExecutionFailureTypeDef = TypedDict(
    "RepositoryTriggerExecutionFailureTypeDef",
    {
        "trigger": str,
        "failureMessage": str,
    },
    total=False,
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateApprovalRuleTemplateContentInputRequestTypeDef = TypedDict(
    "_RequiredUpdateApprovalRuleTemplateContentInputRequestTypeDef",
    {
        "approvalRuleTemplateName": str,
        "newRuleContent": str,
    },
)
_OptionalUpdateApprovalRuleTemplateContentInputRequestTypeDef = TypedDict(
    "_OptionalUpdateApprovalRuleTemplateContentInputRequestTypeDef",
    {
        "existingRuleContentSha256": str,
    },
    total=False,
)


class UpdateApprovalRuleTemplateContentInputRequestTypeDef(
    _RequiredUpdateApprovalRuleTemplateContentInputRequestTypeDef,
    _OptionalUpdateApprovalRuleTemplateContentInputRequestTypeDef,
):
    pass


UpdateApprovalRuleTemplateDescriptionInputRequestTypeDef = TypedDict(
    "UpdateApprovalRuleTemplateDescriptionInputRequestTypeDef",
    {
        "approvalRuleTemplateName": str,
        "approvalRuleTemplateDescription": str,
    },
)

UpdateApprovalRuleTemplateNameInputRequestTypeDef = TypedDict(
    "UpdateApprovalRuleTemplateNameInputRequestTypeDef",
    {
        "oldApprovalRuleTemplateName": str,
        "newApprovalRuleTemplateName": str,
    },
)

UpdateCommentInputRequestTypeDef = TypedDict(
    "UpdateCommentInputRequestTypeDef",
    {
        "commentId": str,
        "content": str,
    },
)

UpdateDefaultBranchInputRequestTypeDef = TypedDict(
    "UpdateDefaultBranchInputRequestTypeDef",
    {
        "repositoryName": str,
        "defaultBranchName": str,
    },
)

_RequiredUpdatePullRequestApprovalRuleContentInputRequestTypeDef = TypedDict(
    "_RequiredUpdatePullRequestApprovalRuleContentInputRequestTypeDef",
    {
        "pullRequestId": str,
        "approvalRuleName": str,
        "newRuleContent": str,
    },
)
_OptionalUpdatePullRequestApprovalRuleContentInputRequestTypeDef = TypedDict(
    "_OptionalUpdatePullRequestApprovalRuleContentInputRequestTypeDef",
    {
        "existingRuleContentSha256": str,
    },
    total=False,
)


class UpdatePullRequestApprovalRuleContentInputRequestTypeDef(
    _RequiredUpdatePullRequestApprovalRuleContentInputRequestTypeDef,
    _OptionalUpdatePullRequestApprovalRuleContentInputRequestTypeDef,
):
    pass


UpdatePullRequestApprovalStateInputRequestTypeDef = TypedDict(
    "UpdatePullRequestApprovalStateInputRequestTypeDef",
    {
        "pullRequestId": str,
        "revisionId": str,
        "approvalState": ApprovalStateType,
    },
)

UpdatePullRequestDescriptionInputRequestTypeDef = TypedDict(
    "UpdatePullRequestDescriptionInputRequestTypeDef",
    {
        "pullRequestId": str,
        "description": str,
    },
)

UpdatePullRequestStatusInputRequestTypeDef = TypedDict(
    "UpdatePullRequestStatusInputRequestTypeDef",
    {
        "pullRequestId": str,
        "pullRequestStatus": PullRequestStatusEnumType,
    },
)

UpdatePullRequestTitleInputRequestTypeDef = TypedDict(
    "UpdatePullRequestTitleInputRequestTypeDef",
    {
        "pullRequestId": str,
        "title": str,
    },
)

_RequiredUpdateRepositoryDescriptionInputRequestTypeDef = TypedDict(
    "_RequiredUpdateRepositoryDescriptionInputRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalUpdateRepositoryDescriptionInputRequestTypeDef = TypedDict(
    "_OptionalUpdateRepositoryDescriptionInputRequestTypeDef",
    {
        "repositoryDescription": str,
    },
    total=False,
)


class UpdateRepositoryDescriptionInputRequestTypeDef(
    _RequiredUpdateRepositoryDescriptionInputRequestTypeDef,
    _OptionalUpdateRepositoryDescriptionInputRequestTypeDef,
):
    pass


UpdateRepositoryNameInputRequestTypeDef = TypedDict(
    "UpdateRepositoryNameInputRequestTypeDef",
    {
        "oldName": str,
        "newName": str,
    },
)

ApprovalRuleTypeDef = TypedDict(
    "ApprovalRuleTypeDef",
    {
        "approvalRuleId": str,
        "approvalRuleName": str,
        "approvalRuleContent": str,
        "ruleContentSha256": str,
        "lastModifiedDate": datetime,
        "creationDate": datetime,
        "lastModifiedUser": str,
        "originApprovalRuleTemplate": OriginApprovalRuleTemplateTypeDef,
    },
    total=False,
)

BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef = TypedDict(
    "BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef",
    {
        "associatedRepositoryNames": List[str],
        "errors": List[BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateApprovalRuleTemplateOutputTypeDef = TypedDict(
    "CreateApprovalRuleTemplateOutputTypeDef",
    {
        "approvalRuleTemplate": ApprovalRuleTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUnreferencedMergeCommitOutputTypeDef = TypedDict(
    "CreateUnreferencedMergeCommitOutputTypeDef",
    {
        "commitId": str,
        "treeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteApprovalRuleTemplateOutputTypeDef = TypedDict(
    "DeleteApprovalRuleTemplateOutputTypeDef",
    {
        "approvalRuleTemplateId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFileOutputTypeDef = TypedDict(
    "DeleteFileOutputTypeDef",
    {
        "commitId": str,
        "blobId": str,
        "treeId": str,
        "filePath": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeletePullRequestApprovalRuleOutputTypeDef = TypedDict(
    "DeletePullRequestApprovalRuleOutputTypeDef",
    {
        "approvalRuleId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRepositoryOutputTypeDef = TypedDict(
    "DeleteRepositoryOutputTypeDef",
    {
        "repositoryId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetApprovalRuleTemplateOutputTypeDef = TypedDict(
    "GetApprovalRuleTemplateOutputTypeDef",
    {
        "approvalRuleTemplate": ApprovalRuleTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBlobOutputTypeDef = TypedDict(
    "GetBlobOutputTypeDef",
    {
        "content": bytes,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFileOutputTypeDef = TypedDict(
    "GetFileOutputTypeDef",
    {
        "commitId": str,
        "blobId": str,
        "filePath": str,
        "fileMode": FileModeTypeEnumType,
        "fileSize": int,
        "fileContent": bytes,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMergeCommitOutputTypeDef = TypedDict(
    "GetMergeCommitOutputTypeDef",
    {
        "sourceCommitId": str,
        "destinationCommitId": str,
        "baseCommitId": str,
        "mergedCommitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMergeOptionsOutputTypeDef = TypedDict(
    "GetMergeOptionsOutputTypeDef",
    {
        "mergeOptions": List[MergeOptionTypeEnumType],
        "sourceCommitId": str,
        "destinationCommitId": str,
        "baseCommitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPullRequestApprovalStatesOutputTypeDef = TypedDict(
    "GetPullRequestApprovalStatesOutputTypeDef",
    {
        "approvals": List[ApprovalTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPullRequestOverrideStateOutputTypeDef = TypedDict(
    "GetPullRequestOverrideStateOutputTypeDef",
    {
        "overridden": bool,
        "overrider": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListApprovalRuleTemplatesOutputTypeDef = TypedDict(
    "ListApprovalRuleTemplatesOutputTypeDef",
    {
        "approvalRuleTemplateNames": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef = TypedDict(
    "ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef",
    {
        "approvalRuleTemplateNames": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBranchesOutputTypeDef = TypedDict(
    "ListBranchesOutputTypeDef",
    {
        "branches": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPullRequestsOutputTypeDef = TypedDict(
    "ListPullRequestsOutputTypeDef",
    {
        "pullRequestIds": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRepositoriesForApprovalRuleTemplateOutputTypeDef = TypedDict(
    "ListRepositoriesForApprovalRuleTemplateOutputTypeDef",
    {
        "repositoryNames": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "tags": Dict[str, str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MergeBranchesByFastForwardOutputTypeDef = TypedDict(
    "MergeBranchesByFastForwardOutputTypeDef",
    {
        "commitId": str,
        "treeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MergeBranchesBySquashOutputTypeDef = TypedDict(
    "MergeBranchesBySquashOutputTypeDef",
    {
        "commitId": str,
        "treeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MergeBranchesByThreeWayOutputTypeDef = TypedDict(
    "MergeBranchesByThreeWayOutputTypeDef",
    {
        "commitId": str,
        "treeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutFileOutputTypeDef = TypedDict(
    "PutFileOutputTypeDef",
    {
        "commitId": str,
        "blobId": str,
        "treeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutRepositoryTriggersOutputTypeDef = TypedDict(
    "PutRepositoryTriggersOutputTypeDef",
    {
        "configurationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateApprovalRuleTemplateContentOutputTypeDef = TypedDict(
    "UpdateApprovalRuleTemplateContentOutputTypeDef",
    {
        "approvalRuleTemplate": ApprovalRuleTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateApprovalRuleTemplateDescriptionOutputTypeDef = TypedDict(
    "UpdateApprovalRuleTemplateDescriptionOutputTypeDef",
    {
        "approvalRuleTemplate": ApprovalRuleTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateApprovalRuleTemplateNameOutputTypeDef = TypedDict(
    "UpdateApprovalRuleTemplateNameOutputTypeDef",
    {
        "approvalRuleTemplate": ApprovalRuleTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef = TypedDict(
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef",
    {
        "disassociatedRepositoryNames": List[str],
        "errors": List[BatchDisassociateApprovalRuleTemplateFromRepositoriesErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetRepositoriesOutputTypeDef = TypedDict(
    "BatchGetRepositoriesOutputTypeDef",
    {
        "repositories": List[RepositoryMetadataTypeDef],
        "repositoriesNotFound": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRepositoryOutputTypeDef = TypedDict(
    "CreateRepositoryOutputTypeDef",
    {
        "repositoryMetadata": RepositoryMetadataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRepositoryOutputTypeDef = TypedDict(
    "GetRepositoryOutputTypeDef",
    {
        "repositoryMetadata": RepositoryMetadataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DifferenceTypeDef = TypedDict(
    "DifferenceTypeDef",
    {
        "beforeBlob": BlobMetadataTypeDef,
        "afterBlob": BlobMetadataTypeDef,
        "changeType": ChangeTypeEnumType,
    },
    total=False,
)

DeleteBranchOutputTypeDef = TypedDict(
    "DeleteBranchOutputTypeDef",
    {
        "deletedBranch": BranchInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBranchOutputTypeDef = TypedDict(
    "GetBranchOutputTypeDef",
    {
        "branch": BranchInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteCommentContentOutputTypeDef = TypedDict(
    "DeleteCommentContentOutputTypeDef",
    {
        "comment": CommentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCommentOutputTypeDef = TypedDict(
    "GetCommentOutputTypeDef",
    {
        "comment": CommentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PostCommentReplyOutputTypeDef = TypedDict(
    "PostCommentReplyOutputTypeDef",
    {
        "comment": CommentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCommentOutputTypeDef = TypedDict(
    "UpdateCommentOutputTypeDef",
    {
        "comment": CommentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CommentsForComparedCommitTypeDef = TypedDict(
    "CommentsForComparedCommitTypeDef",
    {
        "repositoryName": str,
        "beforeCommitId": str,
        "afterCommitId": str,
        "beforeBlobId": str,
        "afterBlobId": str,
        "location": LocationTypeDef,
        "comments": List[CommentTypeDef],
    },
    total=False,
)

CommentsForPullRequestTypeDef = TypedDict(
    "CommentsForPullRequestTypeDef",
    {
        "pullRequestId": str,
        "repositoryName": str,
        "beforeCommitId": str,
        "afterCommitId": str,
        "beforeBlobId": str,
        "afterBlobId": str,
        "location": LocationTypeDef,
        "comments": List[CommentTypeDef],
    },
    total=False,
)

_RequiredPostCommentForComparedCommitInputRequestTypeDef = TypedDict(
    "_RequiredPostCommentForComparedCommitInputRequestTypeDef",
    {
        "repositoryName": str,
        "afterCommitId": str,
        "content": str,
    },
)
_OptionalPostCommentForComparedCommitInputRequestTypeDef = TypedDict(
    "_OptionalPostCommentForComparedCommitInputRequestTypeDef",
    {
        "beforeCommitId": str,
        "location": LocationTypeDef,
        "clientRequestToken": str,
    },
    total=False,
)


class PostCommentForComparedCommitInputRequestTypeDef(
    _RequiredPostCommentForComparedCommitInputRequestTypeDef,
    _OptionalPostCommentForComparedCommitInputRequestTypeDef,
):
    pass


PostCommentForComparedCommitOutputTypeDef = TypedDict(
    "PostCommentForComparedCommitOutputTypeDef",
    {
        "repositoryName": str,
        "beforeCommitId": str,
        "afterCommitId": str,
        "beforeBlobId": str,
        "afterBlobId": str,
        "location": LocationTypeDef,
        "comment": CommentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPostCommentForPullRequestInputRequestTypeDef = TypedDict(
    "_RequiredPostCommentForPullRequestInputRequestTypeDef",
    {
        "pullRequestId": str,
        "repositoryName": str,
        "beforeCommitId": str,
        "afterCommitId": str,
        "content": str,
    },
)
_OptionalPostCommentForPullRequestInputRequestTypeDef = TypedDict(
    "_OptionalPostCommentForPullRequestInputRequestTypeDef",
    {
        "location": LocationTypeDef,
        "clientRequestToken": str,
    },
    total=False,
)


class PostCommentForPullRequestInputRequestTypeDef(
    _RequiredPostCommentForPullRequestInputRequestTypeDef,
    _OptionalPostCommentForPullRequestInputRequestTypeDef,
):
    pass


PostCommentForPullRequestOutputTypeDef = TypedDict(
    "PostCommentForPullRequestOutputTypeDef",
    {
        "repositoryName": str,
        "pullRequestId": str,
        "beforeCommitId": str,
        "afterCommitId": str,
        "beforeBlobId": str,
        "afterBlobId": str,
        "location": LocationTypeDef,
        "comment": CommentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CommitTypeDef = TypedDict(
    "CommitTypeDef",
    {
        "commitId": str,
        "treeId": str,
        "parents": List[str],
        "message": str,
        "author": UserInfoTypeDef,
        "committer": UserInfoTypeDef,
        "additionalData": str,
    },
    total=False,
)

ConflictMetadataTypeDef = TypedDict(
    "ConflictMetadataTypeDef",
    {
        "filePath": str,
        "fileSizes": FileSizesTypeDef,
        "fileModes": FileModesTypeDef,
        "objectTypes": ObjectTypesTypeDef,
        "numberOfConflicts": int,
        "isBinaryFile": IsBinaryFileTypeDef,
        "contentConflict": bool,
        "fileModeConflict": bool,
        "objectTypeConflict": bool,
        "mergeOperations": MergeOperationsTypeDef,
    },
    total=False,
)

ConflictResolutionTypeDef = TypedDict(
    "ConflictResolutionTypeDef",
    {
        "replaceContents": Sequence[ReplaceContentEntryTypeDef],
        "deleteFiles": Sequence[DeleteFileEntryTypeDef],
        "setFileModes": Sequence[SetFileModeEntryTypeDef],
    },
    total=False,
)

CreateCommitOutputTypeDef = TypedDict(
    "CreateCommitOutputTypeDef",
    {
        "commitId": str,
        "treeId": str,
        "filesAdded": List[FileMetadataTypeDef],
        "filesUpdated": List[FileMetadataTypeDef],
        "filesDeleted": List[FileMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreatePullRequestInputRequestTypeDef = TypedDict(
    "_RequiredCreatePullRequestInputRequestTypeDef",
    {
        "title": str,
        "targets": Sequence[TargetTypeDef],
    },
)
_OptionalCreatePullRequestInputRequestTypeDef = TypedDict(
    "_OptionalCreatePullRequestInputRequestTypeDef",
    {
        "description": str,
        "clientRequestToken": str,
    },
    total=False,
)


class CreatePullRequestInputRequestTypeDef(
    _RequiredCreatePullRequestInputRequestTypeDef, _OptionalCreatePullRequestInputRequestTypeDef
):
    pass


_RequiredDescribePullRequestEventsInputDescribePullRequestEventsPaginateTypeDef = TypedDict(
    "_RequiredDescribePullRequestEventsInputDescribePullRequestEventsPaginateTypeDef",
    {
        "pullRequestId": str,
    },
)
_OptionalDescribePullRequestEventsInputDescribePullRequestEventsPaginateTypeDef = TypedDict(
    "_OptionalDescribePullRequestEventsInputDescribePullRequestEventsPaginateTypeDef",
    {
        "pullRequestEventType": PullRequestEventTypeType,
        "actorArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribePullRequestEventsInputDescribePullRequestEventsPaginateTypeDef(
    _RequiredDescribePullRequestEventsInputDescribePullRequestEventsPaginateTypeDef,
    _OptionalDescribePullRequestEventsInputDescribePullRequestEventsPaginateTypeDef,
):
    pass


_RequiredGetCommentsForComparedCommitInputGetCommentsForComparedCommitPaginateTypeDef = TypedDict(
    "_RequiredGetCommentsForComparedCommitInputGetCommentsForComparedCommitPaginateTypeDef",
    {
        "repositoryName": str,
        "afterCommitId": str,
    },
)
_OptionalGetCommentsForComparedCommitInputGetCommentsForComparedCommitPaginateTypeDef = TypedDict(
    "_OptionalGetCommentsForComparedCommitInputGetCommentsForComparedCommitPaginateTypeDef",
    {
        "beforeCommitId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetCommentsForComparedCommitInputGetCommentsForComparedCommitPaginateTypeDef(
    _RequiredGetCommentsForComparedCommitInputGetCommentsForComparedCommitPaginateTypeDef,
    _OptionalGetCommentsForComparedCommitInputGetCommentsForComparedCommitPaginateTypeDef,
):
    pass


_RequiredGetCommentsForPullRequestInputGetCommentsForPullRequestPaginateTypeDef = TypedDict(
    "_RequiredGetCommentsForPullRequestInputGetCommentsForPullRequestPaginateTypeDef",
    {
        "pullRequestId": str,
    },
)
_OptionalGetCommentsForPullRequestInputGetCommentsForPullRequestPaginateTypeDef = TypedDict(
    "_OptionalGetCommentsForPullRequestInputGetCommentsForPullRequestPaginateTypeDef",
    {
        "repositoryName": str,
        "beforeCommitId": str,
        "afterCommitId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetCommentsForPullRequestInputGetCommentsForPullRequestPaginateTypeDef(
    _RequiredGetCommentsForPullRequestInputGetCommentsForPullRequestPaginateTypeDef,
    _OptionalGetCommentsForPullRequestInputGetCommentsForPullRequestPaginateTypeDef,
):
    pass


_RequiredGetDifferencesInputGetDifferencesPaginateTypeDef = TypedDict(
    "_RequiredGetDifferencesInputGetDifferencesPaginateTypeDef",
    {
        "repositoryName": str,
        "afterCommitSpecifier": str,
    },
)
_OptionalGetDifferencesInputGetDifferencesPaginateTypeDef = TypedDict(
    "_OptionalGetDifferencesInputGetDifferencesPaginateTypeDef",
    {
        "beforeCommitSpecifier": str,
        "beforePath": str,
        "afterPath": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetDifferencesInputGetDifferencesPaginateTypeDef(
    _RequiredGetDifferencesInputGetDifferencesPaginateTypeDef,
    _OptionalGetDifferencesInputGetDifferencesPaginateTypeDef,
):
    pass


_RequiredListBranchesInputListBranchesPaginateTypeDef = TypedDict(
    "_RequiredListBranchesInputListBranchesPaginateTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalListBranchesInputListBranchesPaginateTypeDef = TypedDict(
    "_OptionalListBranchesInputListBranchesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListBranchesInputListBranchesPaginateTypeDef(
    _RequiredListBranchesInputListBranchesPaginateTypeDef,
    _OptionalListBranchesInputListBranchesPaginateTypeDef,
):
    pass


_RequiredListPullRequestsInputListPullRequestsPaginateTypeDef = TypedDict(
    "_RequiredListPullRequestsInputListPullRequestsPaginateTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalListPullRequestsInputListPullRequestsPaginateTypeDef = TypedDict(
    "_OptionalListPullRequestsInputListPullRequestsPaginateTypeDef",
    {
        "authorArn": str,
        "pullRequestStatus": PullRequestStatusEnumType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListPullRequestsInputListPullRequestsPaginateTypeDef(
    _RequiredListPullRequestsInputListPullRequestsPaginateTypeDef,
    _OptionalListPullRequestsInputListPullRequestsPaginateTypeDef,
):
    pass


ListRepositoriesInputListRepositoriesPaginateTypeDef = TypedDict(
    "ListRepositoriesInputListRepositoriesPaginateTypeDef",
    {
        "sortBy": SortByEnumType,
        "order": OrderEnumType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

EvaluatePullRequestApprovalRulesOutputTypeDef = TypedDict(
    "EvaluatePullRequestApprovalRulesOutputTypeDef",
    {
        "evaluation": EvaluationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFolderOutputTypeDef = TypedDict(
    "GetFolderOutputTypeDef",
    {
        "commitId": str,
        "folderPath": str,
        "treeId": str,
        "subFolders": List[FolderTypeDef],
        "files": List[FileTypeDef],
        "symbolicLinks": List[SymbolicLinkTypeDef],
        "subModules": List[SubModuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRepositoryTriggersOutputTypeDef = TypedDict(
    "GetRepositoryTriggersOutputTypeDef",
    {
        "configurationId": str,
        "triggers": List[RepositoryTriggerTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutRepositoryTriggersInputRequestTypeDef = TypedDict(
    "PutRepositoryTriggersInputRequestTypeDef",
    {
        "repositoryName": str,
        "triggers": Sequence[RepositoryTriggerTypeDef],
    },
)

TestRepositoryTriggersInputRequestTypeDef = TypedDict(
    "TestRepositoryTriggersInputRequestTypeDef",
    {
        "repositoryName": str,
        "triggers": Sequence[RepositoryTriggerTypeDef],
    },
)

ListRepositoriesOutputTypeDef = TypedDict(
    "ListRepositoriesOutputTypeDef",
    {
        "repositories": List[RepositoryNameIdPairTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MergeHunkTypeDef = TypedDict(
    "MergeHunkTypeDef",
    {
        "isConflict": bool,
        "source": MergeHunkDetailTypeDef,
        "destination": MergeHunkDetailTypeDef,
        "base": MergeHunkDetailTypeDef,
    },
    total=False,
)

PullRequestMergedStateChangedEventMetadataTypeDef = TypedDict(
    "PullRequestMergedStateChangedEventMetadataTypeDef",
    {
        "repositoryName": str,
        "destinationReference": str,
        "mergeMetadata": MergeMetadataTypeDef,
    },
    total=False,
)

PullRequestTargetTypeDef = TypedDict(
    "PullRequestTargetTypeDef",
    {
        "repositoryName": str,
        "sourceReference": str,
        "destinationReference": str,
        "destinationCommit": str,
        "sourceCommit": str,
        "mergeBase": str,
        "mergeMetadata": MergeMetadataTypeDef,
    },
    total=False,
)

_RequiredPutFileEntryTypeDef = TypedDict(
    "_RequiredPutFileEntryTypeDef",
    {
        "filePath": str,
    },
)
_OptionalPutFileEntryTypeDef = TypedDict(
    "_OptionalPutFileEntryTypeDef",
    {
        "fileMode": FileModeTypeEnumType,
        "fileContent": Union[str, bytes, IO[Any], StreamingBody],
        "sourceFile": SourceFileSpecifierTypeDef,
    },
    total=False,
)


class PutFileEntryTypeDef(_RequiredPutFileEntryTypeDef, _OptionalPutFileEntryTypeDef):
    pass


ReactionForCommentTypeDef = TypedDict(
    "ReactionForCommentTypeDef",
    {
        "reaction": ReactionValueFormatsTypeDef,
        "reactionUsers": List[str],
        "reactionsFromDeletedUsersCount": int,
    },
    total=False,
)

TestRepositoryTriggersOutputTypeDef = TypedDict(
    "TestRepositoryTriggersOutputTypeDef",
    {
        "successfulExecutions": List[str],
        "failedExecutions": List[RepositoryTriggerExecutionFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePullRequestApprovalRuleOutputTypeDef = TypedDict(
    "CreatePullRequestApprovalRuleOutputTypeDef",
    {
        "approvalRule": ApprovalRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePullRequestApprovalRuleContentOutputTypeDef = TypedDict(
    "UpdatePullRequestApprovalRuleContentOutputTypeDef",
    {
        "approvalRule": ApprovalRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDifferencesOutputTypeDef = TypedDict(
    "GetDifferencesOutputTypeDef",
    {
        "differences": List[DifferenceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCommentsForComparedCommitOutputTypeDef = TypedDict(
    "GetCommentsForComparedCommitOutputTypeDef",
    {
        "commentsForComparedCommitData": List[CommentsForComparedCommitTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCommentsForPullRequestOutputTypeDef = TypedDict(
    "GetCommentsForPullRequestOutputTypeDef",
    {
        "commentsForPullRequestData": List[CommentsForPullRequestTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetCommitsOutputTypeDef = TypedDict(
    "BatchGetCommitsOutputTypeDef",
    {
        "commits": List[CommitTypeDef],
        "errors": List[BatchGetCommitsErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCommitOutputTypeDef = TypedDict(
    "GetCommitOutputTypeDef",
    {
        "commit": CommitTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMergeConflictsOutputTypeDef = TypedDict(
    "GetMergeConflictsOutputTypeDef",
    {
        "mergeable": bool,
        "destinationCommitId": str,
        "sourceCommitId": str,
        "baseCommitId": str,
        "conflictMetadataList": List[ConflictMetadataTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateUnreferencedMergeCommitInputRequestTypeDef = TypedDict(
    "_RequiredCreateUnreferencedMergeCommitInputRequestTypeDef",
    {
        "repositoryName": str,
        "sourceCommitSpecifier": str,
        "destinationCommitSpecifier": str,
        "mergeOption": MergeOptionTypeEnumType,
    },
)
_OptionalCreateUnreferencedMergeCommitInputRequestTypeDef = TypedDict(
    "_OptionalCreateUnreferencedMergeCommitInputRequestTypeDef",
    {
        "conflictDetailLevel": ConflictDetailLevelTypeEnumType,
        "conflictResolutionStrategy": ConflictResolutionStrategyTypeEnumType,
        "authorName": str,
        "email": str,
        "commitMessage": str,
        "keepEmptyFolders": bool,
        "conflictResolution": ConflictResolutionTypeDef,
    },
    total=False,
)


class CreateUnreferencedMergeCommitInputRequestTypeDef(
    _RequiredCreateUnreferencedMergeCommitInputRequestTypeDef,
    _OptionalCreateUnreferencedMergeCommitInputRequestTypeDef,
):
    pass


_RequiredMergeBranchesBySquashInputRequestTypeDef = TypedDict(
    "_RequiredMergeBranchesBySquashInputRequestTypeDef",
    {
        "repositoryName": str,
        "sourceCommitSpecifier": str,
        "destinationCommitSpecifier": str,
    },
)
_OptionalMergeBranchesBySquashInputRequestTypeDef = TypedDict(
    "_OptionalMergeBranchesBySquashInputRequestTypeDef",
    {
        "targetBranch": str,
        "conflictDetailLevel": ConflictDetailLevelTypeEnumType,
        "conflictResolutionStrategy": ConflictResolutionStrategyTypeEnumType,
        "authorName": str,
        "email": str,
        "commitMessage": str,
        "keepEmptyFolders": bool,
        "conflictResolution": ConflictResolutionTypeDef,
    },
    total=False,
)


class MergeBranchesBySquashInputRequestTypeDef(
    _RequiredMergeBranchesBySquashInputRequestTypeDef,
    _OptionalMergeBranchesBySquashInputRequestTypeDef,
):
    pass


_RequiredMergeBranchesByThreeWayInputRequestTypeDef = TypedDict(
    "_RequiredMergeBranchesByThreeWayInputRequestTypeDef",
    {
        "repositoryName": str,
        "sourceCommitSpecifier": str,
        "destinationCommitSpecifier": str,
    },
)
_OptionalMergeBranchesByThreeWayInputRequestTypeDef = TypedDict(
    "_OptionalMergeBranchesByThreeWayInputRequestTypeDef",
    {
        "targetBranch": str,
        "conflictDetailLevel": ConflictDetailLevelTypeEnumType,
        "conflictResolutionStrategy": ConflictResolutionStrategyTypeEnumType,
        "authorName": str,
        "email": str,
        "commitMessage": str,
        "keepEmptyFolders": bool,
        "conflictResolution": ConflictResolutionTypeDef,
    },
    total=False,
)


class MergeBranchesByThreeWayInputRequestTypeDef(
    _RequiredMergeBranchesByThreeWayInputRequestTypeDef,
    _OptionalMergeBranchesByThreeWayInputRequestTypeDef,
):
    pass


_RequiredMergePullRequestBySquashInputRequestTypeDef = TypedDict(
    "_RequiredMergePullRequestBySquashInputRequestTypeDef",
    {
        "pullRequestId": str,
        "repositoryName": str,
    },
)
_OptionalMergePullRequestBySquashInputRequestTypeDef = TypedDict(
    "_OptionalMergePullRequestBySquashInputRequestTypeDef",
    {
        "sourceCommitId": str,
        "conflictDetailLevel": ConflictDetailLevelTypeEnumType,
        "conflictResolutionStrategy": ConflictResolutionStrategyTypeEnumType,
        "commitMessage": str,
        "authorName": str,
        "email": str,
        "keepEmptyFolders": bool,
        "conflictResolution": ConflictResolutionTypeDef,
    },
    total=False,
)


class MergePullRequestBySquashInputRequestTypeDef(
    _RequiredMergePullRequestBySquashInputRequestTypeDef,
    _OptionalMergePullRequestBySquashInputRequestTypeDef,
):
    pass


_RequiredMergePullRequestByThreeWayInputRequestTypeDef = TypedDict(
    "_RequiredMergePullRequestByThreeWayInputRequestTypeDef",
    {
        "pullRequestId": str,
        "repositoryName": str,
    },
)
_OptionalMergePullRequestByThreeWayInputRequestTypeDef = TypedDict(
    "_OptionalMergePullRequestByThreeWayInputRequestTypeDef",
    {
        "sourceCommitId": str,
        "conflictDetailLevel": ConflictDetailLevelTypeEnumType,
        "conflictResolutionStrategy": ConflictResolutionStrategyTypeEnumType,
        "commitMessage": str,
        "authorName": str,
        "email": str,
        "keepEmptyFolders": bool,
        "conflictResolution": ConflictResolutionTypeDef,
    },
    total=False,
)


class MergePullRequestByThreeWayInputRequestTypeDef(
    _RequiredMergePullRequestByThreeWayInputRequestTypeDef,
    _OptionalMergePullRequestByThreeWayInputRequestTypeDef,
):
    pass


ConflictTypeDef = TypedDict(
    "ConflictTypeDef",
    {
        "conflictMetadata": ConflictMetadataTypeDef,
        "mergeHunks": List[MergeHunkTypeDef],
    },
    total=False,
)

DescribeMergeConflictsOutputTypeDef = TypedDict(
    "DescribeMergeConflictsOutputTypeDef",
    {
        "conflictMetadata": ConflictMetadataTypeDef,
        "mergeHunks": List[MergeHunkTypeDef],
        "nextToken": str,
        "destinationCommitId": str,
        "sourceCommitId": str,
        "baseCommitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PullRequestEventTypeDef = TypedDict(
    "PullRequestEventTypeDef",
    {
        "pullRequestId": str,
        "eventDate": datetime,
        "pullRequestEventType": PullRequestEventTypeType,
        "actorArn": str,
        "pullRequestCreatedEventMetadata": PullRequestCreatedEventMetadataTypeDef,
        "pullRequestStatusChangedEventMetadata": PullRequestStatusChangedEventMetadataTypeDef,
        "pullRequestSourceReferenceUpdatedEventMetadata": PullRequestSourceReferenceUpdatedEventMetadataTypeDef,
        "pullRequestMergedStateChangedEventMetadata": PullRequestMergedStateChangedEventMetadataTypeDef,
        "approvalRuleEventMetadata": ApprovalRuleEventMetadataTypeDef,
        "approvalStateChangedEventMetadata": ApprovalStateChangedEventMetadataTypeDef,
        "approvalRuleOverriddenEventMetadata": ApprovalRuleOverriddenEventMetadataTypeDef,
    },
    total=False,
)

PullRequestTypeDef = TypedDict(
    "PullRequestTypeDef",
    {
        "pullRequestId": str,
        "title": str,
        "description": str,
        "lastActivityDate": datetime,
        "creationDate": datetime,
        "pullRequestStatus": PullRequestStatusEnumType,
        "authorArn": str,
        "pullRequestTargets": List[PullRequestTargetTypeDef],
        "clientRequestToken": str,
        "revisionId": str,
        "approvalRules": List[ApprovalRuleTypeDef],
    },
    total=False,
)

_RequiredCreateCommitInputRequestTypeDef = TypedDict(
    "_RequiredCreateCommitInputRequestTypeDef",
    {
        "repositoryName": str,
        "branchName": str,
    },
)
_OptionalCreateCommitInputRequestTypeDef = TypedDict(
    "_OptionalCreateCommitInputRequestTypeDef",
    {
        "parentCommitId": str,
        "authorName": str,
        "email": str,
        "commitMessage": str,
        "keepEmptyFolders": bool,
        "putFiles": Sequence[PutFileEntryTypeDef],
        "deleteFiles": Sequence[DeleteFileEntryTypeDef],
        "setFileModes": Sequence[SetFileModeEntryTypeDef],
    },
    total=False,
)


class CreateCommitInputRequestTypeDef(
    _RequiredCreateCommitInputRequestTypeDef, _OptionalCreateCommitInputRequestTypeDef
):
    pass


GetCommentReactionsOutputTypeDef = TypedDict(
    "GetCommentReactionsOutputTypeDef",
    {
        "reactionsForComment": List[ReactionForCommentTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDescribeMergeConflictsOutputTypeDef = TypedDict(
    "BatchDescribeMergeConflictsOutputTypeDef",
    {
        "conflicts": List[ConflictTypeDef],
        "nextToken": str,
        "errors": List[BatchDescribeMergeConflictsErrorTypeDef],
        "destinationCommitId": str,
        "sourceCommitId": str,
        "baseCommitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePullRequestEventsOutputTypeDef = TypedDict(
    "DescribePullRequestEventsOutputTypeDef",
    {
        "pullRequestEvents": List[PullRequestEventTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePullRequestOutputTypeDef = TypedDict(
    "CreatePullRequestOutputTypeDef",
    {
        "pullRequest": PullRequestTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPullRequestOutputTypeDef = TypedDict(
    "GetPullRequestOutputTypeDef",
    {
        "pullRequest": PullRequestTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MergePullRequestByFastForwardOutputTypeDef = TypedDict(
    "MergePullRequestByFastForwardOutputTypeDef",
    {
        "pullRequest": PullRequestTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MergePullRequestBySquashOutputTypeDef = TypedDict(
    "MergePullRequestBySquashOutputTypeDef",
    {
        "pullRequest": PullRequestTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MergePullRequestByThreeWayOutputTypeDef = TypedDict(
    "MergePullRequestByThreeWayOutputTypeDef",
    {
        "pullRequest": PullRequestTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePullRequestDescriptionOutputTypeDef = TypedDict(
    "UpdatePullRequestDescriptionOutputTypeDef",
    {
        "pullRequest": PullRequestTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePullRequestStatusOutputTypeDef = TypedDict(
    "UpdatePullRequestStatusOutputTypeDef",
    {
        "pullRequest": PullRequestTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePullRequestTitleOutputTypeDef = TypedDict(
    "UpdatePullRequestTitleOutputTypeDef",
    {
        "pullRequest": PullRequestTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
