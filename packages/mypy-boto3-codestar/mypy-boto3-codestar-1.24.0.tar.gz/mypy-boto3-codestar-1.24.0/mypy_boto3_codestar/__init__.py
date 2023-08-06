"""
Main interface for codestar service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_codestar import (
        Client,
        CodeStarClient,
        ListProjectsPaginator,
        ListResourcesPaginator,
        ListTeamMembersPaginator,
        ListUserProfilesPaginator,
    )

    session = Session()
    client: CodeStarClient = session.client("codestar")

    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
    list_team_members_paginator: ListTeamMembersPaginator = client.get_paginator("list_team_members")
    list_user_profiles_paginator: ListUserProfilesPaginator = client.get_paginator("list_user_profiles")
    ```
"""
from .client import CodeStarClient
from .paginator import (
    ListProjectsPaginator,
    ListResourcesPaginator,
    ListTeamMembersPaginator,
    ListUserProfilesPaginator,
)

Client = CodeStarClient


__all__ = (
    "Client",
    "CodeStarClient",
    "ListProjectsPaginator",
    "ListResourcesPaginator",
    "ListTeamMembersPaginator",
    "ListUserProfilesPaginator",
)
