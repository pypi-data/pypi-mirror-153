"""
Type annotations for guardduty service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_guardduty.client import GuardDutyClient
    from mypy_boto3_guardduty.paginator import (
        ListDetectorsPaginator,
        ListFiltersPaginator,
        ListFindingsPaginator,
        ListIPSetsPaginator,
        ListInvitationsPaginator,
        ListMembersPaginator,
        ListOrganizationAdminAccountsPaginator,
        ListThreatIntelSetsPaginator,
    )

    session = Session()
    client: GuardDutyClient = session.client("guardduty")

    list_detectors_paginator: ListDetectorsPaginator = client.get_paginator("list_detectors")
    list_filters_paginator: ListFiltersPaginator = client.get_paginator("list_filters")
    list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
    list_ip_sets_paginator: ListIPSetsPaginator = client.get_paginator("list_ip_sets")
    list_invitations_paginator: ListInvitationsPaginator = client.get_paginator("list_invitations")
    list_members_paginator: ListMembersPaginator = client.get_paginator("list_members")
    list_organization_admin_accounts_paginator: ListOrganizationAdminAccountsPaginator = client.get_paginator("list_organization_admin_accounts")
    list_threat_intel_sets_paginator: ListThreatIntelSetsPaginator = client.get_paginator("list_threat_intel_sets")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    FindingCriteriaTypeDef,
    ListDetectorsResponseTypeDef,
    ListFiltersResponseTypeDef,
    ListFindingsResponseTypeDef,
    ListInvitationsResponseTypeDef,
    ListIPSetsResponseTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    ListThreatIntelSetsResponseTypeDef,
    PaginatorConfigTypeDef,
    SortCriteriaTypeDef,
)

__all__ = (
    "ListDetectorsPaginator",
    "ListFiltersPaginator",
    "ListFindingsPaginator",
    "ListIPSetsPaginator",
    "ListInvitationsPaginator",
    "ListMembersPaginator",
    "ListOrganizationAdminAccountsPaginator",
    "ListThreatIntelSetsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDetectorsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListDetectors)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listdetectorspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDetectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListDetectors.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listdetectorspaginator)
        """


class ListFiltersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListFilters)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listfilterspaginator)
    """

    def paginate(
        self, *, DetectorId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListFilters.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listfilterspaginator)
        """


class ListFindingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListFindings)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listfindingspaginator)
    """

    def paginate(
        self,
        *,
        DetectorId: str,
        FindingCriteria: FindingCriteriaTypeDef = ...,
        SortCriteria: SortCriteriaTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListFindings.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listfindingspaginator)
        """


class ListIPSetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListIPSets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listipsetspaginator)
    """

    def paginate(
        self, *, DetectorId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListIPSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListIPSets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listipsetspaginator)
        """


class ListInvitationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListInvitations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listinvitationspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListInvitationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListInvitations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listinvitationspaginator)
        """


class ListMembersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListMembers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listmemberspaginator)
    """

    def paginate(
        self,
        *,
        DetectorId: str,
        OnlyAssociated: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListMembers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listmemberspaginator)
        """


class ListOrganizationAdminAccountsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListOrganizationAdminAccounts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listorganizationadminaccountspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOrganizationAdminAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListOrganizationAdminAccounts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listorganizationadminaccountspaginator)
        """


class ListThreatIntelSetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListThreatIntelSets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listthreatintelsetspaginator)
    """

    def paginate(
        self, *, DetectorId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThreatIntelSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Paginator.ListThreatIntelSets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/paginators/#listthreatintelsetspaginator)
        """
