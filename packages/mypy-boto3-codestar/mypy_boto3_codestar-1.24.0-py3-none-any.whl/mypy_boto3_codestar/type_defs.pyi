"""
Type annotations for codestar service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/type_defs/)

Usage::

    ```python
    from mypy_boto3_codestar.type_defs import AssociateTeamMemberRequestRequestTypeDef

    data: AssociateTeamMemberRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AssociateTeamMemberRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CodeCommitCodeDestinationTypeDef",
    "GitHubCodeDestinationTypeDef",
    "S3LocationTypeDef",
    "CreateUserProfileRequestRequestTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteUserProfileRequestRequestTypeDef",
    "DescribeProjectRequestRequestTypeDef",
    "ProjectStatusTypeDef",
    "DescribeUserProfileRequestRequestTypeDef",
    "DisassociateTeamMemberRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ProjectSummaryTypeDef",
    "ListResourcesRequestRequestTypeDef",
    "ResourceTypeDef",
    "ListTagsForProjectRequestRequestTypeDef",
    "ListTeamMembersRequestRequestTypeDef",
    "TeamMemberTypeDef",
    "ListUserProfilesRequestRequestTypeDef",
    "UserProfileSummaryTypeDef",
    "TagProjectRequestRequestTypeDef",
    "UntagProjectRequestRequestTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "UpdateTeamMemberRequestRequestTypeDef",
    "UpdateUserProfileRequestRequestTypeDef",
    "AssociateTeamMemberResultTypeDef",
    "CreateProjectResultTypeDef",
    "CreateUserProfileResultTypeDef",
    "DeleteProjectResultTypeDef",
    "DeleteUserProfileResultTypeDef",
    "DescribeUserProfileResultTypeDef",
    "ListTagsForProjectResultTypeDef",
    "TagProjectResultTypeDef",
    "UpdateTeamMemberResultTypeDef",
    "UpdateUserProfileResultTypeDef",
    "CodeDestinationTypeDef",
    "CodeSourceTypeDef",
    "ToolchainSourceTypeDef",
    "DescribeProjectResultTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListResourcesRequestListResourcesPaginateTypeDef",
    "ListTeamMembersRequestListTeamMembersPaginateTypeDef",
    "ListUserProfilesRequestListUserProfilesPaginateTypeDef",
    "ListProjectsResultTypeDef",
    "ListResourcesResultTypeDef",
    "ListTeamMembersResultTypeDef",
    "ListUserProfilesResultTypeDef",
    "CodeTypeDef",
    "ToolchainTypeDef",
    "CreateProjectRequestRequestTypeDef",
)

_RequiredAssociateTeamMemberRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateTeamMemberRequestRequestTypeDef",
    {
        "projectId": str,
        "userArn": str,
        "projectRole": str,
    },
)
_OptionalAssociateTeamMemberRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateTeamMemberRequestRequestTypeDef",
    {
        "clientRequestToken": str,
        "remoteAccessAllowed": bool,
    },
    total=False,
)

class AssociateTeamMemberRequestRequestTypeDef(
    _RequiredAssociateTeamMemberRequestRequestTypeDef,
    _OptionalAssociateTeamMemberRequestRequestTypeDef,
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

CodeCommitCodeDestinationTypeDef = TypedDict(
    "CodeCommitCodeDestinationTypeDef",
    {
        "name": str,
    },
)

_RequiredGitHubCodeDestinationTypeDef = TypedDict(
    "_RequiredGitHubCodeDestinationTypeDef",
    {
        "name": str,
        "type": str,
        "owner": str,
        "privateRepository": bool,
        "issuesEnabled": bool,
        "token": str,
    },
)
_OptionalGitHubCodeDestinationTypeDef = TypedDict(
    "_OptionalGitHubCodeDestinationTypeDef",
    {
        "description": str,
    },
    total=False,
)

class GitHubCodeDestinationTypeDef(
    _RequiredGitHubCodeDestinationTypeDef, _OptionalGitHubCodeDestinationTypeDef
):
    pass

S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef",
    {
        "bucketName": str,
        "bucketKey": str,
    },
    total=False,
)

_RequiredCreateUserProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserProfileRequestRequestTypeDef",
    {
        "userArn": str,
        "displayName": str,
        "emailAddress": str,
    },
)
_OptionalCreateUserProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserProfileRequestRequestTypeDef",
    {
        "sshPublicKey": str,
    },
    total=False,
)

class CreateUserProfileRequestRequestTypeDef(
    _RequiredCreateUserProfileRequestRequestTypeDef, _OptionalCreateUserProfileRequestRequestTypeDef
):
    pass

_RequiredDeleteProjectRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteProjectRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalDeleteProjectRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteProjectRequestRequestTypeDef",
    {
        "clientRequestToken": str,
        "deleteStack": bool,
    },
    total=False,
)

class DeleteProjectRequestRequestTypeDef(
    _RequiredDeleteProjectRequestRequestTypeDef, _OptionalDeleteProjectRequestRequestTypeDef
):
    pass

DeleteUserProfileRequestRequestTypeDef = TypedDict(
    "DeleteUserProfileRequestRequestTypeDef",
    {
        "userArn": str,
    },
)

DescribeProjectRequestRequestTypeDef = TypedDict(
    "DescribeProjectRequestRequestTypeDef",
    {
        "id": str,
    },
)

_RequiredProjectStatusTypeDef = TypedDict(
    "_RequiredProjectStatusTypeDef",
    {
        "state": str,
    },
)
_OptionalProjectStatusTypeDef = TypedDict(
    "_OptionalProjectStatusTypeDef",
    {
        "reason": str,
    },
    total=False,
)

class ProjectStatusTypeDef(_RequiredProjectStatusTypeDef, _OptionalProjectStatusTypeDef):
    pass

DescribeUserProfileRequestRequestTypeDef = TypedDict(
    "DescribeUserProfileRequestRequestTypeDef",
    {
        "userArn": str,
    },
)

DisassociateTeamMemberRequestRequestTypeDef = TypedDict(
    "DisassociateTeamMemberRequestRequestTypeDef",
    {
        "projectId": str,
        "userArn": str,
    },
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

ListProjectsRequestRequestTypeDef = TypedDict(
    "ListProjectsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ProjectSummaryTypeDef = TypedDict(
    "ProjectSummaryTypeDef",
    {
        "projectId": str,
        "projectArn": str,
    },
    total=False,
)

_RequiredListResourcesRequestRequestTypeDef = TypedDict(
    "_RequiredListResourcesRequestRequestTypeDef",
    {
        "projectId": str,
    },
)
_OptionalListResourcesRequestRequestTypeDef = TypedDict(
    "_OptionalListResourcesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListResourcesRequestRequestTypeDef(
    _RequiredListResourcesRequestRequestTypeDef, _OptionalListResourcesRequestRequestTypeDef
):
    pass

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "id": str,
    },
)

_RequiredListTagsForProjectRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsForProjectRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalListTagsForProjectRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForProjectRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListTagsForProjectRequestRequestTypeDef(
    _RequiredListTagsForProjectRequestRequestTypeDef,
    _OptionalListTagsForProjectRequestRequestTypeDef,
):
    pass

_RequiredListTeamMembersRequestRequestTypeDef = TypedDict(
    "_RequiredListTeamMembersRequestRequestTypeDef",
    {
        "projectId": str,
    },
)
_OptionalListTeamMembersRequestRequestTypeDef = TypedDict(
    "_OptionalListTeamMembersRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListTeamMembersRequestRequestTypeDef(
    _RequiredListTeamMembersRequestRequestTypeDef, _OptionalListTeamMembersRequestRequestTypeDef
):
    pass

_RequiredTeamMemberTypeDef = TypedDict(
    "_RequiredTeamMemberTypeDef",
    {
        "userArn": str,
        "projectRole": str,
    },
)
_OptionalTeamMemberTypeDef = TypedDict(
    "_OptionalTeamMemberTypeDef",
    {
        "remoteAccessAllowed": bool,
    },
    total=False,
)

class TeamMemberTypeDef(_RequiredTeamMemberTypeDef, _OptionalTeamMemberTypeDef):
    pass

ListUserProfilesRequestRequestTypeDef = TypedDict(
    "ListUserProfilesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

UserProfileSummaryTypeDef = TypedDict(
    "UserProfileSummaryTypeDef",
    {
        "userArn": str,
        "displayName": str,
        "emailAddress": str,
        "sshPublicKey": str,
    },
    total=False,
)

TagProjectRequestRequestTypeDef = TypedDict(
    "TagProjectRequestRequestTypeDef",
    {
        "id": str,
        "tags": Mapping[str, str],
    },
)

UntagProjectRequestRequestTypeDef = TypedDict(
    "UntagProjectRequestRequestTypeDef",
    {
        "id": str,
        "tags": Sequence[str],
    },
)

_RequiredUpdateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateProjectRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalUpdateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateProjectRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
    },
    total=False,
)

class UpdateProjectRequestRequestTypeDef(
    _RequiredUpdateProjectRequestRequestTypeDef, _OptionalUpdateProjectRequestRequestTypeDef
):
    pass

_RequiredUpdateTeamMemberRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTeamMemberRequestRequestTypeDef",
    {
        "projectId": str,
        "userArn": str,
    },
)
_OptionalUpdateTeamMemberRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTeamMemberRequestRequestTypeDef",
    {
        "projectRole": str,
        "remoteAccessAllowed": bool,
    },
    total=False,
)

class UpdateTeamMemberRequestRequestTypeDef(
    _RequiredUpdateTeamMemberRequestRequestTypeDef, _OptionalUpdateTeamMemberRequestRequestTypeDef
):
    pass

_RequiredUpdateUserProfileRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateUserProfileRequestRequestTypeDef",
    {
        "userArn": str,
    },
)
_OptionalUpdateUserProfileRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateUserProfileRequestRequestTypeDef",
    {
        "displayName": str,
        "emailAddress": str,
        "sshPublicKey": str,
    },
    total=False,
)

class UpdateUserProfileRequestRequestTypeDef(
    _RequiredUpdateUserProfileRequestRequestTypeDef, _OptionalUpdateUserProfileRequestRequestTypeDef
):
    pass

AssociateTeamMemberResultTypeDef = TypedDict(
    "AssociateTeamMemberResultTypeDef",
    {
        "clientRequestToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateProjectResultTypeDef = TypedDict(
    "CreateProjectResultTypeDef",
    {
        "id": str,
        "arn": str,
        "clientRequestToken": str,
        "projectTemplateId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUserProfileResultTypeDef = TypedDict(
    "CreateUserProfileResultTypeDef",
    {
        "userArn": str,
        "displayName": str,
        "emailAddress": str,
        "sshPublicKey": str,
        "createdTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteProjectResultTypeDef = TypedDict(
    "DeleteProjectResultTypeDef",
    {
        "stackId": str,
        "projectArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteUserProfileResultTypeDef = TypedDict(
    "DeleteUserProfileResultTypeDef",
    {
        "userArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUserProfileResultTypeDef = TypedDict(
    "DescribeUserProfileResultTypeDef",
    {
        "userArn": str,
        "displayName": str,
        "emailAddress": str,
        "sshPublicKey": str,
        "createdTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForProjectResultTypeDef = TypedDict(
    "ListTagsForProjectResultTypeDef",
    {
        "tags": Dict[str, str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagProjectResultTypeDef = TypedDict(
    "TagProjectResultTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTeamMemberResultTypeDef = TypedDict(
    "UpdateTeamMemberResultTypeDef",
    {
        "userArn": str,
        "projectRole": str,
        "remoteAccessAllowed": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateUserProfileResultTypeDef = TypedDict(
    "UpdateUserProfileResultTypeDef",
    {
        "userArn": str,
        "displayName": str,
        "emailAddress": str,
        "sshPublicKey": str,
        "createdTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CodeDestinationTypeDef = TypedDict(
    "CodeDestinationTypeDef",
    {
        "codeCommit": CodeCommitCodeDestinationTypeDef,
        "gitHub": GitHubCodeDestinationTypeDef,
    },
    total=False,
)

CodeSourceTypeDef = TypedDict(
    "CodeSourceTypeDef",
    {
        "s3": S3LocationTypeDef,
    },
)

ToolchainSourceTypeDef = TypedDict(
    "ToolchainSourceTypeDef",
    {
        "s3": S3LocationTypeDef,
    },
)

DescribeProjectResultTypeDef = TypedDict(
    "DescribeProjectResultTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "description": str,
        "clientRequestToken": str,
        "createdTimeStamp": datetime,
        "stackId": str,
        "projectTemplateId": str,
        "status": ProjectStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "ListProjectsRequestListProjectsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListResourcesRequestListResourcesPaginateTypeDef = TypedDict(
    "_RequiredListResourcesRequestListResourcesPaginateTypeDef",
    {
        "projectId": str,
    },
)
_OptionalListResourcesRequestListResourcesPaginateTypeDef = TypedDict(
    "_OptionalListResourcesRequestListResourcesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListResourcesRequestListResourcesPaginateTypeDef(
    _RequiredListResourcesRequestListResourcesPaginateTypeDef,
    _OptionalListResourcesRequestListResourcesPaginateTypeDef,
):
    pass

_RequiredListTeamMembersRequestListTeamMembersPaginateTypeDef = TypedDict(
    "_RequiredListTeamMembersRequestListTeamMembersPaginateTypeDef",
    {
        "projectId": str,
    },
)
_OptionalListTeamMembersRequestListTeamMembersPaginateTypeDef = TypedDict(
    "_OptionalListTeamMembersRequestListTeamMembersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListTeamMembersRequestListTeamMembersPaginateTypeDef(
    _RequiredListTeamMembersRequestListTeamMembersPaginateTypeDef,
    _OptionalListTeamMembersRequestListTeamMembersPaginateTypeDef,
):
    pass

ListUserProfilesRequestListUserProfilesPaginateTypeDef = TypedDict(
    "ListUserProfilesRequestListUserProfilesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListProjectsResultTypeDef = TypedDict(
    "ListProjectsResultTypeDef",
    {
        "projects": List[ProjectSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResourcesResultTypeDef = TypedDict(
    "ListResourcesResultTypeDef",
    {
        "resources": List[ResourceTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTeamMembersResultTypeDef = TypedDict(
    "ListTeamMembersResultTypeDef",
    {
        "teamMembers": List[TeamMemberTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUserProfilesResultTypeDef = TypedDict(
    "ListUserProfilesResultTypeDef",
    {
        "userProfiles": List[UserProfileSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CodeTypeDef = TypedDict(
    "CodeTypeDef",
    {
        "source": CodeSourceTypeDef,
        "destination": CodeDestinationTypeDef,
    },
)

_RequiredToolchainTypeDef = TypedDict(
    "_RequiredToolchainTypeDef",
    {
        "source": ToolchainSourceTypeDef,
    },
)
_OptionalToolchainTypeDef = TypedDict(
    "_OptionalToolchainTypeDef",
    {
        "roleArn": str,
        "stackParameters": Mapping[str, str],
    },
    total=False,
)

class ToolchainTypeDef(_RequiredToolchainTypeDef, _OptionalToolchainTypeDef):
    pass

_RequiredCreateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProjectRequestRequestTypeDef",
    {
        "name": str,
        "id": str,
    },
)
_OptionalCreateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProjectRequestRequestTypeDef",
    {
        "description": str,
        "clientRequestToken": str,
        "sourceCode": Sequence[CodeTypeDef],
        "toolchain": ToolchainTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateProjectRequestRequestTypeDef(
    _RequiredCreateProjectRequestRequestTypeDef, _OptionalCreateProjectRequestRequestTypeDef
):
    pass
