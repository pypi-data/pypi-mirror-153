"""
Type annotations for codedeploy service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codedeploy.client import CodeDeployClient
    from mypy_boto3_codedeploy.paginator import (
        ListApplicationRevisionsPaginator,
        ListApplicationsPaginator,
        ListDeploymentConfigsPaginator,
        ListDeploymentGroupsPaginator,
        ListDeploymentInstancesPaginator,
        ListDeploymentTargetsPaginator,
        ListDeploymentsPaginator,
        ListGitHubAccountTokenNamesPaginator,
        ListOnPremisesInstancesPaginator,
    )

    session = Session()
    client: CodeDeployClient = session.client("codedeploy")

    list_application_revisions_paginator: ListApplicationRevisionsPaginator = client.get_paginator("list_application_revisions")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_deployment_configs_paginator: ListDeploymentConfigsPaginator = client.get_paginator("list_deployment_configs")
    list_deployment_groups_paginator: ListDeploymentGroupsPaginator = client.get_paginator("list_deployment_groups")
    list_deployment_instances_paginator: ListDeploymentInstancesPaginator = client.get_paginator("list_deployment_instances")
    list_deployment_targets_paginator: ListDeploymentTargetsPaginator = client.get_paginator("list_deployment_targets")
    list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
    list_git_hub_account_token_names_paginator: ListGitHubAccountTokenNamesPaginator = client.get_paginator("list_git_hub_account_token_names")
    list_on_premises_instances_paginator: ListOnPremisesInstancesPaginator = client.get_paginator("list_on_premises_instances")
    ```
"""
from typing import Generic, Iterator, Mapping, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    ApplicationRevisionSortByType,
    DeploymentStatusType,
    InstanceStatusType,
    InstanceTypeType,
    ListStateFilterActionType,
    RegistrationStatusType,
    SortOrderType,
    TargetFilterNameType,
)
from .type_defs import (
    ListApplicationRevisionsOutputTypeDef,
    ListApplicationsOutputTypeDef,
    ListDeploymentConfigsOutputTypeDef,
    ListDeploymentGroupsOutputTypeDef,
    ListDeploymentInstancesOutputTypeDef,
    ListDeploymentsOutputTypeDef,
    ListDeploymentTargetsOutputTypeDef,
    ListGitHubAccountTokenNamesOutputTypeDef,
    ListOnPremisesInstancesOutputTypeDef,
    PaginatorConfigTypeDef,
    TagFilterTypeDef,
    TimeRangeTypeDef,
)

__all__ = (
    "ListApplicationRevisionsPaginator",
    "ListApplicationsPaginator",
    "ListDeploymentConfigsPaginator",
    "ListDeploymentGroupsPaginator",
    "ListDeploymentInstancesPaginator",
    "ListDeploymentTargetsPaginator",
    "ListDeploymentsPaginator",
    "ListGitHubAccountTokenNamesPaginator",
    "ListOnPremisesInstancesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApplicationRevisionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListApplicationRevisions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listapplicationrevisionspaginator)
    """

    def paginate(
        self,
        *,
        applicationName: str,
        sortBy: ApplicationRevisionSortByType = ...,
        sortOrder: SortOrderType = ...,
        s3Bucket: str = ...,
        s3KeyPrefix: str = ...,
        deployed: ListStateFilterActionType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListApplicationRevisionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListApplicationRevisions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listapplicationrevisionspaginator)
        """


class ListApplicationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListApplications)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listapplicationspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListApplicationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListApplications.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listapplicationspaginator)
        """


class ListDeploymentConfigsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentConfigs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentconfigspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeploymentConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentConfigs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentconfigspaginator)
        """


class ListDeploymentGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentgroupspaginator)
    """

    def paginate(
        self, *, applicationName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeploymentGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentgroupspaginator)
        """


class ListDeploymentInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentInstances)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentinstancespaginator)
    """

    def paginate(
        self,
        *,
        deploymentId: str,
        instanceStatusFilter: Sequence[InstanceStatusType] = ...,
        instanceTypeFilter: Sequence[InstanceTypeType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeploymentInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentInstances.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentinstancespaginator)
        """


class ListDeploymentTargetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentTargets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymenttargetspaginator)
    """

    def paginate(
        self,
        *,
        deploymentId: str = ...,
        targetFilters: Mapping[TargetFilterNameType, Sequence[str]] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeploymentTargetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentTargets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymenttargetspaginator)
        """


class ListDeploymentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeployments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentspaginator)
    """

    def paginate(
        self,
        *,
        applicationName: str = ...,
        deploymentGroupName: str = ...,
        externalId: str = ...,
        includeOnlyStatuses: Sequence[DeploymentStatusType] = ...,
        createTimeRange: TimeRangeTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeploymentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeployments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentspaginator)
        """


class ListGitHubAccountTokenNamesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListGitHubAccountTokenNames)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listgithubaccounttokennamespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListGitHubAccountTokenNamesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListGitHubAccountTokenNames.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listgithubaccounttokennamespaginator)
        """


class ListOnPremisesInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListOnPremisesInstances)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listonpremisesinstancespaginator)
    """

    def paginate(
        self,
        *,
        registrationStatus: RegistrationStatusType = ...,
        tagFilters: Sequence[TagFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOnPremisesInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListOnPremisesInstances.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listonpremisesinstancespaginator)
        """
