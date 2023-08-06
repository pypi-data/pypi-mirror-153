"""
Type annotations for codestar service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_codestar.client import CodeStarClient

    session = Session()
    client: CodeStarClient = session.client("codestar")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListProjectsPaginator,
    ListResourcesPaginator,
    ListTeamMembersPaginator,
    ListUserProfilesPaginator,
)
from .type_defs import (
    AssociateTeamMemberResultTypeDef,
    CodeTypeDef,
    CreateProjectResultTypeDef,
    CreateUserProfileResultTypeDef,
    DeleteProjectResultTypeDef,
    DeleteUserProfileResultTypeDef,
    DescribeProjectResultTypeDef,
    DescribeUserProfileResultTypeDef,
    ListProjectsResultTypeDef,
    ListResourcesResultTypeDef,
    ListTagsForProjectResultTypeDef,
    ListTeamMembersResultTypeDef,
    ListUserProfilesResultTypeDef,
    TagProjectResultTypeDef,
    ToolchainTypeDef,
    UpdateTeamMemberResultTypeDef,
    UpdateUserProfileResultTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CodeStarClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidServiceRoleException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ProjectAlreadyExistsException: Type[BotocoreClientError]
    ProjectConfigurationException: Type[BotocoreClientError]
    ProjectCreationFailedException: Type[BotocoreClientError]
    ProjectNotFoundException: Type[BotocoreClientError]
    TeamMemberAlreadyAssociatedException: Type[BotocoreClientError]
    TeamMemberNotFoundException: Type[BotocoreClientError]
    UserProfileAlreadyExistsException: Type[BotocoreClientError]
    UserProfileNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CodeStarClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeStarClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#exceptions)
        """

    def associate_team_member(
        self,
        *,
        projectId: str,
        userArn: str,
        projectRole: str,
        clientRequestToken: str = ...,
        remoteAccessAllowed: bool = ...
    ) -> AssociateTeamMemberResultTypeDef:
        """
        Adds an IAM user to the team for an AWS CodeStar project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.associate_team_member)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#associate_team_member)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#can_paginate)
        """

    def create_project(
        self,
        *,
        name: str,
        id: str,
        description: str = ...,
        clientRequestToken: str = ...,
        sourceCode: Sequence[CodeTypeDef] = ...,
        toolchain: ToolchainTypeDef = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateProjectResultTypeDef:
        """
        Creates a project, including project resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.create_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#create_project)
        """

    def create_user_profile(
        self, *, userArn: str, displayName: str, emailAddress: str, sshPublicKey: str = ...
    ) -> CreateUserProfileResultTypeDef:
        """
        Creates a profile for a user that includes user preferences, such as the display
        name and email address assocciated with the user, in AWS CodeStar.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.create_user_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#create_user_profile)
        """

    def delete_project(
        self, *, id: str, clientRequestToken: str = ..., deleteStack: bool = ...
    ) -> DeleteProjectResultTypeDef:
        """
        Deletes a project, including project resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.delete_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#delete_project)
        """

    def delete_user_profile(self, *, userArn: str) -> DeleteUserProfileResultTypeDef:
        """
        Deletes a user profile in AWS CodeStar, including all personal preference data
        associated with that profile, such as display name and email address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.delete_user_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#delete_user_profile)
        """

    def describe_project(self, *, id: str) -> DescribeProjectResultTypeDef:
        """
        Describes a project and its resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.describe_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#describe_project)
        """

    def describe_user_profile(self, *, userArn: str) -> DescribeUserProfileResultTypeDef:
        """
        Describes a user in AWS CodeStar and the user attributes across all projects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.describe_user_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#describe_user_profile)
        """

    def disassociate_team_member(self, *, projectId: str, userArn: str) -> Dict[str, Any]:
        """
        Removes a user from a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.disassociate_team_member)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#disassociate_team_member)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#generate_presigned_url)
        """

    def list_projects(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListProjectsResultTypeDef:
        """
        Lists all projects in AWS CodeStar associated with your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.list_projects)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#list_projects)
        """

    def list_resources(
        self, *, projectId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListResourcesResultTypeDef:
        """
        Lists resources associated with a project in AWS CodeStar.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.list_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#list_resources)
        """

    def list_tags_for_project(
        self, *, id: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListTagsForProjectResultTypeDef:
        """
        Gets the tags for a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.list_tags_for_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#list_tags_for_project)
        """

    def list_team_members(
        self, *, projectId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListTeamMembersResultTypeDef:
        """
        Lists all team members associated with a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.list_team_members)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#list_team_members)
        """

    def list_user_profiles(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListUserProfilesResultTypeDef:
        """
        Lists all the user profiles configured for your AWS account in AWS CodeStar.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.list_user_profiles)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#list_user_profiles)
        """

    def tag_project(self, *, id: str, tags: Mapping[str, str]) -> TagProjectResultTypeDef:
        """
        Adds tags to a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.tag_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#tag_project)
        """

    def untag_project(self, *, id: str, tags: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.untag_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#untag_project)
        """

    def update_project(self, *, id: str, name: str = ..., description: str = ...) -> Dict[str, Any]:
        """
        Updates a project in AWS CodeStar.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.update_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#update_project)
        """

    def update_team_member(
        self,
        *,
        projectId: str,
        userArn: str,
        projectRole: str = ...,
        remoteAccessAllowed: bool = ...
    ) -> UpdateTeamMemberResultTypeDef:
        """
        Updates a team member's attributes in an AWS CodeStar project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.update_team_member)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#update_team_member)
        """

    def update_user_profile(
        self,
        *,
        userArn: str,
        displayName: str = ...,
        emailAddress: str = ...,
        sshPublicKey: str = ...
    ) -> UpdateUserProfileResultTypeDef:
        """
        Updates a user's profile in AWS CodeStar.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.update_user_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#update_user_profile)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_resources"]) -> ListResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_team_members"]
    ) -> ListTeamMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_user_profiles"]
    ) -> ListUserProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar/client/#get_paginator)
        """
