"""
Type annotations for gamesparks service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_gamesparks.client import GameSparksClient
    from mypy_boto3_gamesparks.paginator import (
        ListExtensionVersionsPaginator,
        ListExtensionsPaginator,
        ListGamesPaginator,
        ListGeneratedCodeJobsPaginator,
        ListSnapshotsPaginator,
        ListStageDeploymentsPaginator,
        ListStagesPaginator,
    )

    session = Session()
    client: GameSparksClient = session.client("gamesparks")

    list_extension_versions_paginator: ListExtensionVersionsPaginator = client.get_paginator("list_extension_versions")
    list_extensions_paginator: ListExtensionsPaginator = client.get_paginator("list_extensions")
    list_games_paginator: ListGamesPaginator = client.get_paginator("list_games")
    list_generated_code_jobs_paginator: ListGeneratedCodeJobsPaginator = client.get_paginator("list_generated_code_jobs")
    list_snapshots_paginator: ListSnapshotsPaginator = client.get_paginator("list_snapshots")
    list_stage_deployments_paginator: ListStageDeploymentsPaginator = client.get_paginator("list_stage_deployments")
    list_stages_paginator: ListStagesPaginator = client.get_paginator("list_stages")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListExtensionsResultTypeDef,
    ListExtensionVersionsResultTypeDef,
    ListGamesResultTypeDef,
    ListGeneratedCodeJobsResultTypeDef,
    ListSnapshotsResultTypeDef,
    ListStageDeploymentsResultTypeDef,
    ListStagesResultTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListExtensionVersionsPaginator",
    "ListExtensionsPaginator",
    "ListGamesPaginator",
    "ListGeneratedCodeJobsPaginator",
    "ListSnapshotsPaginator",
    "ListStageDeploymentsPaginator",
    "ListStagesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListExtensionVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Paginator.ListExtensionVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/paginators/#listextensionversionspaginator)
    """

    def paginate(
        self, *, Name: str, Namespace: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListExtensionVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Paginator.ListExtensionVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/paginators/#listextensionversionspaginator)
        """


class ListExtensionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Paginator.ListExtensions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/paginators/#listextensionspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListExtensionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Paginator.ListExtensions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/paginators/#listextensionspaginator)
        """


class ListGamesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Paginator.ListGames)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/paginators/#listgamespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListGamesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Paginator.ListGames.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/paginators/#listgamespaginator)
        """


class ListGeneratedCodeJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Paginator.ListGeneratedCodeJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/paginators/#listgeneratedcodejobspaginator)
    """

    def paginate(
        self, *, GameName: str, SnapshotId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListGeneratedCodeJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Paginator.ListGeneratedCodeJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/paginators/#listgeneratedcodejobspaginator)
        """


class ListSnapshotsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Paginator.ListSnapshots)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/paginators/#listsnapshotspaginator)
    """

    def paginate(
        self, *, GameName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSnapshotsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Paginator.ListSnapshots.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/paginators/#listsnapshotspaginator)
        """


class ListStageDeploymentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Paginator.ListStageDeployments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/paginators/#liststagedeploymentspaginator)
    """

    def paginate(
        self, *, GameName: str, StageName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListStageDeploymentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Paginator.ListStageDeployments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/paginators/#liststagedeploymentspaginator)
        """


class ListStagesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Paginator.ListStages)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/paginators/#liststagespaginator)
    """

    def paginate(
        self, *, GameName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListStagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Paginator.ListStages.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamesparks/paginators/#liststagespaginator)
        """
